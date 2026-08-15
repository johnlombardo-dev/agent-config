#!/usr/bin/env python3
"""Atomically write the current scale-sol-luna-goals snapshot from stdin."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from path_conventions import canonical_record_id, canonical_repository_id


SCHEMA_VERSION = 1
DEFAULT_ROOT = Path.home() / ".codex" / "subagent-state" / "scale-sol-luna-goals"
REQUIRED_FIELDS = {"goal", "state", "decisions", "active", "next", "blockers", "metrics"}
GENERATED_FIELDS = {
    "schema_version",
    "updated_at",
    "repository_id",
    "goal_id",
    "skill_use_id",
}
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")


def fail(message: str) -> None:
    raise SystemExit(message)


def read_payload() -> dict[str, Any]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        fail(f"stdin must contain one JSON object: {error}")
    if not isinstance(payload, dict):
        fail("stdin must contain one JSON object")
    forbidden = GENERATED_FIELDS.intersection(payload)
    if forbidden:
        fail(f"the state helper owns these fields: {', '.join(sorted(forbidden))}")
    missing = REQUIRED_FIELDS.difference(payload)
    if missing:
        fail(f"goal state is missing: {', '.join(sorted(missing))}")
    extra = set(payload).difference(REQUIRED_FIELDS)
    if extra:
        fail(f"goal state has unsupported fields: {', '.join(sorted(extra))}")
    invalid_keys = [key for key in payload if not SNAKE_CASE.fullmatch(key)]
    if invalid_keys:
        fail(f"top-level fields must use snake_case: {', '.join(sorted(invalid_keys))}")
    for field in ("decisions", "active", "next", "blockers"):
        if not isinstance(payload[field], list):
            fail(f"{field} must be an array")
    if not isinstance(payload["metrics"], dict):
        fail("metrics must be an object")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Atomically write the current scale-sol-luna-goals snapshot from stdin."
    )
    parser.add_argument("--repository-id", required=True)
    parser.add_argument("--goal-id", required=True)
    parser.add_argument("--skill-use-id", required=True)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        repository_id = canonical_repository_id(args.repository_id)
    except ValueError as error:
        fail(str(error))
    try:
        goal_id = canonical_record_id(args.goal_id, "goal_id")
        skill_use_id = canonical_record_id(args.skill_use_id, "skill_use_id")
    except ValueError as error:
        fail(str(error))
    payload = read_payload()

    state_path = args.root.expanduser() / repository_id / f"{goal_id}.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = state_path.with_suffix(".lock")
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        **payload,
        "updated_at": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
        "repository_id": repository_id,
        "goal_id": goal_id,
        "skill_use_id": skill_use_id,
    }
    serialized = json.dumps(snapshot, indent=2, sort_keys=True) + "\n"

    with lock_path.open("a", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=state_path.parent,
                prefix=f".{state_path.name}.",
                delete=False,
            ) as temporary:
                temporary.write(serialized)
                temporary.flush()
                os.fsync(temporary.fileno())
                temporary_path = Path(temporary.name)
            temporary_path.chmod(0o600)
            os.replace(temporary_path, state_path)
            directory_fd = os.open(state_path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    print(state_path)


if __name__ == "__main__":
    main()
