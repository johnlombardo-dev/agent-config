---
name: scale-sol-luna-goals
description: >-
  Coordinate explicitly requested large goals through a persistent iterative
  roadmap while preserving main-thread context. Use when the user invokes
  $scale-sol-luna-goals or asks the orchestrator to delegate problem-space
  research and Luna-safe contract writing to capable Sol subagents, dispatch
  bounded Luna execution, integrate evidence, and continue across sub-goals
  until the whole goal is verified. By default, finish through proportionate
  verification, green required CI, and merge. Honor explicit no-PR, no-merge,
  and draft-PR constraints. The main orchestrator owns decisions, worker
  dispatch, integration, replanning, and completion.
---

# Scale Sol-Luna goals

## Normative ownership, terms, and precedence

This file is the sole normative source for role authority, the terms below, dispatch validity, rule precedence, and the canonical goal loop. The [task-packets reference](references/task-packets.md) owns only assignment schemas and Luna profile selection. The [runtime-routing reference](references/runtime-routing.md) owns only logical-to-runtime mappings and degraded-capability behavior. The [delivery reference](references/delivery.md) owns only Git, PR, CI, and merge mechanics. The [outcome-metrics reference](references/outcome-metrics.md) owns the append-only invocation and subagent record pairs plus the final summary. References must not redefine this file's semantics.

## Invocation contract

Once invoked, this skill runs the complete goal lifecycle without requiring separate requests for its normal functions:

- persist and maintain compact goal state;
- record one timestamped objective and terminal result for the invocation and every subagent dispatch;
- summarize whole-goal status and tokens plus subagent counts and outcomes at final signoff;
- retain and reuse one same-domain writer when the reuse rule applies;
- grant bounded depth-one research and external artifact scope when the dispatch rules require them;
- execute the selected delivery mode through its terminal state.

Task-state predicates such as Worth, Decision-ready, applicable delivery steps, and likely writer reuse decide whether work is necessary. They are not user opt-in gates. A reference may specify mechanics or narrow behavior for safety, authority, capability, or relevance. It must not require the user to ask again for a normal function listed above.

SSLG has exactly three current persistence locations, all keyed by the same canonical `repository_id`:

| Data | Canonical path | Shape |
| --- | --- | --- |
| Invocation events and metrics | `~/.codex/subagent-metrics/scale-sol-luna-goals/<repository-id>/<skill-use-id>.jsonl` | One append-only log per invocation |
| Current goal state | `~/.codex/subagent-state/scale-sol-luna-goals/<repository-id>/<goal-id>.json` | One atomically replaced snapshot per goal |
| Necessary long artifacts | `~/.codex/subagent-artifacts/scale-sol-luna-goals/<repository-id>/<skill-use-id>/` | Bounded files referenced by the log or snapshot |

No other path is a current SSLG write target. In particular, do not create or append to `~/.codex/subagent-contracts`; any existing content there is legacy evidence.

- **Worth:** A delegated route's expected context, time, or confidence gain exceeds its setup, verification, and integration cost.
- **Defined:** The question or outcome, authority, relevant state, and expected return are bounded.
- **Consequential Decision:** A choice that changes a public interface, ownership, security, data, migration, goal scope, or acceptance.
- **Decision-ready:** No unresolved Consequential Decision affects the proposed Luna task.
- **Failure Domain:** The state and behavior that could be affected or left inconsistent if work partially succeeds or fails.
- **Safe:** The outcome and its Failure Domain can be evaluated, accepted, rejected, and reverted together under one mutation owner.
- **Checkable:** The cheapest faithful check can observe the claimed result.

Apply orchestration rules as ordered filters:

1. Higher-level instructions, user authorization, and model policy define the permitted routes.
2. Current capability removes routes that cannot be used or verified as required.
3. Assignment validity requires Defined, Safe, and Checkable work; Luna work must also be Decision-ready.
4. Worth selects delegation or the fast path among the routes still permitted.
5. The task-packet profile governs contract detail.
6. Verification rules govern evidence depth and reuse.

Each layer constrains the next; a lower layer never relaxes a higher one. First make the assignment valid, then choose its route. Worth never cures invalidity: for example, Worth but uncheckable work must be redefined rather than dispatched. A required route that is unavailable or invalid remains pending instead of being silently substituted.

## Authority and invariants

Keep the main orchestrator authoritative and its active context compact.

Invoking this skill authorizes the normal Git and GitHub mutations needed to create a branch,
commit, push, open or update a pull request, mark the pull request ready, and merge it. Do not ask
for that authority again. Higher-level instructions and explicit user restrictions still take
precedence.

Apply these delivery modes. Equivalent wording has the same effect, and the most restrictive mode
wins:

| User request | Required delivery |
| --- | --- |
| No delivery restriction | Final verification, green required CI, then merge. |
| “Do not create a PR” | Final verification only; do not push, create a PR, or merge. |
| “Do not merge the PR” | Final verification and green required CI; leave the PR open and unmerged. |
| “Create a draft PR” | Keep the PR draft during final verification and CI; then mark it ready and merge unless merge is also forbidden. |

