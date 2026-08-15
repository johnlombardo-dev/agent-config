#!/usr/bin/env python3
"""Append one validated SSLG invocation metric from stdin."""

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


SCHEMA_VERSION = 2
DEFAULT_ROOT = Path.home() / ".codex" / "subagent-metrics" / "scale-sol-luna-goals"
PAYLOAD_FIELDS = {
    "use_started": {"type", "goal_id", "objective", "start_fingerprint"},
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
GENERATED_FIELDS = {
    "schema_version",
    "created_at",
    "repository_id",
    "skill_use_id",
    "started_at",
    "completed_at",
    "elapsed_ms",
    "timing_status",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_time(value: datetime) -> str:
    return value.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def parse_time(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        fail(f"{field} must be an RFC 3339 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        fail(f"{field} must be an RFC 3339 timestamp: {error}")
    if parsed.tzinfo is None:
        fail(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


def require_non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value


def require_one_line_string(value: Any, field: str) -> str:
    result = require_non_empty_string(value, field)
    if "\n" in result or "\r" in result:
        fail(f"{field} must be one line")
    return result


def validate_failed_criteria(value: Any) -> list[str]:
    if not isinstance(value, list):
        fail("failed_criteria must be an array of unique non-empty strings")
    result: list[str] = []
    for item in value:
        result.append(require_non_empty_string(item, "failed_criteria item"))
    if len(result) != len(set(result)):
        fail("failed_criteria must not contain duplicates")
    return result


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    record_type = payload.get("type")
    if record_type not in PAYLOAD_FIELDS:
        fail(f"unsupported metric type: {record_type!r}")

    forbidden = GENERATED_FIELDS.intersection(payload)
    if forbidden:
        fail(f"the append helper owns these fields: {', '.join(sorted(forbidden))}")

    expected = PAYLOAD_FIELDS[record_type]
    missing = expected.difference(payload)
    unknown = set(payload).difference(expected)
    if missing:
        fail(f"{record_type} is missing fields: {', '.join(sorted(missing))}")
    if unknown:
        fail(f"{record_type} has unknown fields: {', '.join(sorted(unknown))}")

    if record_type == "use_started":
        goal_id = require_non_empty_string(payload["goal_id"], "goal_id")
        try:
            payload["goal_id"] = canonical_record_id(goal_id, "goal_id")
        except ValueError as error:
            fail(str(error))
        require_one_line_string(payload["objective"], "objective")
        require_non_empty_string(payload["start_fingerprint"], "start_fingerprint")
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
    measured_tokens = isinstance(tokens, int) and not isinstance(tokens, bool) and tokens >= 0
    if measurement == "runtime" and not measured_tokens:
        fail("runtime token measurement requires a non-negative integer total_goal_tokens")
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


def validate_log_state(
    records: list[dict[str, Any]],
    repository_id: str,
    skill_use_id: str,
) -> None:
    expected_types = ["use_started", "use_outcome"]
    if len(records) > len(expected_types):
        fail("metrics log already contains more than two records")
    for index, record in enumerate(records):
        if record.get("schema_version") != SCHEMA_VERSION:
            fail("existing metrics log uses an unsupported schema version")
        if record.get("repository_id") != repository_id:
            fail("existing metrics log has a different repository_id")
        if record.get("skill_use_id") != skill_use_id:
            fail("existing metrics log has a different skill_use_id")
        if record.get("type") != expected_types[index]:
            fail("existing metrics log is out of order")


def add_timing(
    payload: dict[str, Any],
    records: list[dict[str, Any]],
    now: datetime,
) -> None:
    if payload["type"] == "use_started":
        if records:
            fail("use_started already exists for this skill_use_id")
        payload["started_at"] = format_time(now)
        return

    if not records:
        fail("use_outcome requires an existing use_started record")
    if len(records) != 1:
        fail("use_outcome already exists for this skill_use_id")
    started_at = parse_time(records[0].get("started_at"), "started_at")
    payload["completed_at"] = format_time(now)
    payload["elapsed_ms"] = max(0, round((now - started_at).total_seconds() * 1000))
    payload["timing_status"] = "measured"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one validated SSLG invocation metric from stdin."
    )
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
    payload = read_payload()

    record_path = args.root.expanduser() / repository_id / f"{skill_use_id}.jsonl"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    now = utc_now()

    with record_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        records = load_records(handle)
        validate_log_state(records, repository_id, skill_use_id)
        add_timing(payload, records, now)
        record = {
            "schema_version": SCHEMA_VERSION,
            **payload,
            "created_at": format_time(now),
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
