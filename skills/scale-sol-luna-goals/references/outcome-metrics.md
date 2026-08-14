# Outcome metrics

Read this reference and record metrics every time the skill is invoked. Persist each invocation incrementally as JSONL under `~/.codex/subagent-metrics/scale-sol-luna-goals/<repository-id>/<skill-use-id>.jsonl`; prefer the canonical remote host/owner/repository for `repository-id`, with a stable local identifier as fallback. Session state may buffer writes temporarily but is not the durable record. If persistence fails, continue the goal, report the gap, and backfill when possible.

This reference owns the required observation record and optional named-evaluation schema only. It does not change dispatch validity, precedence, verification requirements, or completion criteria in the parent `SKILL.md`.

At invocation, write:

```text
USE: ID; goal or continuation ID; start fingerprint; completion criteria; start time if reliably available
```

Append one compact entry per accepted, rejected, or stopped assignment:

```text
<id> | <research|shaping|implementation|verification> | <state fingerprint>
Outcome: <landed|completed-no-change|useful-no-go|failed|aborted|superseded>
Evidence: <artifact, check, commit, or decision pointer>
Rework: <none or concise cause>
```

At each review checkpoint and before ending the invocation, append:

```text
USE OUTCOME: active|goal-verified|user-changed-goal|requires-new-authority|capability-unavailable|ended-with-required-work; unresolved required work
OBSERVATIONS: prerequisite/NO-GO/stop adjudications; contract-caused rework; reopened accepted decisions; writer retention/reuse; evidence revalidation/invalidation
TELEMETRY: elapsed time and input/cached-input/reasoning/output tokens when directly measured; never estimate unavailable fields
```

Record explicit `none`, `ambiguous`, or `unavailable` values rather than omitting an eligible observation. Link continuation invocations to the same goal while giving each invocation its own `USE` ID.

Compare tokens and elapsed time by phase and outcome. Report useful prerequisite or `NO-GO` work separately from failed or abandoned work. Useful secondary measures include review corrections, repeated checks without state change, context-pack size, files or tests produced, and commits landed.

For every local or hosted review cycle append:

```text
REVIEW CYCLE: ID; local|hosted-pr; review source; exact base/head; start/end time when available
FINDINGS: P0/P1/P2/P3 counts; accepted/rejected/duplicate/ambiguous; original/fix-induced/ambiguous attribution
CONTRACTS: proposed/accepted/rejected/completed/superseded; dependency-blocked count; stack and manifest pointers
CYCLE OUTCOME: clean|findings|stale|blocked; unresolved findings; required-check result; resulting head
```

Keep the skill-use outcome active while the selected delivery mode has an unfinished gate. A locally clean cycle, draft-to-ready transition, green intermediate CI run, or completed fix batch is not default `goal-verified`. For default delivery, record `goal-verified` only after the exact locally and remotely clean head passes required CI, has zero unresolved review threads, and is merged. For no-PR mode, require the current clean local gate. For no-merge mode, require both clean gates and green required CI, but not merge. Record a capability or authority blocker with the corresponding non-complete outcome.

After resolving the canonical remote, store its repository ID exactly as `host/owner/repository` in the `USE` entry and reuse that path for every continuation. Do not create separator variants for the same repository.

## Named evaluation protocol

In addition to the required observation record, use this protocol for an explicitly named evaluation goal. Before examining outcomes, record:

```text
EVALUATION: ID; hypothesis and falsifying observation; comparable task stratum or baseline; adjudicator; observation window
```

Include every eligible assignment in the declared cohort, including null, negative, ambiguous, and unavailable results. Preserve measured telemetry separately from retrospective interpretation. Record:

- whole-goal completion and unresolved required work;
- confirmed and rejected `PREREQUISITE`, `NO-GO`, and worker stops, each with its denominator;
- pre-existing, reasonably discoverable prerequisites missed among tasks that entered implementation;
- rework caused by contract contradiction or omission, implementation deviation, new evidence, environmental failure, or external change, allowing primary and contributing causes;
- accepted public decisions reopened during implementation and the observed cause;
- writers retained, actually reused, retired unused, or retired after drift;
- selected evidence repeated, revalidated, invalidated, or opened in full by the parent; and
- elapsed time and token classes only when directly measured.

Do not infer causality from unmatched tasks or treat model agreement as correctness. Use the observations to challenge existing guidance and form hypotheses, not retroactively justify current rules or create automatic routing policy.
