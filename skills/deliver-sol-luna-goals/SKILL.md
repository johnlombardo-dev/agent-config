---
name: deliver-sol-luna-goals
description: >-
  Research and deliver one explicit large goal through a persistent iterative
  Sol-to-Luna loop conducted in the main thread. Use when the user invokes
  $deliver-sol-luna-goals or asks the current Sol orchestrator to resolve the
  problem space, shape successive bounded Luna tasks, integrate their evidence,
  and continue until the whole goal is verified. The orchestrator owns
  architecture, sequencing, worker dispatch, integration, replanning, and
  completion.
---

# Deliver Sol-Luna goals

## Normative ownership, terms, and precedence

This file is the sole normative source for role authority, dispatch routing, rule precedence, and the canonical goal loop. The standalone [shape-luna-contract skill](../shape-luna-contract/SKILL.md) owns next-dispatch Luna decomposition, contract validity and profiles, worker-facing schemas, contract-owned QA seams, and parent dispatch records. The [runtime-routing reference](references/runtime-routing.md) owns only logical-to-runtime mappings and degraded-capability behavior. The [outcome-metrics reference](references/outcome-metrics.md) owns only the optional reporting schema. These sources must not redefine one another's semantics.

- **Worth:** A delegated route's expected context, time, or confidence gain exceeds its setup, review, and integration cost.
- **Defined:** The outcome, authority, relevant state, and expected return are bounded.
- **Consequential Decision:** A choice that changes a public interface, ownership, security, data, migration, goal scope, or acceptance.
- **Decision-ready:** No unresolved Consequential Decision affects the proposed Luna task.
- **Failure Domain:** The state and behavior that could be affected or left inconsistent if work partially succeeds or fails.
- **Safe:** The outcome and its Failure Domain can be reviewed, accepted, rejected, and reverted together under one mutation owner.
- **Checkable:** The cheapest faithful check can observe the claimed result.

Apply orchestration rules as ordered filters:

1. Higher-level instructions, user authorization, and model policy define the permitted routes.
2. Current capability removes routes that cannot be used or verified as required.
3. Assignment validity requires Defined, Decision-ready, Safe, and Checkable work.
4. Worth selects delegation or the fast path among the routes still permitted.
5. `shape-luna-contract` governs Luna eligibility, high-capability escalation, and each next Luna contract's detail.
6. Verification rules govern evidence depth and reuse.

Each layer constrains the next; a lower layer never relaxes a higher one. First make the assignment valid, then choose its route. Worth never cures invalidity: for example, Worth but uncheckable work must be redefined rather than dispatched. A required route that is unavailable or invalid remains pending instead of being silently substituted.

## Authority and invariants

Keep the Sol orchestrator authoritative for the entire goal.

- Sol owns research, Consequential Decisions, sequencing, contract shaping, implementation-worker dispatch, integration, and completion.
- Luna executes one accepted task with frozen Consequential Decisions. It stops when success requires a decision or scope change and cannot dispatch another agent.
- A high-capability implementer owns an indivisible `ESCALATE` outcome, including state-chart design or implementation, at the highest-capability verified route. Select reasoning effort independently as `high`, `xhigh`, or `max` under the shaping policy. Never use `ultra`, silently change the selected route, or split such work merely to make it Luna-routable.
- Give every mutation surface one active owner. Parallel work must be independently acceptable and non-overlapping.
- Return distilled results and evidence pointers, not raw logs or reasoning traces.
- A handoff advances the goal loop; it never completes the larger goal by itself.

Use `scale-sol-luna-goals` when delegating research and contract writing to Sol subagents would materially protect main-thread context or add real parallelism.

## Fast path and dispatch test

After assignment validity is established, choose the cheapest permitted route:

- Execute bounded work directly when ordinary instructions and model policy permit and coordination would cost more than implementation.
- Otherwise apply `shape-luna-contract` to produce the next dispatchable contract.

`map-luna-contracts` is not part of this canonical path. Use it only when the user separately asks
for a whole-problem dependency map or coordinated multi-contract plan.

Dispatch Luna only when it is Worth, Defined, Decision-ready, Safe, and Checkable.

