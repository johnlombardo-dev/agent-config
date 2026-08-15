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
    def append(
        self,
        root: Path,
        payload: dict[str, object],
        *,
        role: str = "orchestrator",
    ) -> dict[str, object]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "append_metric.py"),
                "--repository-id",
                "github.com/example/project",
                "--skill-use-id",
                "use-1",
                "--role",
                role,
                "--root",
                str(root),
            ],
            input=json.dumps(payload),
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_metrics_and_review_events_share_one_timestamped_log(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            started = self.append(
                root,
                {
                    "type": "use_started",
                    "goal_id": "goal-1",
                    "continuation_of": None,
                    "start_fingerprint": "head-1",
                    "completion_criteria": ["done"],
                },
            )
            finding = self.append(
                root,
                {
                    "type": "review_finding",
                    "stage": "local",
                    "finding_id": "finding-1",
                    "cycle_id": "local-1",
                    "severity": "P2",
                    "title": "Example",
                },
                role="writer",
            )

            record_path = root / "github.com/example/project/use-1.jsonl"
            records = [json.loads(line) for line in record_path.read_text().splitlines()]
            self.assertEqual(
                [record["type"] for record in records],
                ["use_started", "review_finding"],
            )
            self.assertEqual(started["repository_id"], "github.com/example/project")
            self.assertIn("created_at", started)
            self.assertIn("created_at", finding)

    def test_writer_cannot_append_an_orchestrator_decision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "append_metric.py"),
                    "--repository-id",
                    "github.com/example/project",
                    "--skill-use-id",
                    "use-1",
                    "--role",
                    "writer",
                    "--root",
                    directory,
                ],
                input='{"type":"review_decision","stage":"local"}',
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot append", result.stderr)


if __name__ == "__main__":
    unittest.main()
