---
name: shape-luna-contract
description: >-
  Shape exactly one next-dispatch Luna implementation contract from current
  evidence. Use when asked for the next worker task, a Luna-sized task packet,
  or an incremental Sol-Luna orchestration step where early blockers or scope
  revisions could make a full dependency map stale. Return one ready contract,
  a high-capability escalation, one precise prerequisite, or a no-op. Do not
  map the whole problem, implement the work, or dispatch an agent.
---

# Shape a Luna contract

Turn current implementation evidence into exactly one dependency-ready worker contract that can
be accepted, rejected, and verified on its own. Optimize for the next dispatch, not for a complete
forecast of the remaining goal. Name at most one provisional successor when it helps the caller
retain direction.

This incremental horizon is deliberate. Re-shape after integration, a blocker, or a material scope
revision so later contracts reflect current evidence instead of a dependency map that has gone
stale.

This skill is the sole normative source for next-dispatch Luna decomposition, contract validity,
profile selection, worker-facing schemas, contract-owned QA seams, and the parent dispatch record.
The caller still owns the larger goal, accepted decisions, sequencing, dispatch, integration,
replanning, and completion.

Use `map-luna-contracts` instead only when the caller asks for a multi-contract dependency map,
shared-surface coordination across contracts, or one unified validation plan. A map is not a
prerequisite for this skill.

## Boundaries

- Inspect only the authoritative sources needed to choose and bound the next valuable outcome.
- Treat prior plans, agent output, persistence, and provisional successors as candidate evidence
  until current authority supports them.
- Do not make a Consequential Decision: a choice that changes a public interface, ownership,
  security, data, migration, goal scope, or acceptance.
- Do not implement, mutate project state, dispatch an agent, select runtime models, or declare the
  larger goal complete.
- Return `PREREQUISITE` when missing authority, evidence, or an unresolved Consequential Decision
  prevents a trustworthy next contract. State the exact prerequisite rather than filling the gap.
- For an indivisible `ESCALATE` outcome, identify any design choices that must remain coupled to
  implementation. The shaper does not make those choices or grant decision authority; it gives the
  caller enough information to freeze them or approve a bounded coupled-decision mandate.

## Luna eligibility gate

Before trying to split or shape the outcome, decide whether a bounded Luna execution worker may own
it. Do not make a strategically coupled outcome appear Luna-safe by slicing its files or steps.

Return `ESCALATE` when any of these holds:

- The work designs or implements a state-chart, state machine, actor protocol, orchestration
  protocol, or workflow topology. This includes changing states, events, transitions, guards,
  actions, invoked actors, context ownership, persistence, cancellation, or lifecycle semantics.
- Consequential architectural decisions must remain coupled to implementation for correctness.
- The outcome requires global reasoning across interacting authority, concurrency, recovery,
  security, migration, or public-contract invariants that cannot be frozen into one bounded packet.
- Splitting would create unsafe intermediate states, divided ownership of one invariant, or checks
  that cannot faithfully accept or reject each slice on its own.

An adjacent test, adapter, documentation update, or mechanical caller migration may still be
Luna-eligible when its contract does not design, implement, or alter the protected protocol. Never
split an escalated outcome merely to avoid the escalation.

An escalation fixes the capability floor and reasoning effort independently. Require the
highest-capability implementation route, choose `high`, `xhigh`, or `max` from the work's actual
reasoning demands. Never select `ultra`. This is a logical requirement; the caller resolves and
verifies the concrete runtime mapping. If the selected route is unavailable, the work remains
pending rather than falling back to Luna.

Use this effort policy for escalated state-chart work:

- Use `high` only to implement already-frozen states, transitions, guards, actions, and acceptance
  checks when the work is primarily faithful translation rather than protocol design.
- Use `xhigh` by default for state-chart design, material semantic changes, and semantic
  verification.
- Use `max` only when a named irreducible interaction spans nested or parallel states, multiple
  actors, time, cancellation, retry or recovery, persistence, authority, security, migration, or
  public consumers and `xhigh` may not faithfully adjudicate it.

A state-chart label, file count, or broad task size does not independently justify `max`. Record the
trigger and why the lower effort is insufficient. Prefer `xhigh` when decisions and acceptance are
already bounded; unnecessary `max` reasoning can reopen frozen decisions, expand scope, or invent
abstractions outside the goal.

## Contract validity

The contract must be:

- **Defined:** one outcome, relevant state, authority, constraints, and expected return are bounded.
- **Decision-ready:** no unresolved Consequential Decision affects implementation.
- **Safe:** its Failure Domain can be evaluated, accepted, rejected, and reverted under one
  mutation owner. The Failure Domain is the state and behavior that partial success or failure
  could leave inconsistent.
- **Checkable:** the cheapest faithful check can observe the claimed result.

Redefine work that is not Checkable. Split work that is not Safe or Luna-sized, then shape only the
first dependency-ready slice. Return `PREREQUISITE` rather than hiding an unresolved decision in a
worker prompt.

## Workflow

1. **Establish current state.** Confirm the goal checkpoint, relevant fingerprint, accepted
   decisions, authoritative sources, baseline, protected areas, active mutation owners, and known
   blockers.