If not Defined, frame it. If not Decision-ready, research or decide. If not Safe, split it. If not Checkable, redefine the expected result. Only after validity is established, use the fast path when delegation is not Worth.

## Compact goal state

Maintain a replaceable goal ledger outside the active prompt when task state or a shared session artifact is available; otherwise keep the smallest inline version. Never create a repository artifact solely for orchestration without authorization.

```text
GOAL: completion criteria and next review checkpoint
STATE: commit plus relevant dirty state, document/dependency versions, and known baseline
DECISIONS: accepted decision IDs with evidence pointers
ACTIVE: task IDs, owners, and reserved mutation surfaces
NEXT: one ready task and at most one provisional successor
BLOCKERS: unresolved decisions, prerequisites, capability gaps, and risks
```

Replace superseded entries instead of appending history. Reuse accepted evidence unless relevant state changed or the evidence is insufficient for the current decision.

## Canonical iterative goal loop

Repeat this loop until the whole goal is verified:

1. **Frame.** Confirm the goal, completion criteria, state, accepted decisions, dependencies, and next meaningful review checkpoint.
2. **Research.** Investigate only the smallest uncertainty that unlocks valuable work. Stop when enough evidence exists to decide the next outcome; record precise `NO-GO` and prerequisites as useful results.
3. **Shape.** Before each implementation dispatch, read [shape-luna-contract](../shape-luna-contract/SKILL.md) completely and apply it to exactly one dependency-ready outcome. Freeze Consequential Decisions in the main thread. Admit its `READY` Luna contract or preserve its `ESCALATE` outcome for the required high-capability route; feed `PREREQUISITE` or `NO-OP` back into the goal loop. If the skill is unavailable or unreadable, record a capability blocker instead of reconstructing its rules.
4. **Dispatch.** Recheck the task fingerprint; treat changed facts, decisions, ownership, constraints, dependencies, or checks as material drift requiring reshaping. Reserve mutation ownership, verify the current runtime route, and send only route-appropriate worker content. Never send an `ESCALATE` outcome to Luna.
5. **Integrate.** Review scope and evidence, run proportionate independent verification, integrate or reject the result, close the worker, and update the ledger.
6. **Replan or finish.** Feed findings back into the roadmap. Reapply `shape-luna-contract` while required work remains; otherwise run the final goal gate.

Do not stop because an initial roadmap or one Luna handoff is exhausted. Stop only when the goal is verified, the user changes it, or progress requires new authority, unavailable capability, or an unresolved Consequential Decision.

## Task and response economy

Use [shape-luna-contract](../shape-luna-contract/SKILL.md) for next-dispatch Luna decomposition, profiles, worker-facing task formats, and parent-only records.

- Require the shortest sufficient worker handoff, with decision-critical nuance, artifacts, concise evidence, and deviations.
- Use a shared session artifact for necessary long detail only when explicitly authorized and available. Never write into the user's repository merely to shorten a handoff.

## Verification and recovery

- Let Luna run its `DONE WHEN` checks. Independently rerun an owning or integration check only for public boundaries, integration seams, behavior governed by a Consequential Decision, uncertain evidence, or changed state.
- Reuse unchanged baselines and successful checks. Run broad repository or release gates only at review milestones and final signoff.
- Distinguish product failure from environmental flakiness. Retry once only with evidence of a transient condition; otherwise record the environment blocker without automatically reshaping sound work.
- On worker failure, diagnose contract size, implementation error, and environment separately. Split or reduce an oversized task before increasing effort or changing model class.
- Require focused retirement accounting only for removal, move, rename, or replacement work.

Before model-specific dispatch, read [references/runtime-routing.md](references/runtime-routing.md). Keep logical role requirements stable and runtime mappings isolated there.

## Completion and review

At each named review checkpoint, assess assumptions, confidence, risks, rework, verification cost, and whether the roadmap still reflects integrated evidence.

Before final signoff, verify the actual goal criteria, required retirement accounting, final integration checks, and absence of unresolved required work. For unusually long goals or requested cost analysis, read [references/outcome-metrics.md](references/outcome-metrics.md).
