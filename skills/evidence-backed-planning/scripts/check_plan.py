#!/usr/bin/env python3
"""Validate the structural requirements of an evidence-backed plan."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_HEADINGS = (
    "## Evidence baseline",
    "## Scope",
    "## Behavioral-seam manifest",
    "## Planning-shield applicability",
    "## Non-negotiable invariants",
    "## Architecture decisions",
    "## Risk and finding traceability",
    "## Delivery slices",
    "## Acceptance matrices",
    "## Evidence tiers and promotion",
    "## Explicit gaps and deferred work",
)

REQUIRED_EVIDENCE_TIERS = (
    "static",
    "isolated",
    "composed",
    "capacity",
    "live",
    "security",
    "operations",
    "documentation",
    "delivery",
)

EXPECTED_SHIELDS = {f"S{number:02d}" for number in range(1, 13)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("evidence", nargs="*", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = [args.plan, *args.evidence]
    errors: list[str] = []

    for path in paths:
        if not path.is_file():
            errors.append(f"missing file: {path}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    plan = args.plan.read_text(encoding="utf-8")
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    lowered = combined.casefold()

    for heading in REQUIRED_HEADINGS:
        if heading not in plan:
            errors.append(f"plan is missing heading: {heading}")

    actual_shields = set(re.findall(r"\bS(?:0[1-9]|1[0-2])\b", combined))
    missing_shields = sorted(EXPECTED_SHIELDS - actual_shields)
    if missing_shields:
        errors.append("planning-shield ledger is missing: " + ", ".join(missing_shields))

    for shield in sorted(EXPECTED_SHIELDS):
        pattern = rf"\|\s*{shield}\s*\|\s*(required|not applicable|gap)\s*\|"
        if not re.search(pattern, combined, flags=re.IGNORECASE):
            errors.append(f"{shield} lacks a routed status: required, not applicable, or gap")

    for tier in REQUIRED_EVIDENCE_TIERS:
        if tier not in lowered:
            errors.append(f"planning pack is missing evidence tier: {tier}")

    required_table_terms = (
        "supports",
        "limits",
        "rejected alternative",
        "faithful proof",
        "owner",
        "status",
    )
    for term in required_table_terms:
        if term not in lowered:
            errors.append(f"planning pack is missing traceability term: {term}")

    if re.search(r"\b(?:TODO|TBD|PLACEHOLDER)\b", plan, flags=re.IGNORECASE):
        errors.append("plan contains unresolved planning markers")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: plan contains the evidence, routing, traceability, and promotion structure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
