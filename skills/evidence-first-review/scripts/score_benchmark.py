#!/usr/bin/env python3

"""Validate and score paired review-skill benchmark results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SEVERITY_WEIGHTS = {"P0": 8, "P1": 5, "P2": 3, "P3": 1}
KINDS = {"discovery", "repair"}
SPLITS = {"development", "holdout"}
LANES = {
    "value-integrity",
    "accessibility-interaction",
    "public-contract",
    "lifecycle-rendering",
    "control",
}


class BenchmarkError(ValueError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise BenchmarkError(f"cannot read JSON from {path}: {error}") from error


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise BenchmarkError(f"cannot read JSONL from {path}: {error}") from error

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise BenchmarkError(f"invalid JSONL at {path}:{line_number}: {error}") from error
        if not isinstance(record, dict):
            raise BenchmarkError(f"record at {path}:{line_number} must be an object")
        records.append(record)
    return records


def require_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(keys - value.keys())
    if missing:
        raise BenchmarkError(f"{label} is missing: {', '.join(missing)}")


def validate_corpus(corpus: Any, root: Path) -> dict[str, dict[str, Any]]:
    if not isinstance(corpus, dict) or corpus.get("schema_version") != 1:
        raise BenchmarkError("corpus must use schema_version 1")
    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        raise BenchmarkError("corpus cases must be a non-empty array")

    indexed: dict[str, dict[str, Any]] = {}
    for index, case in enumerate(cases):
        label = f"corpus case {index}"
        if not isinstance(case, dict):
            raise BenchmarkError(f"{label} must be an object")
        require_keys(case, {"id", "kind", "split", "lane", "project", "packet"}, label)
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            raise BenchmarkError(f"{label} id must be a non-empty string")
        if case_id in indexed:
            raise BenchmarkError(f"duplicate corpus case id: {case_id}")
        if case["kind"] not in KINDS:
            raise BenchmarkError(f"{case_id} has invalid kind")
        if case["split"] not in SPLITS:
            raise BenchmarkError(f"{case_id} has invalid split")
        if case["lane"] not in LANES:
            raise BenchmarkError(f"{case_id} has invalid lane")
        if not isinstance(case["project"], str) or not case["project"]:
            raise BenchmarkError(f"{case_id} project must be a non-empty string")
        packet = root / case["packet"]
        if not packet.is_file():
            raise BenchmarkError(f"{case_id} packet does not exist: {packet}")
        indexed[case_id] = case
    return indexed


def validate_answers(answers: Any, cases: dict[str, dict[str, Any]], corpus_root: Path) -> dict[str, list[dict[str, str]]]:
    if not isinstance(answers, dict) or answers.get("schema_version") != 1:
        raise BenchmarkError("answers must use schema_version 1")
    raw_answers = answers.get("answers")
    if not isinstance(raw_answers, dict) or set(raw_answers) != set(cases):
        raise BenchmarkError("answers must contain exactly one entry for every corpus case")

    indexed: dict[str, list[dict[str, str]]] = {}
    finding_ids: set[str] = set()
    for case_id, answer in raw_answers.items():
        if not isinstance(answer, dict) or not isinstance(answer.get("findings"), list):
            raise BenchmarkError(f"answer for {case_id} must contain a findings array")
        findings: list[dict[str, str]] = []
        for finding in answer["findings"]:
            if not isinstance(finding, dict):
                raise BenchmarkError(f"finding for {case_id} must be an object")
            require_keys(finding, {"id", "severity", "defect_class"}, f"finding for {case_id}")
            finding_id = finding["id"]
            if not isinstance(finding_id, str) or not finding_id:
                raise BenchmarkError(f"finding id for {case_id} must be a non-empty string")
            if finding_id in finding_ids:
                raise BenchmarkError(f"duplicate finding id: {finding_id}")
            if finding["severity"] not in SEVERITY_WEIGHTS:
                raise BenchmarkError(f"{finding_id} has invalid severity")
            if not isinstance(finding["defect_class"], str) or not finding["defect_class"]:
                raise BenchmarkError(f"{finding_id} defect_class must be a non-empty string")
            finding_ids.add(finding_id)
            findings.append(finding)

        packet_text = (corpus_root / cases[case_id]["packet"]).read_text(encoding="utf-8")
        leaked = [
            value
            for finding in findings
            for value in (finding["id"], finding["defect_class"])
            if value in packet_text
        ]
        if leaked:
            raise BenchmarkError(f"{case_id} packet leaks answer ids: {', '.join(leaked)}")
        indexed[case_id] = findings
    return indexed


def validate_results(
    records: list[dict[str, Any]],
    cases: dict[str, dict[str, Any]],
    required_pairs: set[tuple[str, str]],
) -> dict[tuple[str, str], dict[str, Any]]:
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    required = {
        "approach",
        "case_id",
        "detected_finding_ids",
        "false_positives",
        "input_tokens",
        "output_tokens",
        "elapsed_ms",
    }
    for index, record in enumerate(records):
        label = f"result record {index}"
        require_keys(record, required, label)
        approach = record["approach"]
        case_id = record["case_id"]
        if case_id not in cases:
            raise BenchmarkError(f"{label} has unknown case_id: {case_id}")
        key = (approach, case_id)
        if key not in required_pairs:
            raise BenchmarkError(f"{label} has unexpected approach/case pair: {approach}/{case_id}")
        if key in indexed:
            raise BenchmarkError(f"duplicate result for {approach}/{case_id}")
        detected = record["detected_finding_ids"]
        if not isinstance(detected, list) or not all(isinstance(item, str) for item in detected):
            raise BenchmarkError(f"{label} detected_finding_ids must be a string array")
        if len(detected) != len(set(detected)):
            raise BenchmarkError(f"{label} detected_finding_ids contains duplicates")
        for field in ("false_positives", "input_tokens", "output_tokens"):
            value = record[field]
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise BenchmarkError(f"{label} {field} must be a non-negative integer")
        elapsed = record["elapsed_ms"]
        if elapsed is not None and (
            not isinstance(elapsed, int) or isinstance(elapsed, bool) or elapsed < 0
        ):
            raise BenchmarkError(f"{label} elapsed_ms must be null or a non-negative integer")
        indexed[key] = record

    missing = sorted(required_pairs - indexed.keys())
    if missing:
        rendered = ", ".join(f"{approach}/{case_id}" for approach, case_id in missing)
        raise BenchmarkError(f"results are missing required pairs: {rendered}")
    return indexed


def score_slice(
    *,
    cases: dict[str, dict[str, Any]],
    answers: dict[str, list[dict[str, str]]],
    results: dict[tuple[str, str], dict[str, Any]],
    approach: str,
    kind: str,
    split: str,
) -> dict[str, Any]:
    case_ids = [case_id for case_id, case in cases.items() if case["kind"] == kind and case["split"] == split]
    total_weight = 0
    detected_weight = 0
    true_positives = 0
    false_positives = 0
    expected_classes: set[str] = set()
    detected_classes: set[str] = set()
    total_tokens = 0
    elapsed_values: list[int] = []
    elapsed_available = True

    for case_id in case_ids:
        expected = {finding["id"]: finding for finding in answers[case_id]}
        record = results[(approach, case_id)]
        detected = set(record["detected_finding_ids"])
        unknown = detected - expected.keys()
        true_ids = detected & expected.keys()
        total_weight += sum(SEVERITY_WEIGHTS[finding["severity"]] for finding in expected.values())
        detected_weight += sum(SEVERITY_WEIGHTS[expected[finding_id]["severity"]] for finding_id in true_ids)
        true_positives += len(true_ids)
        false_positives += record["false_positives"] + len(unknown)
        expected_classes.update(finding["defect_class"] for finding in expected.values())
        detected_classes.update(expected[finding_id]["defect_class"] for finding_id in true_ids)
        total_tokens += record["input_tokens"] + record["output_tokens"]
        elapsed = record["elapsed_ms"]
        if elapsed is None:
            elapsed_available = False
        else:
            elapsed_values.append(elapsed)

    precision_denominator = true_positives + false_positives
    metrics = {
        "cases": len(case_ids),
        "weighted_recall": detected_weight / total_weight if total_weight else 1.0,
        "precision": true_positives / precision_denominator if precision_denominator else 1.0,
        "defect_class_coverage": len(detected_classes) / len(expected_classes) if expected_classes else 1.0,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "total_tokens": total_tokens,
        "cost_per_true_finding": total_tokens / true_positives if true_positives else None,
        "elapsed_ms": sum(elapsed_values) if elapsed_available else None,
    }
    if kind == "repair":
        metrics["repair_escape_detection"] = metrics["weighted_recall"]
    return metrics


def cost_ratio(candidate: dict[str, Any], baseline: dict[str, Any]) -> float | None:
    if baseline["total_tokens"] == 0:
        return None
    return candidate["total_tokens"] / baseline["total_tokens"]


def discovery_passes(candidate: dict[str, Any], baseline: dict[str, Any]) -> bool:
    precision_ok = candidate["precision"] >= baseline["precision"] - 0.05
    recall_gain = (
        candidate["weighted_recall"] > 0
        if baseline["weighted_recall"] == 0
        else candidate["weighted_recall"] >= baseline["weighted_recall"] * 1.25
    )
    ratio = cost_ratio(candidate, baseline)
    equal_recall_lower_cost = (
        candidate["weighted_recall"] >= baseline["weighted_recall"]
        and ratio is not None
        and ratio <= 0.60
    )
    return precision_ok and (recall_gain or equal_recall_lower_cost)


def repair_passes(candidate: dict[str, Any], baseline: dict[str, Any]) -> bool:
    ratio = cost_ratio(candidate, baseline)
    return (
        candidate["weighted_recall"] >= baseline["weighted_recall"]
        and candidate["precision"] >= baseline["precision"]
        and ratio is not None
        and ratio <= 0.60
    )


def build_report(
    cases: dict[str, dict[str, Any]],
    answers: dict[str, list[dict[str, str]]],
    results: dict[tuple[str, str], dict[str, Any]],
    baseline: str,
    discovery_candidate: str,
    repair_candidate: str,
    splits: set[str] | None = None,
) -> dict[str, Any]:
    selected_splits = splits or SPLITS
    report: dict[str, Any] = {
        "schema_version": 1,
        "approaches": {
            baseline: {
                kind: {
                    split: score_slice(
                        cases=cases,
                        answers=answers,
                        results=results,
                        approach=baseline,
                        kind=kind,
                        split=split,
                    )
                    for split in sorted(selected_splits)
                }
                for kind in sorted(KINDS)
            },
            discovery_candidate: {
                "discovery": {
                    split: score_slice(
                        cases=cases,
                        answers=answers,
                        results=results,
                        approach=discovery_candidate,
                        kind="discovery",
                        split=split,
                    )
                    for split in sorted(selected_splits)
                }
            },
            repair_candidate: {
                "repair": {
                    split: score_slice(
                        cases=cases,
                        answers=answers,
                        results=results,
                        approach=repair_candidate,
                        kind="repair",
                        split=split,
                    )
                    for split in sorted(selected_splits)
                }
            },
        },
    }

    report["gates"] = {}
    if "holdout" in selected_splits:
        discovery_base = report["approaches"][baseline]["discovery"]["holdout"]
        discovery_new = report["approaches"][discovery_candidate]["discovery"]["holdout"]
        repair_base = report["approaches"][baseline]["repair"]["holdout"]
        repair_new = report["approaches"][repair_candidate]["repair"]["holdout"]
        report["gates"] = {
            "discovery": {
                "passed": discovery_passes(discovery_new, discovery_base),
                "cost_ratio": cost_ratio(discovery_new, discovery_base),
            },
            "repair": {
                "passed": repair_passes(repair_new, repair_base),
                "cost_ratio": cost_ratio(repair_new, repair_base),
            },
        }
        report["passed"] = all(gate["passed"] for gate in report["gates"].values())
    else:
        report["passed"] = None
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--baseline", default="review-agent")
    parser.add_argument("--discovery-candidate", default="evidence-first-review")
    parser.add_argument("--repair-candidate", default="verify-repair-seam")
    parser.add_argument("--split", choices=["all", *sorted(SPLITS)], default="all")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        corpus = load_json(args.corpus)
        cases = validate_corpus(corpus, args.corpus.parent)
        answers = validate_answers(load_json(args.answers), cases, args.corpus.parent)
        selected_splits = SPLITS if args.split == "all" else {args.split}
        selected_cases = {
            case_id: case for case_id, case in cases.items() if case["split"] in selected_splits
        }
        required_pairs = {
            (args.baseline, case_id) for case_id in selected_cases
        } | {
            (args.discovery_candidate, case_id)
            for case_id, case in selected_cases.items()
            if case["kind"] == "discovery"
        } | {
            (args.repair_candidate, case_id)
            for case_id, case in selected_cases.items()
            if case["kind"] == "repair"
        }
        results = validate_results(load_jsonl(args.results), cases, required_pairs)
        report = build_report(
            cases,
            answers,
            results,
            args.baseline,
            args.discovery_candidate,
            args.repair_candidate,
            selected_splits,
        )
    except BenchmarkError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["passed"] is False else 0


if __name__ == "__main__":
    raise SystemExit(main())
