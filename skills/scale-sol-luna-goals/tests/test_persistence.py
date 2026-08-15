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
                "github.com/example/project",
                "--skill-use-id",
                "use-1",
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

    def summarize(self, root: Path) -> dict[str, object]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "summarize_metrics.py"),
                "--repository-id",
                "github.com/example/project",
                "--skill-use-id",
                "use-1",
                "--root",
                str(root),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def start(self, root: Path) -> dict[str, object]:
        return self.append(
            root,
            {
                "type": "use_started",
                "goal_id": "goal-1",
                "objective": "Implement the plan.",
                "start_fingerprint": "head-1 clean",
            },
        )

    def outcome(
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

    def test_records_only_start_and_terminal_whole_goal_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            started = self.start(root)
            outcome = self.outcome(
                root,
                status="failure",
                failed_criteria=["criterion-2"],
            )

            record_path = root / "github.com/example/project/use-1.jsonl"
            records = [json.loads(line) for line in record_path.read_text().splitlines()]
            self.assertEqual([record["type"] for record in records], ["use_started", "use_outcome"])
            self.assertEqual(started["schema_version"], 2)
            self.assertIn("started_at", started)
            self.assertEqual(outcome["total_goal_tokens"], 1234)
            self.assertIsInstance(outcome["elapsed_ms"], int)

            summary = self.summarize(root)
            self.assertEqual(summary["status"], "failure")
            self.assertEqual(summary["objective"], "Implement the plan.")
            self.assertEqual(summary["result"], "Implemented and verified the plan.")
            self.assertEqual(summary["failed_criteria"], ["criterion-2"])
            self.assertEqual(summary["total_goal_tokens"], 1234)
            self.assertEqual(summary["token_measurement"], "runtime")

    def test_unavailable_tokens_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.start(root)
            self.outcome(root, tokens=None, measurement="unavailable")
            summary = self.summarize(root)
            self.assertIsNone(summary["total_goal_tokens"])
            self.assertEqual(summary["token_measurement"], "unavailable")

    def test_active_summary_does_not_invent_an_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.start(root)
            summary = self.summarize(root)
            self.assertEqual(summary["status"], "active")
            self.assertEqual(summary["objective"], "Implement the plan.")
            self.assertIsNone(summary["result"])
            self.assertIsNone(summary["elapsed_ms"])
            self.assertIsNone(summary["total_goal_tokens"])
            self.assertIsNone(summary["token_measurement"])

    def test_invalid_or_extra_fields_are_rejected(self) -> None:
        invalid_payloads = (
            {"type": "assignment_outcome"},
            {
                "type": "use_started",
                "goal_id": "goal-1",
                "objective": "Implement the plan.",
                "start_fingerprint": "head-1",
                "observation": "extra",
            },
            {"type": "use_started", "goal_id": "goal-1"},
            {
                "type": "use_started",
                "goal_id": "goal-1",
                "objective": "first line\nsecond line",
                "start_fingerprint": "head-1",
            },
            {
                "type": "use_outcome",
                "status": "success",
                "result": "Implemented the plan.",
                "failed_criteria": ["criterion-1"],
                "end_fingerprint": "head-2",
                "total_goal_tokens": 1,
                "token_measurement": "runtime",
            },
            {
                "type": "use_outcome",
                "status": "blocked",
                "failed_criteria": [],
                "end_fingerprint": "head-2",
                "total_goal_tokens": None,
                "token_measurement": "unavailable",
            },
            {
                "type": "use_outcome",
                "status": "blocked",
                "result": "first line\nsecond line",
                "failed_criteria": [],
                "end_fingerprint": "head-2",
                "total_goal_tokens": None,
                "token_measurement": "unavailable",
            },
            {
                "type": "use_outcome",
                "status": "failure",
                "result": "The plan failed.",
                "failed_criteria": [],
                "end_fingerprint": "head-2",
                "total_goal_tokens": 1,
                "token_measurement": "runtime",
            },
            {
                "type": "use_outcome",
                "status": "failure",
                "result": "The plan failed.",
                "failed_criteria": ["criterion-1"],
                "end_fingerprint": "head-2",
                "total_goal_tokens": -1,
                "token_measurement": "runtime",
            },
            {
                "type": "use_outcome",
                "status": "blocked",
                "result": "The plan was blocked.",
                "failed_criteria": [],
                "end_fingerprint": "head-2",
                "total_goal_tokens": 1,
                "token_measurement": "unavailable",
            },
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as directory:
                result = self.append_result(Path(directory), payload)
                self.assertNotEqual(result.returncode, 0)

    def test_records_must_be_ordered_and_unique(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing_start = self.append_result(
                root,
                {
                    "type": "use_outcome",
                    "status": "blocked",
                    "result": "The plan was blocked.",
                    "failed_criteria": [],
                    "end_fingerprint": "head-1",
                    "total_goal_tokens": None,
                    "token_measurement": "unavailable",
                },
            )
            self.assertNotEqual(missing_start.returncode, 0)

            self.start(root)
            duplicate_start = self.append_result(
                root,
                {
                    "type": "use_started",
                    "goal_id": "goal-1",
                    "objective": "Implement the plan.",
                    "start_fingerprint": "head-1",
                },
            )
            self.assertNotEqual(duplicate_start.returncode, 0)

            self.outcome(root)
            duplicate_outcome = self.append_result(
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
            self.assertNotEqual(duplicate_outcome.returncode, 0)

    def test_legacy_schema_is_not_extended(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record_path = root / "github.com/example/project/use-1.jsonl"
            record_path.parent.mkdir(parents=True)
            record_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "type": "use_started",
                        "repository_id": "github.com/example/project",
                        "skill_use_id": "use-1",
                        "started_at": "2026-08-15T00:00:00.000Z",
                    }
                )
                + "\n"
            )
            result = self.append_result(
                root,
                {
                    "type": "use_outcome",
                    "status": "blocked",
                    "result": "The plan was blocked.",
                    "failed_criteria": [],
                    "end_fingerprint": "head-1",
                    "total_goal_tokens": None,
                    "token_measurement": "unavailable",
                },
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported schema", result.stderr)


if __name__ == "__main__":
    unittest.main()
