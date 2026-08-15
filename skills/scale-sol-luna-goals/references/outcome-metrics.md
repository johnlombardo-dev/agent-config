# Outcome metrics

Read this reference and record events every time the skill is invoked. One append-only JSONL file is the canonical durable record for the invocation, including metrics, review findings, proposed contracts, decisions, and results:

```text
~/.codex/subagent-metrics/scale-sol-luna-goals/<repository-id>/<skill-use-id>.jsonl
```

Use [`append_metric.py`](../scripts/append_metric.py) for every append. Do not create or write a separate `~/.codex/subagent-contracts` tree. Existing files there are legacy evidence, not a current write target. Session state may buffer writes temporarily but is not the durable record. If persistence fails, continue the goal, report the gap, and backfill only facts that remain directly measurable.

This reference owns the required observation records, review timing records, routine summary, and controlled-comparison schema only. It does not change dispatch validity, precedence, verification requirements, or completion criteria in the parent `SKILL.md`.

## Contents

- [Canonical JSONL envelope](#canonical-jsonl-envelope)
- [Repository identity](#repository-identity)
- [Skill-use records](#skill-use-records)
- [Review timing](#review-timing)
- [Routine analysis](#routine-analysis)
- [Controlled comparison protocol](#controlled-comparison-protocol)

## Canonical JSONL envelope

Write each line as one JSON object. Include these fields on every new record:

```json
{
  "schema_version": 1,
  "type": "stable_snake_case_record_type",
  "created_at": "2026-08-14T12:34:56.789Z",
  "repository_id": "host/owner/repository",
  "skill_use_id": "unique invocation ID"
}
```

Pass one JSON object without envelope or generated timing fields on standard input:

```sh
metric_writer="/absolute/path/to/scale-sol-luna-goals/scripts/append_metric.py"
printf '%s\n' '{"type":"use_checkpoint","status":"active","unresolved_required_work":[]}' | \
  python3 "$metric_writer" \
    --repository-id host/owner/repository \
    --skill-use-id ID
```

The helper adds `schema_version`, `created_at`, `repository_id`, and `skill_use_id` immediately before appending. It adds start timestamps to start events and calculates finish timestamps and elapsed milliseconds from their persisted start events. Contract writers invoke it with `--role writer`; the default `orchestrator` role writes all other event types. The helper rejects event types outside the selected role. Do not write the log directly or supply generated fields yourself. If the helper cannot obtain a reliable clock or append the record, report the persistence gap instead of inventing values.

Use the exact field names and record types in this reference. Do not substitute camel case, `record`, `record_type`, or prose-only entries. Never infer or backfill timestamps from file modification times, neighboring records, model recollection, or elapsed-time estimates. Treat older records without the canonical envelope as legacy observations with unavailable event timing.

## Repository identity

Resolve the identifier once before the first record:

```sh
repository_id_resolver="/absolute/path/to/scale-sol-luna-goals/scripts/repository_id.py"
repository_id="$(python3 "$repository_id_resolver" --repository-root /absolute/repository/root)"
```

A hosted `repository_id` has exactly three lowercase slash-separated segments:

```text
<dns-host>/<owner>/<repository>
```

For example, `git@github.com:programbo/picodash.git` and `https://github.com/programbo/picodash.git` both resolve to `github.com/programbo/picodash`. Omit the transport, user, port, leading slash, trailing slash, and `.git` suffix. Never flatten the segments with hyphens or underscores.

When the selected remote does not exist, the resolver emits:

```text
local/<repository-name>/<12-character-sha256-prefix-of-absolute-git-common-dir>
```

Every persistence helper validates this format. Resolve it once and reuse the returned string unchanged for metrics, goal state, artifacts, continuations, and review events.

`goal_id` and `skill_use_id` are single lowercase path-safe segments containing only letters, digits, dots, underscores, and hyphens. UUIDs satisfy this rule. They never contain slashes or transport syntax.

## Skill-use records

At invocation, append `use_started` before dispatching work:

```json
{
  "schema_version": 1,
  "type": "use_started",
  "created_at": "RFC3339 UTC",
  "repository_id": "host/owner/repository",
  "skill_use_id": "ID",
  "goal_id": "goal or continuation ID",
  "continuation_of": null,
  "start_fingerprint": "current state fingerprint",
  "completion_criteria": ["criterion"],
  "started_at": "RFC3339 UTC"
}
```

Append one `assignment_outcome` for every accepted, rejected, or stopped assignment:

```json
{
  "schema_version": 1,
  "type": "assignment_outcome",
  "created_at": "RFC3339 UTC",
  "repository_id": "host/owner/repository",
  "skill_use_id": "ID",
  "assignment_id": "ID",
  "phase": "research|shaping|implementation|verification",
  "state_fingerprint": "relevant state",
  "outcome": "landed|completed-no-change|useful-no-go|failed|aborted|superseded",
  "evidence": ["artifact, check, commit, or decision pointer"],
  "rework": null
}
```

At each review checkpoint, append `use_checkpoint`. Before ending the invocation, append `use_outcome`. Include:

- `status`: `active`, `goal-verified`, `user-changed-goal`, `requires-new-authority`, `capability-unavailable`, or `ended-with-required-work`.
- `unresolved_required_work`: an explicit array, including an empty array when none remains.
- `observations`: prerequisite, `NO-GO`, and stop adjudications; contract-caused rework; reopened accepted decisions; writer retention and reuse; evidence revalidation or invalidation.
- `telemetry`: directly measured elapsed time and input, cached-input, reasoning, and output tokens. Use explicit `null` values for unavailable measurements.
- `completed_at` on `use_outcome`, using the same timestamp rules as `created_at`.

Record explicit `none`, `ambiguous`, or `unavailable` values rather than omitting an eligible observation. Link continuation invocations to the same goal while giving each invocation its own `skill_use_id`.

## Review timing

An append timestamp alone cannot measure duration. Persist start and finish events around each review cycle and each canonical review step.

Use these step names:

- `prepare`: resolve and fingerprint the exact review target.
- `wait_for_hosted_review`: wait for the configured hosted reviewer. Use only when applicable.
- `review_and_shape`: collect findings, normalize them, propose dispositions, and shape contracts.
- `fix_and_integrate`: execute accepted review contracts and integrate their results. Use only when findings require changes.
- `verify`: run the required checks and determine the cycle outcome.

Before a cycle begins, append `review_cycle_started`. Before each step begins, append `review_step_started`. Append `review_step_finished` immediately after that step ends, including failures and interruptions. Use one stable `cycle_id` and `step_id` to correlate the events. The helper looks up the corresponding start event and adds `started_at`, `completed_at`, `elapsed_ms`, and `timing_status` to finish records.

```json
{
  "schema_version": 1,
  "type": "review_step_finished",
  "created_at": "RFC3339 UTC",
  "repository_id": "host/owner/repository",
  "skill_use_id": "ID",
  "cycle_id": "local-1",
  "step_id": "local-1-review-and-shape-1",
  "stage": "local|hosted-pr",
  "step": "prepare|wait_for_hosted_review|review_and_shape|fix_and_integrate|verify",
  "attempt": 1,
  "started_at": "RFC3339 UTC",
  "completed_at": "RFC3339 UTC",
  "elapsed_ms": 1234,
  "timing_status": "measured",
  "outcome": "completed|completed-no-change|failed|blocked|superseded",
  "evidence": ["artifact or check pointer"]
}
```

Give `review_cycle_started` the cycle ID, stage, review source, exact base and head, and `started_at`. Give `review_step_started` the cycle ID, step ID, stage, step, attempt, and `started_at`.

At the end of every local or hosted cycle, append `review_cycle_outcome` with:

- the cycle ID, stage, review source, exact base and head;
- `started_at`, `completed_at`, `elapsed_ms`, and `timing_status`;
- P0, P1, P2, and P3 finding counts;
- accepted, rejected, duplicate, and ambiguous finding counts;
- original, fix-induced, and ambiguous attribution counts;
- proposed, accepted, rejected, completed, superseded, and dependency-blocked contract counts;
- stack and manifest pointers;
- `outcome`: `clean`, `findings`, `stale`, or `blocked`;
- unresolved finding IDs, required-check result, and resulting head.

Capture timestamps before doing the work. Do not reconstruct a step start from its finish event. The helper rejects finish records without a matching persisted start. If measurement fails, preserve any start event, report the gap, and treat the duration as unavailable. Do not bypass the helper with guessed or null timing fields.

Keep the skill-use outcome active while the selected delivery mode has an unfinished gate. A locally clean cycle, draft-to-ready transition, green intermediate CI run, or completed fix batch is not default `goal-verified`. For default delivery, record `goal-verified` only after the exact locally and remotely clean head passes required CI, has zero unresolved review threads, and is merged. For no-PR mode, require the current clean local gate. For no-merge mode, require both clean gates and green required CI, but not merge. Record a capability or authority blocker with the corresponding non-complete outcome.

After resolving the canonical remote, store its repository ID exactly as `host/owner/repository` in `use_started` and reuse that path and value for every continuation. Do not create separator variants for the same repository.

## Routine analysis

Run [`summarize_metrics.py`](../scripts/summarize_metrics.py) at each review checkpoint and before the final response. Do not wait for a separate user request. Report the measured review-step and cycle totals concisely, including unfinished steps and unavailable timing.

```sh
metrics_reader="/absolute/path/to/scale-sol-luna-goals/scripts/summarize_metrics.py"
python3 "$metrics_reader" \
  --repository-id host/owner/repository \
  --skill-use-id ID
```

Compare measured elapsed time by review step, review stage, phase, and outcome. Keep hosted-review wait time separate from active review and repair work. Report useful prerequisite or `NO-GO` work separately from failed or abandoned work.

Always retain enough structured observations to assess:

- whole-goal completion and unresolved required work;
- confirmed and rejected `PREREQUISITE`, `NO-GO`, and worker stops;
- discoverable prerequisites missed before implementation;
- rework caused by contract omission, implementation deviation, new evidence, environment, or external change;
- accepted public decisions reopened during implementation;
- writers retained, reused, retired unused, or retired after drift;
- evidence repeated, revalidated, invalidated, or opened in full by the parent;
- review corrections and repeated checks without state change; and
- elapsed time and token classes only when directly measured.

Do not sum overlapping worker durations and call the result wall-clock time. Use the review-step interval for wall-clock analysis and worker telemetry for compute or token analysis.

## Controlled comparison protocol

When the goal itself is a controlled comparison, append `comparison_started` before examining outcomes. Include the common envelope plus the comparison ID, hypothesis and falsifying observation, comparable task stratum or baseline, adjudicator, and observation window. This adds cohort discipline to routine metrics. It does not gate routine capture, analysis, or reporting.

Include every eligible assignment in the declared cohort, including null, negative, ambiguous, and unavailable results. Preserve measured telemetry separately from retrospective interpretation. Record:

- the denominator for each confirmed or rejected prerequisite, `NO-GO`, and stop;
- primary and contributing rework causes; and
- the declared baseline or task stratum for every included result.

Do not infer causality from unmatched tasks or treat model agreement as correctness. Use the observations to challenge existing guidance and form hypotheses, not retroactively justify current rules or create automatic routing policy.
