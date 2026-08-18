from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "score_benchmark.py"
SPEC = importlib.util.spec_from_file_location("score_benchmark", SCRIPT_PATH)
assert SPEC and SPEC.loader
score_benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score_benchmark)


class ScoreBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus_path = SKILL_ROOT / "evals" / "corpus.json"
        cls.answers_path = SKILL_ROOT / "evals" / "answers.json"
        cls.cases = score_benchmark.validate_corpus(
            score_benchmark.load_json(cls.corpus_path),
            cls.corpus_path.parent,
        )
        cls.answers = score_benchmark.validate_answers(
            score_benchmark.load_json(cls.answers_path),
            cls.cases,
            cls.corpus_path.parent,
        )

    def required_pairs(self) -> set[tuple[str, str]]:
        return {
            ("review-agent", case_id) for case_id in self.cases
        } | {
            ("evidence-first-review", case_id)
            for case_id, case in self.cases.items()
            if case["kind"] == "discovery"
        } | {
            ("verify-repair-seam", case_id)
            for case_id, case in self.cases.items()
            if case["kind"] == "repair"
        }

    def make_results(self, candidate_cost: int = 40) -> list[dict[str, object]]:
        records: list[dict[str, object]] = []
        for approach, case_id in sorted(self.required_pairs()):
            case = self.cases[case_id]
            expected_ids = [
                finding["id"] for finding in self.answers[case_id]["findings"]
            ]
            if approach == "review-agent":
                detected = expected_ids if case["split"] == "development" else expected_ids[:1]
                if case["kind"] == "discovery" and case["split"] == "holdout" and case["lane"] in {
                    "public-contract",
                    "lifecycle-resource-ownership",
                }:
                    detected = []
                tokens = 100
            else:
                detected = expected_ids
                tokens = candidate_cost
            record = {
                "approach": approach,
                "case_id": case_id,
                "detected_finding_ids": detected,
                "false_positives": 0,
                "input_tokens": tokens,
                "output_tokens": 0,
                "elapsed_ms": tokens,
            }
            if approach == "evidence-first-review":
                record["selected_lanes"] = self.answers[case_id]["routing"][
                    "required_lanes"
                ]
            records.append(record)
        return records

    def validate(self, records: list[dict[str, object]]):
        return score_benchmark.validate_results(
            records, self.cases, self.required_pairs(), "evidence-first-review"
        )

    def report(self, records: list[dict[str, object]]):
        return score_benchmark.build_report(
            self.cases,
            self.answers,
            self.validate(records),
            "review-agent",
            "evidence-first-review",
            "verify-repair-seam",
        )

    def test_shipped_corpus_is_complete_and_blind(self) -> None:
        self.assertEqual(len(self.cases), 31)
        self.assertEqual(
            {case["lane"] for case in self.cases.values()},
            {
                "domain-value-integrity",
                "accessibility-interaction",
                "public-contract",
                "lifecycle-resource-ownership",
                "security-privacy-trust",
                "persistence-migration-recovery",
                "concurrency-workflow-ordering",
                "performance-capacity-backpressure",
                "external-protocol-integration",
                "operations-configuration-deployment",
                "control",
            },
        )
        self.assertIn("generic-react-typescript", {case["project"] for case in self.cases.values()})

    def test_shipped_corpus_contains_cross_boundary_cases(self) -> None:
        expected_routes = {
            "D-COMPOSED-PUBLICATION-DEV": {
                "concurrency-workflow-ordering",
                "persistence-migration-recovery",
                "external-protocol-integration",
            },
            "D-OUTCOME-RECOVERY-HOLDOUT": {
                "persistence-migration-recovery",
                "operations-configuration-deployment",
            },
        }
        for case_id, expected in expected_routes.items():
            self.assertEqual(
                set(self.answers[case_id]["routing"]["required_lanes"]),
                expected,
            )

    def test_answer_id_or_defect_class_leak_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "packet.md").write_text("contains hidden-defect-class", encoding="utf-8")
            cases = {
                "case": {
                    "id": "case",
                    "kind": "discovery",
                    "split": "holdout",
                    "lane": "domain-value-integrity",
                    "project": "fixture",
                    "packet": "packet.md",
                }
            }
            answers = {
                "schema_version": 2,
                "answers": {
                    "case": {
                        "findings": [
                            {
                                "id": "finding-id",
                                "severity": "P2",
                                "defect_class": "hidden-defect-class",
                            }
                        ],
                        "routing": {
                            "required_lanes": ["domain-value-integrity"],
                            "acceptable_lanes": ["domain-value-integrity"],
                            "critical_lanes": [],
                        },
                    }
                },
            }
            with self.assertRaisesRegex(score_benchmark.BenchmarkError, "packet leaks"):
                score_benchmark.validate_answers(answers, cases, root)

    def test_passing_results_meet_both_holdout_gates(self) -> None:
        report = self.report(self.make_results())
        self.assertTrue(report["passed"])
        self.assertTrue(report["gates"]["discovery"]["passed"])
        self.assertTrue(report["gates"]["repair"]["passed"])
        self.assertEqual(
            report["approaches"]["verify-repair-seam"]["repair"]["holdout"][
                "repair_escape_detection"
            ],
            1.0,
        )

    def test_cost_threshold_failure_is_reported(self) -> None:
        report = self.report(self.make_results(candidate_cost=80))
        self.assertFalse(report["gates"]["repair"]["passed"])
        self.assertGreater(report["gates"]["repair"]["cost_ratio"], 0.60)

    def test_zero_baseline_recall_does_not_make_zero_candidate_recall_a_gain(self) -> None:
        baseline = {"weighted_recall": 0.0, "precision": 1.0, "total_tokens": 100}
        candidate = {
            "weighted_recall": 0.0,
            "precision": 1.0,
            "total_tokens": 100,
            "routing": {
                "available": True,
                "critical_lane_recall": 1.0,
                "weighted_required_lane_recall": 1.0,
                "routing_precision": 1.0,
            },
        }
        self.assertFalse(score_benchmark.discovery_passes(candidate, baseline))

    def test_routing_gate_rejects_missed_critical_lane(self) -> None:
        records = self.make_results()
        record = next(
            item
            for item in records
            if item["approach"] == "evidence-first-review"
            and item["case_id"] == "D-SECURITY-HOLDOUT"
        )
        record["selected_lanes"] = []
        report = self.report(records)
        routing = report["approaches"]["evidence-first-review"]["discovery"][
            "holdout"
        ]["routing"]
        self.assertLess(routing["critical_lane_recall"], 1.0)
        self.assertFalse(report["gates"]["discovery"]["passed"])

    def test_routing_gate_rejects_overselection(self) -> None:
        records = self.make_results()
        for record in records:
            if record["approach"] == "evidence-first-review" and self.cases[
                record["case_id"]
            ]["split"] == "holdout":
                record["selected_lanes"] = sorted(score_benchmark.REVIEW_LANES)
        report = self.report(records)
        routing = report["approaches"]["evidence-first-review"]["discovery"][
            "holdout"
        ]["routing"]
        self.assertLess(routing["routing_precision"], 0.75)
        self.assertFalse(report["gates"]["discovery"]["passed"])

    def test_unknown_selected_lane_is_rejected(self) -> None:
        records = self.make_results()
        record = next(
            item for item in records if item["approach"] == "evidence-first-review"
        )
        record["selected_lanes"] = ["everything"]
        with self.assertRaisesRegex(score_benchmark.BenchmarkError, "unknown lanes"):
            self.validate(records)

    def test_candidate_discovery_requires_selected_lanes(self) -> None:
        records = self.make_results()
        record = next(
            item
            for item in records
            if item["approach"] == "evidence-first-review"
        )
        del record["selected_lanes"]
        with self.assertRaisesRegex(score_benchmark.BenchmarkError, "selected_lanes"):
            self.validate(records)

    def test_unknown_detected_id_counts_as_false_positive(self) -> None:
        records = self.make_results()
        record = next(
            item
            for item in records
            if item["approach"] == "evidence-first-review" and item["case_id"] == "D-CONTROL-HOLDOUT"
        )
        record["detected_finding_ids"] = ["UNMAPPED"]
        report = self.report(records)
        metrics = report["approaches"]["evidence-first-review"]["discovery"]["holdout"]
        self.assertEqual(metrics["false_positives"], 1)

    def test_missing_result_pair_is_rejected(self) -> None:
        records = self.make_results()
        records.pop()
        with self.assertRaisesRegex(score_benchmark.BenchmarkError, "missing required pairs"):
            self.validate(records)

    def test_malformed_jsonl_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "results.jsonl"
            path.write_text('{"approach":', encoding="utf-8")
            with self.assertRaisesRegex(score_benchmark.BenchmarkError, "invalid JSONL"):
                score_benchmark.load_jsonl(path)

    def test_missing_elapsed_time_is_reported_without_estimation(self) -> None:
        records = self.make_results()
        records[0]["elapsed_ms"] = None
        report = self.report(records)
        approach = records[0]["approach"]
        case = self.cases[records[0]["case_id"]]
        self.assertIsNone(report["approaches"][approach][case["kind"]][case["split"]]["elapsed_ms"])

    def test_cli_returns_failure_for_failed_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            results_path = Path(temporary_directory) / "results.jsonl"
            results_path.write_text(
                "\n".join(json.dumps(record) for record in self.make_results(candidate_cost=80)) + "\n",
                encoding="utf-8",
            )
            with redirect_stdout(io.StringIO()):
                exit_code = score_benchmark.main(
                    [
                        "--corpus",
                        str(self.corpus_path),
                        "--answers",
                        str(self.answers_path),
                        "--results",
                        str(results_path),
                    ]
                )
            self.assertEqual(exit_code, 1)

    def test_development_score_is_informational_not_a_failed_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            results = [
                record
                for record in self.make_results()
                if self.cases[record["case_id"]]["split"] == "development"
            ]
            results_path = Path(temporary_directory) / "results.jsonl"
            results_path.write_text(
                "\n".join(json.dumps(record) for record in results) + "\n",
                encoding="utf-8",
            )
            with redirect_stdout(io.StringIO()):
                exit_code = score_benchmark.main(
                    [
                        "--corpus",
                        str(self.corpus_path),
                        "--answers",
                        str(self.answers_path),
                        "--results",
                        str(results_path),
                        "--split",
                        "development",
                    ]
                )
            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
