---
name: scale-sol-luna-goals
description: >-
  Coordinate explicitly requested large goals through a persistent iterative
  roadmap while preserving main-thread context. Use when the user invokes
  $scale-sol-luna-goals or asks the orchestrator to delegate problem-space
  research and Luna-safe contract writing to capable Sol subagents, dispatch
  bounded Luna execution, integrate evidence, and continue across sub-goals
  until the whole goal is verified. By default, finish through local
  review-agent convergence, hosted PR review convergence, green required CI,
  and merge. Honor explicit no-PR, no-merge, and draft-PR constraints. The main
  orchestrator owns decisions, worker dispatch, integration, replanning, and
  completion.
---

# Scale Sol-Luna goals

## Normative ownership, terms, and precedence

This file is the sole normative source for role authority, the terms below, dispatch validity, rule precedence, and the canonical goal loop. The [task-packets reference](references/task-packets.md) owns only assignment schemas and Luna profile selection. The [runtime-routing reference](references/runtime-routing.md) owns only logical-to-runtime mappings and degraded-capability behavior. The [review-convergence reference](references/review-convergence.md) owns only the local and hosted review mechanics, review-contract stack, and manifest. The [outcome-metrics reference](references/outcome-metrics.md) owns only the required observation record and optional evaluation schema. References must not redefine this file's semantics.

- **Worth:** A delegated route's expected context, time, or confidence gain exceeds its setup, review, and integration cost.
- **Defined:** The question or outcome, authority, relevant state, and expected return are bounded.
- **Consequential Decision:** A choice that changes a public interface, ownership, security, data, migration, goal scope, or acceptance.
- **Decision-ready:** No unresolved Consequential Decision affects the proposed Luna task.
- **Failure Domain:** The state and behavior that could be affected or left inconsistent if work partially succeeds or fails.
- **Safe:** The outcome and its Failure Domain can be reviewed, accepted, rejected, and reverted together under one mutation owner.
- **Checkable:** The cheapest faithful check can observe the claimed result.
- **Review convergence:** An exact-head review cycle that ends only when its reviewer reports no actionable findings and its required checks are green.

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
commit, push, open or update a pull request, request review, resolve settled threads, mark the pull
request ready, and merge it. Do not ask for that authority again. Higher-level instructions and
explicit user restrictions still take precedence.

Apply these delivery modes. Equivalent wording has the same effect, and the most restrictive mode
wins:

| User request | Required delivery |
| --- | --- |
| No delivery restriction | Local gate, hosted gate, green required CI, then merge. |
| “Do not create a PR” | Local `review-agent` gate only; do not push, create a PR, run hosted review, or merge. |
| “Do not merge the PR” | Local and hosted gates with green required CI; leave the PR open and unmerged. |
| “Create a draft PR” | Keep the PR draft during review and request each hosted review with a top-level `@codex review` comment; after both gates pass, mark it ready and merge unless merge is also forbidden. |

“Do not create a PR” overrides draft-PR and no-merge instructions. “Do not merge” overrides the
default merge after a draft review.

- The orchestrator owns the user goal, roadmap, Consequential Decisions, contract acceptance, implementation-worker dispatch, integration, and completion.
- Sol contract writers research and propose; they do not decide for the orchestrator, implement, integrate, or declare completion. Under the review-phase `xhigh` profile, a contract writer may append normalized findings and proposed contracts only to its explicitly assigned external review-contract stack; persistence never accepts a finding disposition or contract and grants no repository, Git, or GitHub mutation authority.
- Reviewers inspect one exact target read-only and return findings. They do not shape contracts, implement, integrate, persist state, or dispatch another agent.
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

Keep goal state inline or in available task/session state by default. Persist it only with explicit authorization. Before repository-local persistence, verify that the target is ignored and assign one mutation owner. Keep persisted state bounded, redacted, safely discardable, reconstructible from current authorities, and non-authoritative. Treat missing, stale, corrupt, or partial state as a cache miss. Require no particular persistence path or directory layout.

```text
GOAL: completion criteria and next review checkpoint
STATE: commit plus relevant dirty state, document/dependency versions, and known baseline
DECISIONS: accepted decision IDs with evidence pointers
ACTIVE: task IDs, owners, and reserved mutation surfaces
NEXT: one ready task and at most one provisional successor
BLOCKERS: unresolved decisions, prerequisites, capability gaps, and risks
METRICS: current skill-use ID and record pointer or compact inline state
```

Replace superseded entries instead of appending history. Give each agent only relevant `KNOWN`, `VERIFY`, `UNKNOWN`, and `AVOID` facts. Require an evidence gap or changed state before repeating prior research.

## Reuse and retained writers

Treat agent output as candidate evidence, not authority. `KNOWN` means a current, source-backed fact admitted by the orchestrator; keep accepted Consequential Decisions separate. Prior conversation, review, persistence, or model identity never upgrades a claim.

