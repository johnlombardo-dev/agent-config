#!/usr/bin/env python3
"""Append one canonical scale-sol-luna-goals invocation event from stdin."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from path_conventions import canonical_record_id, canonical_repository_id


SCHEMA_VERSION = 1
DEFAULT_ROOT = Path.home() / ".codex" / "subagent-metrics" / "scale-sol-luna-goals"
ALLOWED_TYPES = {
    "assignment_outcome",
    "comparison_started",
    "review_contract_proposed",
    "review_contract_result",
    "review_cycle_outcome",
    "review_cycle_observed",
    "review_cycle_started",
    "review_decision",
    "review_finding",
    "review_step_finished",
    "review_step_started",
    "use_checkpoint",
    "use_outcome",
    "use_started",
}
WRITER_TYPES = {"review_contract_proposed", "review_cycle_observed", "review_finding"}
ORCHESTRATOR_TYPES = ALLOWED_TYPES.difference(WRITER_TYPES)
REVIEW_EVENT_TYPES = {
    "review_contract_proposed",
    "review_contract_result",
    "review_cycle_observed",
    "review_decision",
    "review_finding",
}
ENVELOPE_KEYS = {"schema_version", "created_at", "repository_id", "skill_use_id"}
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")


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


def read_payload(role: str) -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        fail(f"stdin must contain one JSON object: {error}")
    if not isinstance(payload, dict):
        fail("stdin must contain one JSON object")
    forbidden = ENVELOPE_KEYS.intersection(payload)
    if forbidden:
        fail(f"the append helper owns these fields: {', '.join(sorted(forbidden))}")
    invalid_keys = [key for key in payload if not SNAKE_CASE.fullmatch(key)]
    if invalid_keys:
        fail(f"top-level fields must use snake_case: {', '.join(sorted(invalid_keys))}")
    record_type = payload.get("type")
    permitted_types = WRITER_TYPES if role == "writer" else ORCHESTRATOR_TYPES
    if record_type not in permitted_types:
        fail(f"role {role!r} cannot append type {record_type!r}")
    if record_type in REVIEW_EVENT_TYPES:
        if payload.get("stage") not in {"local", "hosted-pr"}:
            fail(f"{record_type} requires stage local or hosted-pr")
    return payload


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
        if isinstance(record, dict):
            records.append(record)
    return records


def find_start(
    records: list[dict[str, Any]],
    start_type: str,
    identity: dict[str, Any],
) -> dict[str, Any]:
    for record in reversed(records):
        if record.get("type") != start_type:
            continue
        if all(record.get(key) == value for key, value in identity.items()):
            return record
    formatted = ", ".join(f"{key}={value!r}" for key, value in identity.items())
    fail(f"missing {start_type} record for {formatted}")


def add_timing(
    payload: dict[str, Any],
    records: list[dict[str, Any]],
    now: datetime,
) -> None:
    record_type = payload["type"]
    start_types = {
        "comparison_started",
        "review_cycle_started",
        "review_step_started",
        "use_started",
    }
    if record_type in start_types:
        if "started_at" in payload:
            fail("the append helper owns started_at for start events")
        payload["started_at"] = format_time(now)
        return

    start_type: str | None = None
    identity: dict[str, Any] = {}
    if record_type == "use_outcome":
        start_type = "use_started"
    elif record_type == "review_cycle_outcome":
        start_type = "review_cycle_started"
        identity = {"cycle_id": payload.get("cycle_id")}
    elif record_type == "review_step_finished":
        start_type = "review_step_started"
        identity = {
            "cycle_id": payload.get("cycle_id"),
            "step_id": payload.get("step_id"),
        }

    if start_type is None:
        return
    if any(value is None for value in identity.values()):
        fail(f"{record_type} is missing its correlation identifier")
    for field in ("started_at", "completed_at", "elapsed_ms", "timing_status"):
        if field in payload:
            fail(f"the append helper owns {field} for {record_type}")
    start = find_start(records, start_type, identity)
    started_at = parse_time(start.get("started_at"), "started_at")
    payload["started_at"] = format_time(started_at)
    payload["completed_at"] = format_time(now)
    payload["elapsed_ms"] = max(0, round((now - started_at).total_seconds() * 1000))
    payload["timing_status"] = "measured"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append one canonical scale-sol-luna-goals invocation event from stdin."
    )
    parser.add_argument("--repository-id", required=True)
    parser.add_argument("--skill-use-id", required=True)
    parser.add_argument("--role", choices=("orchestrator", "writer"), default="orchestrator")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        repository_id = canonical_repository_id(args.repository_id)
    except ValueError as error:
        fail(str(error))
    try:
        skill_use_id = canonical_record_id(args.skill_use_id, "skill_use_id")
    except ValueError as error:
        fail(str(error))
    payload = read_payload(args.role)

    record_path = args.root.expanduser() / repository_id / f"{skill_use_id}.jsonl"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    now = utc_now()

    with record_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        records = load_records(handle)
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
