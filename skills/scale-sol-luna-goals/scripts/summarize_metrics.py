#!/usr/bin/env python3
"""Summarize one SSLG invocation and its subagent journal as JSON."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from path_conventions import canonical_record_id, canonical_repository_id


SCHEMA_VERSION = 3
DEFAULT_ROOT = Path.home() / ".codex" / "subagent-metrics" / "scale-sol-luna-goals"
SUBAGENT_OUTCOMES = {
    "completed",
    "useful-no-go",
    "failed",
    "blocked",
    "cancelled",
    "interrupted",
    "superseded",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def load_records(record_path: Path) -> list[dict[str, Any]]:
    if not record_path.is_file():
        fail(f"metrics file does not exist: {record_path}")
    records: list[dict[str, Any]] = []
    with record_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                fail(f"invalid JSONL at line {line_number}: {error}")
            if not isinstance(record, dict):
                fail(f"metrics line {line_number} must be an object")
            records.append(record)
    return records


def require_string(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value


def require_one_line_string(record: dict[str, Any], field: str) -> str:
    value = require_string(record, field)
    if "\n" in value or "\r" in value:
        fail(f"{field} must be one line")
    return value


def require_optional_one_line_string(record: dict[str, Any], field: str) -> str | None:
    if record.get(field) is None:
        return None
    return require_one_line_string(record, field)


def require_id(record: dict[str, Any], field: str) -> str:
    value = require_string(record, field)
    try:
        return canonical_record_id(value, field)
    except ValueError as error:
        fail(str(error))


def validate_envelope(
    record: dict[str, Any], repository_id: str, skill_use_id: str
) -> None:
    if record.get("schema_version") != SCHEMA_VERSION:
        fail("metrics log uses an unsupported schema version")
    if record.get("repository_id") != repository_id:
        fail("metrics log has a different repository_id")
    if record.get("skill_use_id") != skill_use_id:
        fail("metrics log has a different skill_use_id")
    require_one_line_string(record, "created_at")


def validate_use_outcome(outcome: dict[str, Any]) -> None:
    if outcome.get("status") not in {"success", "failure", "blocked"}:
        fail("outcome status is invalid")
    failed_criteria = outcome.get("failed_criteria")
    if not isinstance(failed_criteria, list) or any(
        not isinstance(item, str) or not item.strip() for item in failed_criteria
    ):
        fail("failed_criteria must be an array of non-empty strings")
    if len(failed_criteria) != len(set(failed_criteria)):
        fail("failed_criteria must not contain duplicates")
    if outcome["status"] == "success" and failed_criteria:
        fail("successful outcome must not contain failed criteria")
    if outcome["status"] == "failure" and not failed_criteria:
        fail("failed outcome must name at least one failed criterion")
    require_one_line_string(outcome, "result")
    require_string(outcome, "end_fingerprint")

    tokens = outcome.get("total_goal_tokens")
    measurement = outcome.get("token_measurement")
    if measurement == "runtime":
        if not isinstance(tokens, int) or isinstance(tokens, bool) or tokens < 0:
            fail("runtime token measurement is invalid")
    elif measurement == "unavailable":
        if tokens is not None:
            fail("unavailable token measurement is invalid")
    else:
        fail("token_measurement is invalid")


def validate_records(
    records: list[dict[str, Any]], repository_id: str, skill_use_id: str
) -> tuple[dict[str, Any], dict[str, Any] | None, list[dict[str, Any]]]:
    if not records:
        fail("metrics log has no records")

    started = records[0]
    if started.get("type") != "use_started":
        fail("metrics log must begin with use_started")
    validate_envelope(started, repository_id, skill_use_id)
    require_id(started, "goal_id")
    require_one_line_string(started, "objective")
    require_string(started, "start_fingerprint")

    starts: dict[str, dict[str, Any]] = {}
    outcomes: dict[str, dict[str, Any]] = {}
    use_outcome: dict[str, Any] | None = None

    for record in records[1:]:
        validate_envelope(record, repository_id, skill_use_id)
        record_type = record.get("type")
        if use_outcome is not None:
            fail("metrics log contains records after use_outcome")
        if record_type == "use_started":
            fail("metrics log contains duplicate use_started")
        if record_type == "subagent_started":
            assignment_id = require_id(record, "assignment_id")
            if assignment_id in starts:
                fail(f"duplicate subagent_started for {assignment_id}")
            parent_id = record.get("parent_assignment_id")
            if parent_id is not None:
                try:
                    parent_id = canonical_record_id(parent_id, "parent_assignment_id")
                except (TypeError, ValueError) as error:
                    fail(str(error))
                if parent_id not in starts:
                    fail(f"parent assignment has not started: {parent_id}")
            require_one_line_string(record, "role")
            require_optional_one_line_string(record, "requested_model")
            require_optional_one_line_string(record, "requested_reasoning_effort")
            require_one_line_string(record, "model")
            require_one_line_string(record, "reasoning_effort")
            require_one_line_string(record, "objective")
            starts[assignment_id] = record
        elif record_type == "subagent_outcome":
            assignment_id = require_id(record, "assignment_id")
            if assignment_id not in starts:
                fail(f"subagent_outcome has no matching start: {assignment_id}")
            if assignment_id in outcomes:
                fail(f"duplicate subagent_outcome for {assignment_id}")
            if record.get("outcome") not in SUBAGENT_OUTCOMES:
                fail("subagent outcome is invalid")
            require_one_line_string(record, "result")
            outcomes[assignment_id] = record
        elif record_type == "use_outcome":
            validate_use_outcome(record)
            use_outcome = record
        else:
            fail(f"unsupported record type: {record_type!r}")

    unfinished = sorted(set(starts).difference(outcomes))
    if use_outcome is not None and unfinished:
        fail(
            f"terminal invocation contains unfinished subagents: {', '.join(unfinished)}"
        )

    invocations: list[dict[str, Any]] = []
    for assignment_id, start in starts.items():
        outcome = outcomes.get(assignment_id)
        invocations.append(
            {
                "assignment_id": assignment_id,
                "parent_assignment_id": start.get("parent_assignment_id"),
                "role": start.get("role"),
                "requested_model": start.get("requested_model"),
                "requested_reasoning_effort": start.get("requested_reasoning_effort"),
                "model": start.get("model"),
                "reasoning_effort": start.get("reasoning_effort"),
                "objective": start.get("objective"),
                "started_created_at": start.get("created_at"),
                "outcome": outcome.get("outcome") if outcome else None,
                "result": outcome.get("result") if outcome else None,
                "outcome_created_at": outcome.get("created_at") if outcome else None,
            }
        )
    return started, use_outcome, invocations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize one SSLG invocation and its subagent journal as JSON."
    )
    parser.add_argument("--repository-id", required=True)
    parser.add_argument("--skill-use-id", required=True)
    parser.add_argument(
        "--root", type=Path, default=DEFAULT_ROOT, help=argparse.SUPPRESS
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        repository_id = canonical_repository_id(args.repository_id)
        skill_use_id = canonical_record_id(args.skill_use_id, "skill_use_id")
    except ValueError as error:
        fail(str(error))
    record_path = args.root.expanduser() / repository_id / f"{skill_use_id}.jsonl"
    records = load_records(record_path)
    started, outcome, invocations = validate_records(
        records, repository_id, skill_use_id
    )
    outcome_counts = Counter(
        invocation["outcome"]
        for invocation in invocations
        if invocation["outcome"] is not None
    )
    summary = {
        "repository_id": repository_id,
        "skill_use_id": skill_use_id,
        "goal_id": started["goal_id"],
        "objective": started["objective"],
        "started_created_at": started["created_at"],
        "status": outcome["status"] if outcome else "active",
        "result": outcome["result"] if outcome else None,
        "outcome_created_at": outcome["created_at"] if outcome else None,
        "failed_criteria": outcome["failed_criteria"] if outcome else [],
        "start_fingerprint": started["start_fingerprint"],
        "end_fingerprint": outcome["end_fingerprint"] if outcome else None,
        "total_goal_tokens": outcome["total_goal_tokens"] if outcome else None,
        "token_measurement": outcome["token_measurement"] if outcome else None,
        "subagent_count": len(invocations),
        "subagent_outcome_counts": dict(sorted(outcome_counts.items())),
        "unfinished_assignment_ids": [
            invocation["assignment_id"]
            for invocation in invocations
            if invocation["outcome"] is None
        ],
        "subagents": invocations,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
