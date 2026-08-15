---
name: evidence-first-review
description: >-
  Review a code change or existing system by mapping its behavioral seams,
  running four focused defect-finding lanes, and requiring executable evidence
  where the risk can be exercised. Use for code review, regression hunts,
  pre-merge audits, large integrated changes, or system-wide bug hunts when a
  broad diff reading is likely to miss value, accessibility, public API, or
  lifecycle failures.
---

# Evidence-first review

Find and batch demonstrated defects before anyone starts repairing them.

## Set the target

Choose one mode and record it in the result.

- **Change mode:** review the exact diff, its changed behavior, and adjacent consumers. Classify findings as introduced, pre-existing, fix-induced, or unknown.
- **System mode:** review a named behavior or subsystem without limiting findings to one diff. Do not describe a defect as introduced unless history proves it.

Freeze the target fingerprint, repository instructions, allowed tools, time or token budget, and checks that may run. Treat dirty state as part of the target. Review read-only. Do not implement fixes, change Git or PR state, or write metrics.

## Map the seams

Before reading line by line, list the boundaries where behavior can disagree:

- canonical, draft, formatted, serialized, and external values;
- direct controls, composed wrappers, portals, focus targets, and input methods;
- public types, runtime guards, exports, packages, and server or browser entrypoints;
- refs, observers, subscriptions, effects, timers, hidden state, hydration, and cleanup;
- modes, events, guards, effects, retries, cancellation, and interacting processes that form an informal state machine.

Use this map to select evidence. Do not spend equal effort on every file.

## Run four independent lanes

Run all applicable lanes independently. Parallel execution is useful when fresh reviewers and a shared target are available. Do not pass one lane's conclusions into another before they return.

1. **Value integrity:** lossless formatting, round trips, canonical versus draft values, atomic writes, unavailable choices, invalid numbers, and silent normalization.
2. **Accessibility and interaction:** names, descriptions, errors, keyboard and pointer behavior, focus return, disabled and read-only behavior, portals, coarse pointers, forced colors, and RTL.
3. **Public contract:** generic inference, runtime configuration guards, exact props, exports, package isolation, SSR, and direct versus composed behavior.
4. **Lifecycle and rendering:** refs, observers, subscriptions, hidden-state cleanup, hydration, resizing, streaming buffers, realms, and rendering-library behavior.

Read [evidence-techniques.md](references/evidence-techniques.md) after the seam map. Pick the cheapest faithful methods for the identified risks. A passing broad suite is context, not proof of an uncovered interaction.

## Keep only demonstrated findings

Keep a finding only when it has all of these:

- a violated invariant or user-visible failure;
- a minimal reproduction, executable probe, or direct source proof;
- a narrow location and affected behavior;
- a severity and provenance classification;
- enough evidence that an implementer can verify the repair.

Do not repair while lanes are active. Deduplicate after every lane returns, then publish one batch.

## Report

Return:

```text
TARGET: mode, fingerprint, budget, checks run
SEAMS: reviewed boundaries
FINDINGS: severity, provenance, invariant, reproduction, location, evidence
GAPS: seams not exercised and why
RESULT: findings | no confirmed findings
```

Write `no confirmed findings`, never `clean` or `proved correct`. Stop after this batch. A later repair belongs to `verify-repair-seam`, not another whole-target pass.

This skill does not own implementation, repair scheduling, Git delivery, hosted review, merge decisions, or persistence.
