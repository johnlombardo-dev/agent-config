#!/usr/bin/env python3
"""Summarize measured scale-sol-luna-goals review timing as JSON."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from path_conventions import canonical_record_id, canonical_repository_id


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
            if isinstance(record, dict):
                records.append(record)
    return records


def interval_summary(values: list[int]) -> dict[str, int | float]:
    return {
        "count": len(values),
        "total_elapsed_ms": sum(values),
        "average_elapsed_ms": round(sum(values) / len(values), 2),
        "minimum_elapsed_ms": min(values),
        "maximum_elapsed_ms": max(values),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize measured scale-sol-luna-goals review timing as JSON."
    )
    parser.add_argument("--repository-id", required=True)
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
        skill_use_id = canonical_record_id(args.skill_use_id, "skill_use_id")
    except ValueError as error:
        fail(str(error))
    record_path = args.root.expanduser() / repository_id / f"{skill_use_id}.jsonl"
    records = load_records(record_path)

    step_values: dict[str, list[int]] = defaultdict(list)
    cycle_values: dict[str, list[int]] = defaultdict(list)
    started_steps: set[str] = set()
    finished_steps: set[str] = set()
    use_elapsed_ms: int | None = None

    for record in records:
        record_type = record.get("type")
        if record_type == "review_step_started" and isinstance(record.get("step_id"), str):
            started_steps.add(record["step_id"])
        elif record_type == "review_step_finished":
            step_id = record.get("step_id")
            if isinstance(step_id, str):
                finished_steps.add(step_id)
            elapsed_ms = record.get("elapsed_ms")
            if isinstance(elapsed_ms, int) and elapsed_ms >= 0:
                key = f"{record.get('stage', 'unknown')}/{record.get('step', 'unknown')}"
                step_values[key].append(elapsed_ms)
        elif record_type == "review_cycle_outcome":
            elapsed_ms = record.get("elapsed_ms")
            if isinstance(elapsed_ms, int) and elapsed_ms >= 0:
                cycle_values[str(record.get("stage", "unknown"))].append(elapsed_ms)
        elif record_type == "use_outcome":
            elapsed_ms = record.get("elapsed_ms")
            if isinstance(elapsed_ms, int) and elapsed_ms >= 0:
                use_elapsed_ms = elapsed_ms

    summary = {
        "repository_id": repository_id,
        "skill_use_id": skill_use_id,
        "record_count": len(records),
        "use_elapsed_ms": use_elapsed_ms,
        "review_steps": {
            key: interval_summary(values) for key, values in sorted(step_values.items())
        },
        "review_cycles": {
            key: interval_summary(values) for key, values in sorted(cycle_values.items())
        },
        "unfinished_step_ids": sorted(started_steps.difference(finished_steps)),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