“Do not create a PR” overrides draft-PR and no-merge instructions. “Do not merge” overrides the
default merge after a draft delivery.

- The orchestrator owns the user goal, roadmap, Consequential Decisions, contract acceptance, implementation-worker dispatch, integration, and completion.
- Sol contract writers research and propose; they do not decide for the orchestrator, implement, integrate, or declare completion. An agent that dispatches a child may append only that child's `subagent_started` and `subagent_outcome` records to the orchestrator-provided journal.
- Luna executes one accepted task with frozen Consequential Decisions. It stops when success requires a decision or scope change and cannot dispatch another agent.
- Give every mutation surface one active owner. Parallel work must be independently acceptable and non-overlapping.
- Return distilled findings and evidence pointers, not raw research, logs, or reasoning traces.
- A handoff advances the goal loop; it never completes the larger goal by itself.

## Fast path and dispatch test

After assignment validity is established, choose the cheapest permitted route:

- Execute bounded work directly when ordinary instructions and model policy permit and coordination would cost more than implementation.
- When implementation should remain with Luna but research is unnecessary, let the orchestrator shape its task packet directly.
- Use Sol contract writers only when delegated research or shaping saves material main-context work, provides real parallelism, or adds valuable independent confidence.

Dispatch research or shaping only when it is Worth, Defined, Safe, and Checkable. Dispatch Luna only when those conditions hold and the task is Decision-ready.

If not Defined, frame it. If Luna work is not Decision-ready, research or decide. If not Safe, split it. If not Checkable, redefine the expected result. Only after validity is established, use the fast path when delegation is not Worth.

## Compact goal state

Resolve `repository_id` once at invocation with `scripts/repository_id.py` and reuse that exact value for every SSLG path and record. Keep a compact copy of goal state inline and persist its current snapshot outside repositories at `~/.codex/subagent-state/scale-sol-luna-goals/<repository-id>/<goal-id>.json`. Invoking this skill authorizes that bounded state file. Write it with `scripts/write_goal_state.py` before the first dispatch, after every integration or replan, at each framing checkpoint, and before ending the invocation. Do not ask for separate persistence authorization.

Keep persisted state bounded, redacted, safely discardable, reconstructible from current authorities, and non-authoritative. Treat missing, stale, corrupt, or partial state as a cache miss. Never put this coordination state in the user's repository.

```json
{
  "goal": {
    "summary": "goal",
    "completion_criteria": ["criterion"],
    "next_checkpoint": "checkpoint"
  },
  "state": {
    "fingerprint": "commit and relevant dirty state",
    "baseline": ["document, dependency, or check state"]
  },
  "decisions": ["accepted decision and evidence pointer"],
  "active": ["task, owner, and reserved mutation surface"],
  "next": ["one ready task and at most one provisional successor"],
  "blockers": ["decision, prerequisite, capability gap, or risk"],
  "metrics": {
    "skill_use_id": "ID",
    "record_path": "path"
  }
}
```

Replace superseded entries instead of appending history. Give each agent only relevant `KNOWN`, `VERIFY`, `UNKNOWN`, and `AVOID` facts. Require an evidence gap or changed state before repeating prior research.

## Reuse and retained writers

Treat agent output as candidate evidence, not authority. `KNOWN` means a current, source-backed fact admitted by the orchestrator; keep accepted Consequential Decisions separate. Prior conversation, persistence, or model identity never upgrades a claim.

While required work remains, retain at most one idle same-domain writer through the next framing checkpoint when its domain has a likely next research or shaping question. The orchestrator identifies that probable reuse without asking the user. Close the writer when no such use exists. Resume it only after the new assignment passes the validity and Worth filters. Treat every resumption as a new dispatch and provide the current question, authority, material state delta, stop conditions, and expected return. Carry no mutation right, accepted fact, decision, or runtime guarantee through retention.

Reuse only selected findings with authoritative evidence pointers, applicability, last-checked state, and invalidation triggers. Revalidate affected findings after material drift. If retained context is unreliable or its runtime cannot satisfy the new assignment's verified route, dispatch a fresh writer or keep the work pending.

Use an independent evidence check only when an incorrect reused finding could affect a Consequential Decision or several later assignments and the check is Worth. Treat it as a read-only Sol assignment. The checker may support, qualify, reject, or deduplicate candidate claims; only the orchestrator may admit findings into current task state or accept decisions.

## Canonical iterative goal loop

At invocation, read [references/outcome-metrics.md](references/outcome-metrics.md) and initialize its durable skill-use record with `scripts/append_metric.py` before dispatching work. Append `subagent_started` immediately before every dispatch and `subagent_outcome` when it terminates. Give a nested dispatcher the same journal identity and helper path so it records its child's pair. Use the helper for every append so it can enforce the schema and add `created_at` without modifying prior records. Never calculate or persist per-subagent duration. Metrics persistence is authorized by this skill and remains outside the repository and its worktrees.

Repeat this loop until the whole goal is verified:

