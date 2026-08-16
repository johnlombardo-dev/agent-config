from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from path_conventions import canonical_repository_id, repository_id_from_remote


class RepositoryIdentityTests(unittest.TestCase):
    def test_remote_forms_resolve_to_one_identifier(self) -> None:
        expected = "github.com/programbo/picodash"
        self.assertEqual(
            repository_id_from_remote("git@github.com:programbo/picodash.git"),
            expected,
        )
        self.assertEqual(
            repository_id_from_remote("https://GitHub.com/Programbo/Picodash.git"),
            expected,
        )

    def test_flattened_and_mixed_case_identifiers_are_rejected(self) -> None:
        for value in (
            "github.com-programbo-picodash",
            "github.com_programbo_picodash",
            "github.com/Programbo/picodash",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                canonical_repository_id(value)


class InvocationLogTests(unittest.TestCase):
    repository_id = "github.com/example/project"
    skill_use_id = "use-1"

    def append_result(
        self,
        root: Path,
        payload: dict[str, object],
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "append_metric.py"),
                "--repository-id",
                self.repository_id,
                "--skill-use-id",
                self.skill_use_id,
                "--root",
                str(root),
            ],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
        )

    def append(self, root: Path, payload: dict[str, object]) -> dict[str, object]:
        result = self.append_result(root, payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def summarize_result(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "summarize_metrics.py"),
                "--repository-id",
                self.repository_id,
                "--skill-use-id",
                self.skill_use_id,
                "--root",
                str(root),
            ],
            capture_output=True,
            text=True,
        )

    def summarize(self, root: Path) -> dict[str, object]:
        result = self.summarize_result(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def record_path(self, root: Path) -> Path:
        return root / self.repository_id / f"{self.skill_use_id}.jsonl"

    def start_use(self, root: Path) -> dict[str, object]:
        return self.append(
            root,
            {
                "type": "use_started",
                "goal_id": "goal-1",
                "objective": "Implement the plan.",
                "start_fingerprint": "head-1 clean",
            },
        )

    def start_subagent(
        self,
        root: Path,
        assignment_id: str,
        *,
        parent_assignment_id: str | None = None,
        objective: str = "Implement the bounded task.",
    ) -> dict[str, object]:
        return self.append(
            root,
            {
                "type": "subagent_started",
                "assignment_id": assignment_id,
                "parent_assignment_id": parent_assignment_id,
                "role": "luna_worker",
                "requested_model": None,
                "requested_reasoning_effort": "medium",
                "objective": objective,
            },
        )

    def finish_subagent(
        self,
        root: Path,
        assignment_id: str,
        *,
        outcome: str = "completed",
        result: str = "Completed and verified the bounded task.",
    ) -> dict[str, object]:
        return self.append(
            root,
            {
                "type": "subagent_outcome",
                "assignment_id": assignment_id,
                "outcome": outcome,
                "result": result,
            },
        )

    def finish_use(
        self,
        root: Path,
        *,
        status: str = "success",
        failed_criteria: list[str] | None = None,
        tokens: int | None = 1234,
        measurement: str = "runtime",
    ) -> dict[str, object]:
        return self.append(
            root,
            {
                "type": "use_outcome",
                "status": status,
                "result": "Implemented and verified the plan.",
                "failed_criteria": failed_criteria or [],
                "end_fingerprint": "head-2 clean",
                "total_goal_tokens": tokens,
                "token_measurement": measurement,
            },
        )

    def finish_subagent_result(
        self, root: Path, assignment_id: str
    ) -> subprocess.CompletedProcess[str]:
        return self.append_result(
            root,
            {
                "type": "subagent_outcome",
                "assignment_id": assignment_id,
                "outcome": "completed",
                "result": "Completed the task.",
            },
        )

    def finish_use_result(self, root: Path) -> subprocess.CompletedProcess[str]:
        return self.append_result(
            root,
            {
                "type": "use_outcome",
                "status": "success",
                "result": "Implemented the plan.",
                "failed_criteria": [],
                "end_fingerprint": "head-2",
                "total_goal_tokens": 1234,
                "token_measurement": "runtime",
            },
        )

    def test_records_append_only_invocation_and_nested_subagent_pairs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.start_use(root)
            self.start_subagent(
                root,
                "implementation-1",
                objective="Implement the storage migration.",
            )
            prefix = self.record_path(root).read_bytes()

            self.start_subagent(
                root,
                "fixture-1",
                parent_assignment_id="implementation-1",
                objective="Create a bounded migration fixture.",
            )
            self.finish_subagent(
                root,
                "fixture-1",
                outcome="useful-no-go",
                result="Proved that the proposed fixture was unnecessary.",
            )
            self.finish_subagent(
                root,
                "implementation-1",
                result="Implemented the migration and passed its focused tests.",
            )
            self.finish_use(root)

            journal = self.record_path(root).read_bytes()
            self.assertTrue(journal.startswith(prefix))
            records = [json.loads(line) for line in journal.splitlines()]
            self.assertEqual(
                [record["type"] for record in records],
                [
                    "use_started",
                    "subagent_started",
                    "subagent_started",
                    "subagent_outcome",
                    "subagent_outcome",
                    "use_outcome",
                ],
            )

            for record in records:
                self.assertEqual(record["schema_version"], 3)
                self.assertIsInstance(record["created_at"], str)
                self.assertTrue(record["created_at"])
                for forbidden in (
                    "started_at",
                    "completed_at",
                    "elapsed_ms",
                    "timing_status",
                ):
                    self.assertNotIn(forbidden, record)

            for record in records:
                if record["type"].endswith("started"):
                    self.assertIsInstance(record["objective"], str)
                    self.assertTrue(record["objective"])
                else:
                    self.assertIsInstance(record["result"], str)
                    self.assertTrue(record["result"])

            summary = self.summarize(root)
            self.assertEqual(summary["status"], "success")
            self.assertEqual(summary["started_created_at"], records[0]["created_at"])
            self.assertEqual(summary["outcome_created_at"], records[-1]["created_at"])
            self.assertEqual(summary["subagent_count"], 2)
            self.assertEqual(
                summary["subagent_outcome_counts"],
                {"completed": 1, "useful-no-go": 1},
            )
            self.assertEqual(summary["unfinished_assignment_ids"], [])
            self.assertEqual(
                summary["subagents"][1]["parent_assignment_id"],
                "implementation-1",
            )
            self.assertEqual(
                summary["subagents"][1]["result"],
                "Proved that the proposed fixture was unnecessary.",
            )

    def test_zero_subagent_invocation_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.start_use(root)
            self.finish_use(root)
            summary = self.summarize(root)
            self.assertEqual(summary["subagent_count"], 0)
            self.assertEqual(summary["subagent_outcome_counts"], {})

    def test_active_summary_reports_unfinished_subagents_without_inventing_results(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.start_use(root)
            self.start_subagent(root, "implementation-1")
            summary = self.summarize(root)
            self.assertEqual(summary["status"], "active")
            self.assertIsNone(summary["result"])
            self.assertEqual(summary["unfinished_assignment_ids"], ["implementation-1"])
            self.assertIsNone(summary["subagents"][0]["outcome"])
            self.assertIsNone(summary["subagents"][0]["result"])

    def test_unavailable_goal_tokens_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.start_use(root)
            self.finish_use(root, tokens=None, measurement="unavailable")
            summary = self.summarize(root)
            self.assertIsNone(summary["total_goal_tokens"])
            self.assertEqual(summary["token_measurement"], "unavailable")

    def test_invalid_payload_fields_and_values_are_rejected(self) -> None:
        valid_start = {
            "type": "use_started",
            "goal_id": "goal-1",
            "objective": "Implement the plan.",
            "start_fingerprint": "head-1",
        }
        invalid_payloads = (
            {"type": "assignment_outcome"},
            {**valid_start, "observation": "extra"},
            {key: value for key, value in valid_start.items() if key != "objective"},
            {**valid_start, "objective": "first line\nsecond line"},
            {**valid_start, "elapsed_ms": 1},
            {**valid_start, "created_at": "2026-01-01T00:00:00Z"},
        )
        for payload in invalid_payloads:
            with (
                self.subTest(payload=payload),
                tempfile.TemporaryDirectory() as directory,
            ):
                result = self.append_result(Path(directory), payload)
                self.assertNotEqual(result.returncode, 0)

    def test_subagent_payload_requires_objective_result_and_allowed_outcome(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.start_use(root)
            missing_objective = self.append_result(
                root,
                {
                    "type": "subagent_started",
                    "assignment_id": "implementation-1",
                    "parent_assignment_id": None,
                    "role": "worker",
                    "requested_model": None,
                    "requested_reasoning_effort": None,
                },
            )
            self.assertNotEqual(missing_objective.returncode, 0)

            self.start_subagent(root, "implementation-1")
            for payload in (
                {
                    "type": "subagent_outcome",
                    "assignment_id": "implementation-1",
                    "outcome": "completed",
                },
                {
                    "type": "subagent_outcome",
                    "assignment_id": "implementation-1",
                    "outcome": "mysterious",
                    "result": "Something happened.",
                },
                {
                    "type": "subagent_outcome",
                    "assignment_id": "implementation-1",
                    "outcome": "completed",
                    "result": "first line\nsecond line",
                },
            ):
                with self.subTest(payload=payload):
                    result = self.append_result(root, payload)
                    self.assertNotEqual(result.returncode, 0)

    def test_record_order_pairing_and_terminal_completeness_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing_use_start = self.finish_subagent_result(root, "implementation-1")
            self.assertNotEqual(missing_use_start.returncode, 0)

            self.start_use(root)
            missing_parent = self.append_result(
                root,
                {
                    "type": "subagent_started",
                    "assignment_id": "child-1",
                    "parent_assignment_id": "parent-1",
                    "role": "worker",
                    "requested_model": None,
                    "requested_reasoning_effort": None,
                    "objective": "Do the child task.",
                },
            )
            self.assertNotEqual(missing_parent.returncode, 0)

            self.start_subagent(root, "implementation-1")
            duplicate_start = self.append_result(
                root,
                {
                    "type": "subagent_started",
                    "assignment_id": "implementation-1",
                    "parent_assignment_id": None,
                    "role": "worker",
                    "requested_model": None,
                    "requested_reasoning_effort": None,
                    "objective": "Repeat the task.",
                },
            )
            self.assertNotEqual(duplicate_start.returncode, 0)

            unfinished = self.finish_use_result(root)
            self.assertNotEqual(unfinished.returncode, 0)
            self.finish_subagent(root, "implementation-1")
            duplicate_outcome = self.finish_subagent_result(root, "implementation-1")
            self.assertNotEqual(duplicate_outcome.returncode, 0)
            self.finish_use(root)
            after_terminal = self.append_result(
                root,
                {
                    "type": "subagent_started",
                    "assignment_id": "late-1",
                    "parent_assignment_id": None,
                    "role": "worker",
                    "requested_model": None,
                    "requested_reasoning_effort": None,
                    "objective": "Start too late.",
                },
            )
            self.assertNotEqual(after_terminal.returncode, 0)

    def test_legacy_schema_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record_path = self.record_path(root)
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "type": "use_started",
                        "goal_id": "goal-1",
                        "objective": "Implement the plan.",
                        "start_fingerprint": "head-1",
                        "started_at": "2026-01-01T00:00:00Z",
                        "repository_id": self.repository_id,
                        "skill_use_id": self.skill_use_id,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            append_result = self.finish_use_result(root)
            self.assertNotEqual(append_result.returncode, 0)
            summary_result = self.summarize_result(root)
            self.assertNotEqual(summary_result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
