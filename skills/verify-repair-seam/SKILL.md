---
name: verify-repair-seam
description: >-
  Verify one accepted bug repair without reopening the entire change for broad
  review. Use after a fix, review response, regression patch, or hosted finding
  when Codex must rerun the original reproduction, prove the repaired
  invariant, test adjacent counterexamples, and check for fix-induced failures
  only in the affected behavior and its direct consumers.
---

# Verify a repair seam

Prove that a specific repair closes its defect without moving the failure nearby.

## Freeze the claim

Record the accepted finding, original reproduction, promised invariant, changed files, direct consumers, and checks already run. If the repair changed a public contract or expanded the failure domain beyond the accepted finding, return `blocked` and ask for a new implementation decision.

Work read-only. Do not edit the repair, widen its scope, change Git or PR state, or run a whole-repository review.

## Verify in order

1. Rerun the original reproduction against the repair. A substitute test is not enough when the original path is still available.
2. Exercise the invariant at its owning boundary. Use the lowest public layer that can prove the claim.
3. Generate adjacent counterexamples from the seam. Vary the next value, state, input method, wrapper, lifecycle event, or failure path that could expose a displaced bug.
4. Inspect only the changed behavior, its direct callers, and shared code reached by the repair for fix-induced regressions.
5. Run the narrowest checks that execute those cases. Reuse unchanged evidence instead of rerunning broad gates.

Use browser evidence for focus, portals, geometry, pointer input, forced colors, and other rendered behavior. Use compile fixtures for public TypeScript claims. Use deterministic lifecycle controls for observers, subscriptions, timers, visibility, hydration, and cleanup.

## Return one outcome

```text
FINDING: accepted finding and repair fingerprint
ORIGINAL REPRODUCTION: passed | failed | unavailable
INVARIANT: evidence
COUNTEREXAMPLES: cases and results
FIX-INDUCED CHECK: affected code and result
CHECKS: commands or probes
GAPS: untested claims
RESULT: verified | failed | blocked
```

`verified` requires the original reproduction, invariant, and applicable counterexamples to pass. `failed` means the defect remains or the repair created a demonstrated regression. `blocked` means faithful evidence is unavailable or the repair changed the decision being verified.

Stop after this seam. Do not convert the result into another broad review cycle.