1. **Frame.** Confirm the goal, completion criteria, state, accepted decisions, dependencies, and the next meaningful checkpoint.
2. **Research.** Select the smallest uncertainty that unlocks valuable work. Dispatch a Sol writer only when the dispatch test passes; otherwise research in the main thread. Stop early on a precise `NO-GO` or `PREREQUISITE`.
3. **Shape.** Resolve Consequential Decisions in the main thread and choose one dependency-ready outcome. Select its Luna profile from [references/task-packets.md](references/task-packets.md).
4. **Dispatch.** Recheck the task fingerprint; treat changed facts, decisions, ownership, constraints, or checks as material drift requiring re-adjudication. Reserve mutation ownership, verify the current runtime route, and send only worker-facing contract content.
5. **Integrate.** Inspect scope and evidence, run proportionate independent verification, integrate or reject the result, close the execution worker, and update the durable ledger. Retain one writer automatically when the reuse rule above applies; otherwise close it.
6. **Deliver.** Apply the selected delivery mode and the Git, PR, CI, and merge requirements in [references/delivery.md](references/delivery.md). SSLG does not initiate local or hosted code review.
7. **Replan or finish.** Continue from step 2 while required work remains; otherwise run the final goal gate.

Do not stop because an initial roadmap, one writer assignment, one Luna handoff, or a green intermediate commit is exhausted. Stop only when the goal is verified, the user changes it, or progress requires new authority, unavailable capability, or an unresolved Consequential Decision.

## Research and response economy

For Sol assignment formats, bounded depth-one read-only researchers, and Luna Compact/Full contracts, read [references/task-packets.md](references/task-packets.md) when preparing a dispatch.

Apply these rules before loading that reference:

- Shape only the next ready task and at most one provisional successor unless stable independent outcomes justify fanout.
- Start research with a viability scan. Return immediately on `NO-GO` or `PREREQUISITE`; use final `GO` only when the requested result is ready.
- Let a contract writer use a research child only under a depth-one budget recorded in its task packet and only when the child can answer a small read-only question without inheriting most of the writer's context. The orchestrator may grant this internal budget when the dispatch test passes; it does not require another user request.
- Require the shortest sufficient response, not an arbitrary bullet count. Preserve decision-critical nuance while excluding repeated facts and exploratory history.
- When necessary detail cannot be distilled safely, use an available bounded session artifact or `~/.codex/subagent-artifacts/scale-sol-luna-goals/<repository-id>/<skill-use-id>/`. Invoking the skill authorizes redacted, reconstructible artifacts at that external path. Record the pointer in goal state. Never write into the user's repository merely to shorten a handoff.

## Verification and recovery

- Before implementation, name the one or two affected QA seams in the task packet. Use value integrity, accessibility and interaction, public contract, or lifecycle and rendering. Add more only when the change genuinely crosses them.
- Give each affected seam one invariant, its cheapest faithful check, and one adjacent counterexample that could expose a displaced bug. Prefer compile fixtures, focused unit or component tests, deterministic lifecycle controls, then browser evidence when rendering owns the claim.
- For value changes, follow an emitted value through validation, canonical mutation, formatting, serialization, and back. For wrappers, compare direct and composed behavior when they promise parity.
- For interaction changes, test the rendered focus target and applicable input/state combinations. For public contracts, test supported construction forms and runtime guards. For lifecycle changes, test the changed mount, update, hide, cleanup, owner, or remount path.
- When modes, events, guards, retries, cancellation, or cleanup form a state machine, include the affected transition and failure paths in `DONE WHEN`. Use property checks, differential probes, or targeted mutations only when cheaper examples could pass without exercising the invariant.
- Let the worker run its `DONE WHEN` checks. Independently rerun an owning or integration check only for public boundaries, integration seams, behavior governed by a Consequential Decision, uncertain evidence, or changed state.
- Reuse unchanged baselines and successful checks. Run broad repository or release gates only when the repository requires them for final signoff.
- Distinguish product failure from environmental flakiness. Retry once only with evidence of a transient condition; otherwise record the environment blocker without automatically reshaping sound work.
- On worker failure, diagnose contract size, implementation error, and environment separately. Split or reduce an oversized task before increasing effort or changing model class.
- Require focused retirement accounting only for removal, move, rename, or replacement work.

Before any model-specific dispatch, read [references/runtime-routing.md](references/runtime-routing.md). Keep logical role requirements stable and runtime mappings isolated there.

## Completion

At each named checkpoint, assess assumptions, confidence, risks, rework, duplicated research, verification cost, and whether the roadmap still reflects integrated evidence. When a fix repeatedly reopens the same Failure Domain or expands its dependent failure surface, stop patch fanout and reframe that domain before dispatching more Luna work.

Before final signoff, verify the actual goal criteria, required retirement accounting, final integration checks, absence of unresolved required work, and the selected delivery mode's terminal state. Default completion requires the exact verified head to pass required CI and be merged. No-PR completion requires final local verification. No-merge completion requires final verification and green required CI, but not merge. Record a terminal outcome for every started subagent, complete the invocation record, update the durable goal snapshot, run `scripts/summarize_metrics.py`, and report whole-goal runtime telemetry plus the persisted subagent count and outcomes. Do not invent missing timing or require the user to ask for metrics analysis.
