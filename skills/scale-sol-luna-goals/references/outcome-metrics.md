# Outcome metrics

Record one append-only JSONL journal for each SSLG invocation:

```text
~/.codex/subagent-metrics/scale-sol-luna-goals/<repository-id>/<skill-use-id>.jsonl
```

Use [`append_metric.py`](../scripts/append_metric.py) for every append. The helper validates the
payload, adds the canonical envelope and `created_at`, locks the journal, and appends one new line.
It never modifies an existing line or calculates per-subagent duration.

If persistence fails, continue the goal and report the gap. Never reconstruct records, timing, or
token counts from model recollection, file modification times, or partial worker reports.

## Invocation pair

Resolve `repository_id` once with [`repository_id.py`](../scripts/repository_id.py). Reuse the same
lowercase `host/owner/repository` value and `skill_use_id` for every record.

Append `use_started` before any work or dispatch:

```json
{
  "type": "use_started",
  "goal_id": "goal-1",
  "objective": "Implement the accepted Agent Mail Phase 1 plan.",
  "start_fingerprint": "commit and relevant dirty state"
}
```

Append `use_outcome` after every subagent has a terminal record:

```json
{
  "type": "use_outcome",
  "status": "success",
  "result": "Implemented and verified the Agent Mail Phase 1 plan.",
  "failed_criteria": [],
  "end_fingerprint": "verified commit and relevant dirty state",
  "total_goal_tokens": 12345,
  "token_measurement": "runtime"
}
```

Use `success`, `failure`, or `blocked`. A successful result has no failed criteria; a failure names
at least one stable acceptance-check ID. Record a directly measured whole-goal token total when the
runtime supplies it. Otherwise use `total_goal_tokens: null` and `token_measurement: unavailable`.
Do not estimate.

The runtime owns whole-goal elapsed time. Report its terminal goal telemetry to the user, but do not
derive or persist elapsed time through this journal.

## Subagent pair

Append `subagent_started` immediately before every subagent dispatch:

```json
{
  "type": "subagent_started",
  "assignment_id": "implementation-1",
  "parent_assignment_id": null,
  "role": "luna_worker",
  "requested_model": null,
  "requested_reasoning_effort": "medium",
  "objective": "Implement the bounded storage migration and run its focused tests."
}
```

Append `subagent_outcome` when that dispatch reaches a terminal state:

```json
{
  "type": "subagent_outcome",
  "assignment_id": "implementation-1",
  "outcome": "completed",
  "result": "Implemented the migration and passed the focused storage tests."
}
```

Every start and outcome receives its own generated `created_at`. `objective` and `result` are
required, non-empty, single-line descriptions. Use requested runtime settings in the start record;
use `null` when a model or effort was not requested explicitly.

Allowed outcomes are `completed`, `useful-no-go`, `failed`, `blocked`, `cancelled`, `interrupted`,
and `superseded`. Record null, negative, ambiguous, and unavailable results through the applicable
outcome and concrete result text instead of omitting the dispatch.

For a nested dispatch, set `parent_assignment_id` to the dispatching agent's `assignment_id`. Give
that agent the journal identity and helper path. The agent that dispatches the child owns the
child's pair and may append only those observational records. It must not edit prior records or
write invocation outcomes.

Before appending `use_outcome`, add terminal records for every started subagent. Use `interrupted`,
`cancelled`, `blocked`, or `failed` when a dispatch did not complete normally. The helper rejects
duplicate starts, duplicate outcomes, outcomes without starts, missing parents, records after the
invocation outcome, and terminal invocation outcomes with unfinished subagents.

## Append command

Pass one payload on standard input:

```sh
printf '%s\n' "$payload" | python3 /absolute/path/to/append_metric.py \
  --repository-id host/owner/repository \
  --skill-use-id use-1
```

The helper generates `schema_version`, `created_at`, `repository_id`, and `skill_use_id`. Do not
supply those envelope fields or the obsolete timing fields `started_at`, `completed_at`,
`elapsed_ms`, and `timing_status`. Do not record prompts, reasoning traces, per-subagent duration,
per-subagent token estimates, routine tool calls, review events, or comparison cohorts.

## Final summary

After `use_outcome`, run [`summarize_metrics.py`](../scripts/summarize_metrics.py). Report the
invocation status, whole-goal token total when available, subagent count, outcome counts, and any
unfinished assignment IDs. The summary must not calculate durations.

```sh
python3 /absolute/path/to/summarize_metrics.py \
  --repository-id host/owner/repository \
  --skill-use-id use-1
```
