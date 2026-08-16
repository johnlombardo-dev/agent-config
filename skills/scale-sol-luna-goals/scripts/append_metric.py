#!/usr/bin/env python3
"""Append one validated SSLG metric event without rewriting prior records."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from path_conventions import canonical_record_id, canonical_repository_id


SCHEMA_VERSION = 3
DEFAULT_ROOT = Path.home() / ".codex" / "subagent-metrics" / "scale-sol-luna-goals"
PAYLOAD_FIELDS = {
    "use_started": {"type", "goal_id", "objective", "start_fingerprint"},
    "subagent_started": {
        "type",
        "assignment_id",
        "parent_assignment_id",
        "role",
        "requested_model",
        "requested_reasoning_effort",
        "objective",
    },
    "subagent_outcome": {"type", "assignment_id", "outcome", "result"},
    "use_outcome": {
        "type",
        "status",
        "result",
        "failed_criteria",
        "end_fingerprint",
        "total_goal_tokens",
        "token_measurement",
    },
}
ENVELOPE_FIELDS = {
    "schema_version",
    "created_at",
    "repository_id",
    "skill_use_id",
}
OBSOLETE_TIMING_FIELDS = {
    "started_at",
    "completed_at",
    "elapsed_ms",
    "timing_status",
}
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


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )


def require_non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value


def require_one_line_string(value: Any, field: str) -> str:
    result = require_non_empty_string(value, field)
    if "\n" in result or "\r" in result:
        fail(f"{field} must be one line")
    return result


def require_record_id(value: Any, field: str) -> str:
    result = require_non_empty_string(value, field)
    try:
        return canonical_record_id(result, field)
    except ValueError as error:
        fail(str(error))


def require_optional_record_id(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return require_record_id(value, field)


def require_optional_one_line_string(value: Any, field: str) -> str | None:
    if value is None:
        return None
    return require_one_line_string(value, field)


def validate_failed_criteria(value: Any) -> list[str]:
    if not isinstance(value, list):
        fail("failed_criteria must be an array of unique non-empty strings")
    result = [require_non_empty_string(item, "failed_criteria item") for item in value]
    if len(result) != len(set(result)):
        fail("failed_criteria must not contain duplicates")
    return result


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    record_type = payload.get("type")
    if record_type not in PAYLOAD_FIELDS:
        fail(f"unsupported metric type: {record_type!r}")

    forbidden = (ENVELOPE_FIELDS | OBSOLETE_TIMING_FIELDS).intersection(payload)
    if forbidden:
        fail(f"the append helper does not accept: {', '.join(sorted(forbidden))}")

    expected = PAYLOAD_FIELDS[record_type]
    missing = expected.difference(payload)
    unknown = set(payload).difference(expected)
    if missing:
        fail(f"{record_type} is missing fields: {', '.join(sorted(missing))}")
    if unknown:
        fail(f"{record_type} has unknown fields: {', '.join(sorted(unknown))}")

    if record_type == "use_started":
        payload["goal_id"] = require_record_id(payload["goal_id"], "goal_id")
        require_one_line_string(payload["objective"], "objective")
        require_non_empty_string(payload["start_fingerprint"], "start_fingerprint")
        return payload

    if record_type == "subagent_started":
        payload["assignment_id"] = require_record_id(
            payload["assignment_id"], "assignment_id"
        )
        payload["parent_assignment_id"] = require_optional_record_id(
            payload["parent_assignment_id"], "parent_assignment_id"
        )
        require_one_line_string(payload["role"], "role")
        require_optional_one_line_string(payload["requested_model"], "requested_model")
        require_optional_one_line_string(
            payload["requested_reasoning_effort"], "requested_reasoning_effort"
        )
        require_one_line_string(payload["objective"], "objective")
        return payload

    if record_type == "subagent_outcome":
        payload["assignment_id"] = require_record_id(
            payload["assignment_id"], "assignment_id"
        )
        if payload["outcome"] not in SUBAGENT_OUTCOMES:
            fail(f"outcome must be one of: {', '.join(sorted(SUBAGENT_OUTCOMES))}")
        require_one_line_string(payload["result"], "result")
        return payload

    status = payload["status"]
    if status not in {"success", "failure", "blocked"}:
        fail("status must be success, failure, or blocked")
    failed_criteria = validate_failed_criteria(payload["failed_criteria"])
    if status == "success" and failed_criteria:
        fail("failed_criteria must be empty when status is success")
    if status == "failure" and not failed_criteria:
        fail("failed_criteria must name at least one check when status is failure")
    require_one_line_string(payload["result"], "result")
    require_non_empty_string(payload["end_fingerprint"], "end_fingerprint")

    tokens = payload["total_goal_tokens"]
    measurement = payload["token_measurement"]
    measured_tokens = (
        isinstance(tokens, int) and not isinstance(tokens, bool) and tokens >= 0
    )
    if measurement == "runtime" and not measured_tokens:
        fail(
            "runtime token measurement requires a non-negative integer total_goal_tokens"
        )
    if measurement == "unavailable" and tokens is not None:
        fail("unavailable token measurement requires total_goal_tokens to be null")
    if measurement not in {"runtime", "unavailable"}:
        fail("token_measurement must be runtime or unavailable")
    return payload


def read_payload() -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        fail(f"stdin must contain one JSON object: {error}")
    if not isinstance(payload, dict):
        fail("stdin must contain one JSON object")
    return validate_payload(payload)


def load_records(handle: Any) -> list[dict[str, Any]]:
    handle.seek(0)
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(handle, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            fail(f"existing JSONL is invalid at line {line_number}: {error}")
        if not isinstance(record, dict):
            fail(f"existing JSONL line {line_number} must be an object")
        records.append(record)
    return records


def inspect_log(
    records: list[dict[str, Any]], repository_id: str, skill_use_id: str
) -> tuple[set[str], set[str], bool]:
    started_assignments: set[str] = set()
    finished_assignments: set[str] = set()
    use_outcome_seen = False

    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            fail("existing metrics log uses an unsupported schema version")
        if record.get("repository_id") != repository_id:
            fail("existing metrics log has a different repository_id")
        if record.get("skill_use_id") != skill_use_id:
            fail("existing metrics log has a different skill_use_id")
        record_type = record.get("type")
        if index == 0 and record_type != "use_started":
            fail("existing metrics log must begin with use_started")
        if index > 0 and record_type == "use_started":
            fail("existing metrics log contains duplicate use_started")
        if use_outcome_seen:
            fail("existing metrics log contains records after use_outcome")

        if record_type == "subagent_started":
            assignment_id = require_record_id(
                record.get("assignment_id"), "assignment_id"
            )
            if assignment_id in started_assignments:
                fail(f"duplicate subagent_started for {assignment_id}")
            parent_id = require_optional_record_id(
                record.get("parent_assignment_id"), "parent_assignment_id"
            )
            if parent_id is not None and parent_id not in started_assignments:
                fail(f"parent assignment has not started: {parent_id}")
            started_assignments.add(assignment_id)
        elif record_type == "subagent_outcome":
            assignment_id = require_record_id(
                record.get("assignment_id"), "assignment_id"
            )
            if assignment_id not in started_assignments:
                fail(f"subagent_outcome has no matching start: {assignment_id}")
            if assignment_id in finished_assignments:
                fail(f"duplicate subagent_outcome for {assignment_id}")
            finished_assignments.add(assignment_id)
        elif record_type == "use_outcome":
            use_outcome_seen = True
        elif record_type != "use_started":
            fail(f"unsupported record type in existing log: {record_type!r}")

    return started_assignments, finished_assignments, use_outcome_seen


def validate_append(
    payload: dict[str, Any],
    records: list[dict[str, Any]],
    repository_id: str,
    skill_use_id: str,
) -> None:
    record_type = payload["type"]
    if record_type == "use_started":
        if records:
            fail("use_started already exists for this skill_use_id")
        return
    if not records:
        fail(f"{record_type} requires an existing use_started record")

    started, finished, use_outcome_seen = inspect_log(
        records, repository_id, skill_use_id
    )
    if use_outcome_seen:
        fail("no records may be appended after use_outcome")

    if record_type == "subagent_started":
        assignment_id = payload["assignment_id"]
        if assignment_id in started:
            fail(f"subagent_started already exists for {assignment_id}")
        parent_id = payload["parent_assignment_id"]
        if parent_id is not None and parent_id not in started:
            fail(f"parent assignment has not started: {parent_id}")
    elif record_type == "subagent_outcome":
        assignment_id = payload["assignment_id"]
        if assignment_id not in started:
            fail(f"subagent_outcome requires a matching start: {assignment_id}")
        if assignment_id in finished:
            fail(f"subagent_outcome already exists for {assignment_id}")
    elif record_type == "use_outcome":
        unfinished = sorted(started.difference(finished))
        if unfinished:
            fail(f"use_outcome requires terminal records for: {', '.join(unfinished)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one validated SSLG metric event without rewriting prior records."
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
    payload = read_payload()

    record_path = args.root.expanduser() / repository_id / f"{skill_use_id}.jsonl"
    record_path.parent.mkdir(parents=True, exist_ok=True)

    with record_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        records = load_records(handle)
        validate_append(payload, records, repository_id, skill_use_id)
        record = {
            "schema_version": SCHEMA_VERSION,
            **payload,
            "created_at": utc_now(),
            "repository_id": repository_id,
            "skill_use_id": skill_use_id,
        }
        serialized = json.dumps(record, separators=(",", ":"), sort_keys=True)
        handle.seek(0, os.SEEK_END)
        handle.write(f"{serialized}\n")
        handle.flush()
        os.fsync(handle.fileno())
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    print(serialized)


if __name__ == "__main__":
    main()