Keep writers ephemeral by default. At integration, retain one idle same-domain writer through the next framing checkpoint only when one probable sequential reuse is named. Resume it only after the new assignment passes the validity and Worth filters. Treat every resumption as a new dispatch and provide the current question, authority, material state delta, stop conditions, and expected return. Carry no mutation right, accepted fact, decision, or runtime guarantee through retention.

Reuse only selected findings with authoritative evidence pointers, applicability, last-checked state, and invalidation triggers. Revalidate affected findings after material drift. If retained context is unreliable or its runtime cannot satisfy the new assignment's verified route, dispatch a fresh writer or keep the work pending.

Use independent evidence review only when an incorrect reused finding could affect a Consequential Decision or several later assignments and the review is Worth. Treat review as a read-only Sol assignment. Reviewers may support, qualify, reject, or deduplicate candidate claims; only the orchestrator may admit findings into current task state or accept decisions.

## Canonical iterative goal loop

At invocation, read [references/outcome-metrics.md](references/outcome-metrics.md) and initialize its durable skill-use record before dispatching work. Metrics persistence is authorized by this skill and remains outside the repository and its worktrees.

Repeat this loop until the whole goal is verified:

1. **Frame.** Confirm the goal, completion criteria, state, accepted decisions, dependencies, and the next meaningful review checkpoint.
2. **Research.** Select the smallest uncertainty that unlocks valuable work. Dispatch a Sol writer only when the dispatch test passes; otherwise research in the main thread. Stop early on a precise `NO-GO` or `PREREQUISITE`.
3. **Shape.** Resolve Consequential Decisions in the main thread and choose one dependency-ready outcome. Select its Luna profile from [references/task-packets.md](references/task-packets.md).
4. **Dispatch.** Recheck the task fingerprint; treat changed facts, decisions, ownership, constraints, or checks as material drift requiring re-adjudication. Reserve mutation ownership, verify the current runtime route, and send only worker-facing contract content.
5. **Integrate.** Review scope and evidence, run proportionate independent verification, integrate or reject the result, close the execution worker, and update the ledger. Retain one writer through the next framing checkpoint only when a same-domain use is named; otherwise close it.
6. **Review-converge and deliver.** Apply the selected delivery mode, then run its local gate, hosted gate, and merge requirements from [references/review-convergence.md](references/review-convergence.md). Feed accepted findings back through Shape, Dispatch, and Integrate. Never skip a required gate or infer cleanliness after a changed head.
7. **Replan or finish.** Feed findings back into the roadmap. Continue from step 2 while required work remains; otherwise run the final goal gate.

Do not stop because an initial roadmap, one writer assignment, one Luna handoff, a locally clean review, or a green intermediate commit is exhausted. Stop only when the goal is verified, the user changes it, or progress requires new authority, unavailable capability, or an unresolved Consequential Decision.

## Research and response economy

For Sol assignment formats, optional depth-one read-only researchers, and Luna Compact/Full contracts, read [references/task-packets.md](references/task-packets.md) when preparing a dispatch.

Apply these rules before loading that reference:

- Shape only the next ready task and at most one provisional successor unless stable independent outcomes justify fanout.
- Start research with a viability scan. Return immediately on `NO-GO` or `PREREQUISITE`; use final `GO` only when the requested result is ready.
- Let a contract writer use a research child only under an explicit depth-one budget and only when the child can answer a small read-only question without inheriting most of the writer's context.
- Require the shortest sufficient response, not an arbitrary bullet count. Preserve decision-critical nuance while excluding repeated facts and exploratory history.
- Use a shared session artifact for necessary long detail only when explicitly authorized and available. Never write into the user's repository merely to shorten a handoff.

## Verification and recovery

- Let the worker run its `DONE WHEN` checks. Independently rerun an owning or integration check only for public boundaries, integration seams, behavior governed by a Consequential Decision, uncertain evidence, or changed state.
- Reuse unchanged baselines and successful checks. Run broad repository or release gates only at review milestones and final signoff.
- Distinguish product failure from environmental flakiness. Retry once only with evidence of a transient condition; otherwise record the environment blocker without automatically reshaping sound work.
- On worker failure, diagnose contract size, implementation error, and environment separately. Split or reduce an oversized task before increasing effort or changing model class.
- Require focused retirement accounting only for removal, move, rename, or replacement work.

Before any model-specific dispatch, read [references/runtime-routing.md](references/runtime-routing.md). Keep logical role requirements stable and runtime mappings isolated there.

## Completion and review

At each named review checkpoint, assess assumptions, confidence, risks, rework, duplicated research, verification cost, and whether the roadmap still reflects integrated evidence. When a fix repeatedly reopens the same Failure Domain or expands its dependent failure surface, stop patch fanout and reframe that domain before dispatching more Luna work.

Before final signoff, verify the actual goal criteria, required retirement accounting, final integration checks, absence of unresolved required work, and the selected delivery mode's terminal state. Default completion requires the reviewed green head to be merged. No-PR completion requires a clean current local gate. No-merge completion requires a clean current local gate, clean exact-head hosted review, green required CI, and no unresolved review threads. Complete the current skill-use record, including null, negative, ambiguous, and unavailable observations.
