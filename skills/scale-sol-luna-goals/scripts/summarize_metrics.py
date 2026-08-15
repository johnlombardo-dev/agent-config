#!/usr/bin/env python3
"""Summarize one SSLG invocation as JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from path_conventions import canonical_record_id, canonical_repository_id


SCHEMA_VERSION = 2
DEFAULT_ROOT = Path.home() / ".codex" / "subagent-metrics" / "scale-sol-luna-goals"


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


def validate_records(
    records: list[dict[str, Any]],
    repository_id: str,
    skill_use_id: str,
) -> None:
    if not records:
        fail("metrics log has no records")
    if len(records) > 2:
        fail("metrics log contains more than two records")
    expected_types = ["use_started", "use_outcome"]
    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            fail("metrics log uses an unsupported schema version")
        if record.get("repository_id") != repository_id:
            fail("metrics log has a different repository_id")
        if record.get("skill_use_id") != skill_use_id:
            fail("metrics log has a different skill_use_id")
        if record.get("type") != expected_types[index]:
            fail("metrics log is out of order")
        require_string(record, "created_at")

    started = records[0]
    require_string(started, "goal_id")
    require_string(started, "start_fingerprint")
    require_string(started, "started_at")

    if len(records) == 1:
        return
    outcome = records[1]
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
    require_string(outcome, "end_fingerprint")
    require_string(outcome, "completed_at")
    elapsed_ms = outcome.get("elapsed_ms")
    if not isinstance(elapsed_ms, int) or isinstance(elapsed_ms, bool) or elapsed_ms < 0:
        fail("elapsed_ms must be a non-negative integer")
    if outcome.get("timing_status") != "measured":
        fail("timing_status must be measured")
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize one SSLG invocation as JSON.")
    parser.add_argument("--repository-id", required=True)
    parser.add_argument("--skill-use-id", required=True)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help=argparse.SUPPRESS)
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
    validate_records(records, repository_id, skill_use_id)

    started = records[0]
    outcome = records[1] if len(records) == 2 else None
    summary = {
        "repository_id": repository_id,
        "skill_use_id": skill_use_id,
        "goal_id": started["goal_id"],
        "status": outcome["status"] if outcome else "active",
        "failed_criteria": outcome["failed_criteria"] if outcome else [],
        "start_fingerprint": started["start_fingerprint"],
        "end_fingerprint": outcome["end_fingerprint"] if outcome else None,
        "started_at": started["started_at"],
        "completed_at": outcome["completed_at"] if outcome else None,
        "elapsed_ms": outcome["elapsed_ms"] if outcome else None,
        "total_goal_tokens": outcome["total_goal_tokens"] if outcome else None,
        "token_measurement": outcome["token_measurement"] if outcome else None,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