2. **Choose the next outcome.** Select the highest-value outcome whose dependencies are satisfied
   now. Prefer an end-to-end behavior slice over a file, layer, setup step, or speculative future
   task.
3. **Apply the Luna eligibility gate.** Return `ESCALATE` before decomposition when the outcome owns
   indivisible high-capability design or implementation.
4. **Resolve the decision boundary.** Freeze accepted behavior and constraints. If implementation
   still requires a Consequential Decision that the orchestrator can resolve separately, return
   that prerequisite.
5. **Bound the Failure Domain.** Give one owner exact mutation authority. Separate protected and
   concurrently owned surfaces. Split the task if partial failure cannot be accepted or reverted
   as one unit.
6. **Choose QA seams.** Select the one or two affected QA seams and define the invariant, cheapest
   faithful check, and one adjacent counterexample.
7. **Write one contract.** Choose Compact or Full. Include only worker-facing evidence and
   constraints. Record at most one provisional successor outside the worker prompt.

## QA seams

Choose only seams the outcome affects:

- **Value integrity:** the implementation preserves the intended user or system outcome.
- **Accessibility and interaction:** input, focus, semantics, and assistive behavior remain usable.
- **Public contract:** callers, types, schemas, APIs, and compatibility boundaries stay coherent.
- **Lifecycle and rendering:** ordering, retries, cancellation, cleanup, persistence, and rendered
  state remain correct.

Prefer compile fixtures, focused unit or component tests, and deterministic lifecycle controls.
Require browser evidence when rendering owns the claim. Use property checks, differential probes,
or targeted mutations only when cheaper examples could pass without exercising the invariant.

When apparently local work reveals coordinated modes, events, guards, effects, retries,
cancellation, cleanup, or interacting processes, stop and reapply the Luna eligibility gate. The
worst state machine is the one you don't know you're writing.

## Profile selection

Use **Compact** for one bounded, independently verifiable outcome.

Use **Full** only when that same outcome changes a public boundary, security or data behavior,
migration or deletion, several integration seams, a known red baseline inside its Failure Domain,
or another invariant governed by a Consequential Decision. Add only the triggered sections. If the
Full additions make the task incoherent, split it and shape the first slice instead.

## Compact worker contract

```text
GOAL
One independently verifiable outcome.

STATE
Relevant fingerprint, accepted facts, satisfied dependencies, and facts to avoid assuming.

AUTHORITY
Read: sources Luna may inspect.
Mutate: exact files, data, or actions Luna may change; protected and concurrently owned areas.

DECISIONS AND CONSTRAINTS
Frozen interfaces, behavior, policy, and invariants.

DONE WHEN
Affected QA seams; invariant; cheapest faithful checks; adjacent counterexample; required artifacts;
and evidence to return.

STOP AND RETURN
False assumptions, dependency drift, scope or decision changes, ownership conflicts, or evidence
outside authority.

HANDOFF
Shortest sufficient summary; artifacts; commands with concise results; deviations and unresolved
risks.
```

## Full additions

Add only the sections required by risk:

```text
RISKS AND CASES
Relevant invariants, hostile inputs, rollback boundaries, or failure cases.

BASELINE
Relevant known failures before the task; evidence pointer instead of full logs.

INTEGRATION RATCHET
Cheapest check that detects a new failure in the owned Failure Domain.

RETIREMENT ACCOUNTING
Artifacts removed, moved, renamed, or replaced; callers and evidence preserved; focused reference
scan.
```

## Result

Return one of:

- `READY`: exactly one worker contract, its profile, decisive evidence pointers, and at most one
  provisional successor for the caller.
- `ESCALATE`: the indivisible outcome, reason it is not Luna-safe, coupled decision questions and
  invariants, exact authority and acceptance boundary, questions that require a caller-approved
  bounded coupled-decision mandate, and the logical requirement for the highest-capability
  implementation route with independently selected `high`, `xhigh`, or `max` effort and `ultra`
  forbidden.
- `PREREQUISITE`: the exact missing decision, evidence, authority, dependency, or mutation owner.
- `NO-OP`: evidence that no implementation outcome is currently required at this checkpoint.

When composed inside an orchestrator, also return this logical parent-only record. Never put it in
a Luna prompt, and do not fill caller-owned runtime fields:

```text
TASK: ID, profile, outcome and Failure Domain, prerequisite state, split/reshape trigger
ROUTE REQUIREMENT: execution-worker role and logical capability or verification constraints
OWNERSHIP: mutation reservation, protected surfaces, and concurrent tasks
NEXT: at most one provisional successor plus its dependency or reshape trigger
```

After accepting the result, the caller augments it with the concrete runtime mapping, selected and
effective worker effort, context fork, and route-verification evidence. Those fields are not part of
the shaper result.

For `ESCALATE`, replace `TASK` and `ROUTE REQUIREMENT` with:

```text
ESCALATION: outcome, indivisible Failure Domain, coupled decision questions/invariants, exact authority, acceptance checks, and required decision-mandate boundary
ROUTE REQUIREMENT: highest-capability implementer, required logical high/xhigh/max effort, effort trigger, why lower effort is insufficient when max, and ultra forbidden
```

The caller must freeze the coupled questions or approve the bounded decision mandate before
dispatch, then populate the concrete runtime mapping, effective effort confirmation, context fork,
and route-verification evidence.
