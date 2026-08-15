# Outcome metrics

Record exactly two events for each SSLG invocation in one append-only JSONL file:

```text
~/.codex/subagent-metrics/scale-sol-luna-goals/<repository-id>/<skill-use-id>.jsonl
```

Use [`append_metric.py`](../scripts/append_metric.py) for both writes. The helper validates the
payload, adds the canonical envelope, records timestamps, calculates whole-invocation elapsed time,
locks the file, and rejects duplicate or out-of-order records. Do not write the log directly.

If persistence fails, continue the goal and report the gap. Never reconstruct time or token counts
from model recollection, file modification times, or partial worker records.

## Start

Resolve `repository_id` once with [`repository_id.py`](../scripts/repository_id.py). Reuse the same
lowercase `host/owner/repository` value and `skill_use_id` for both records.

Append `use_started` before dispatching work:

```sh
printf '%s\n' '{
  "type":"use_started",
  "goal_id":"goal-1",
  "objective":"Implement the accepted Agent Mail Phase 1 plan.",
  "start_fingerprint":"commit and relevant dirty state"
}' | python3 /absolute/path/to/append_metric.py \
  --repository-id host/owner/repository \
  --skill-use-id use-1
```

The helper adds `schema_version`, `created_at`, `repository_id`, `skill_use_id`, and `started_at`.

## Outcome

Append one `use_outcome` when the invocation reaches its terminal state:

```sh
printf '%s\n' '{
  "type":"use_outcome",
  "status":"success",
  "result":"Implemented and verified the Agent Mail Phase 1 plan.",
  "failed_criteria":[],
  "end_fingerprint":"verified commit and relevant dirty state",
  "total_goal_tokens":12345,
  "token_measurement":"runtime"
}' | python3 /absolute/path/to/append_metric.py \
  --repository-id host/owner/repository \
  --skill-use-id use-1
```

Use these values:

- `objective`: one line stating what the orchestrator was tasked to do.
- `status`: `success`, `failure`, or `blocked`.
- `result`: one line stating what the orchestrator actually did.
- `failed_criteria`: stable acceptance-check IDs. It must be empty for `success` and non-empty for
  `failure`.
- `end_fingerprint`: the terminal commit and relevant dirty state.
- `total_goal_tokens`: the directly measured total for the main task and all subagents, or `null`.
- `token_measurement`: `runtime` when the total is measured, otherwise `unavailable`.

The helper adds `completed_at`, `elapsed_ms`, and `timing_status`. It rejects caller-supplied
timing, negative token counts, inconsistent token fields, unknown fields, missing starts, and
duplicate outcomes.

Do not record assignment outcomes, checkpoints, subagent durations, token-category breakdowns,
review events, comparison cohorts, or qualitative observations. A controlled comparison belongs to
an external harness that measures SSLG and its control arm under the same rules.

## Final summary

Run [`summarize_metrics.py`](../scripts/summarize_metrics.py) after `use_outcome` and report the
available status, whole-goal elapsed time, and total goal tokens. Treat `null` as unavailable. Do
not estimate it.

```sh
python3 /absolute/path/to/summarize_metrics.py \
  --repository-id host/owner/repository \
  --skill-use-id use-1
```
