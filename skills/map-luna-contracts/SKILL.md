---
name: map-luna-contracts
description: >-
  Map a large implementation problem into dependency-aware execution nodes,
  shape Luna-eligible nodes through shape-luna-contract, preserve indivisible
  high-capability work, coordinate shared-surface ownership and dispatch waves,
  and define one unified validation plan. Use when the caller explicitly needs
  a whole-problem contract map, coordinated parallel work, or durable cross-
  contract planning. Do not use for ordinary next-dispatch shaping when early
  blockers or scope revisions may invalidate later work. Do not implement or
  dispatch.
---

# Map Luna contracts

Turn current implementation evidence into a dependency-aware contract map for the stated problem.
Use [shape-luna-contract](../shape-luna-contract/SKILL.md) as the normative shaper for every
Luna-eligible worker contract and as the eligibility gate for high-capability execution nodes. This
skill adds only set-level coverage, dependency, shared-surface, scheduling, and validation
semantics.

Do not use this skill as a mandatory preflight for `scale-sol-luna-goals`. A full map has a higher
planning cost and a larger invalidation surface than one next-dispatch contract. Use it when the
caller values a whole-problem map enough to accept that later nodes may need reshaping after early
evidence changes.

The caller still owns the larger goal, accepted decisions, route selection, worker dispatch,
integration, replanning, and completion.

## Composition contract

Before shaping any worker node, read `../shape-luna-contract/SKILL.md` completely.

- Apply its boundaries, contract validity rules, profile selection, QA seams, worker schemas, and
  result semantics to each node.
- Do not copy, summarize, or redefine those rules here.
- A per-node `ESCALATE` becomes a `requires-higher-capability` graph node. Preserve the indivisible
  Failure Domain and required route; do not split it again to manufacture Luna work.
- Do not apply the shaper to an outcome whose named graph dependencies are incomplete. Preserve it
  as an unshaped `blocked-by-dependency` node with the known outcome, dependency IDs, expected
  produced-state handoff, and reshape trigger.
- A per-node `PREREQUISITE` becomes a set-level prerequisite when it blocks trustworthy mapping, or
  an unshaped `reshape-after-evidence` node when named non-dependency evidence can resolve it. Never
  weaken it into a dispatchable contract.
- A per-node `NO-OP` removes that node unless its absence is itself evidence needed by goal
  closure.
- Preserve the next-dispatch skill's parent record per node. Its provisional `NEXT` must be `none`
  or match an existing successor and dependency or reshape trigger in the graph. The graph is
  authoritative; a newly suggested successor outside it invalidates the affected map rather than
  silently extending it. Add set-level records separately.

## Boundaries

- Inspect the authoritative sources needed to establish the goal's affected surface, not only the
  first likely edit.
- Treat prior plans, agent output, and persisted maps as candidate evidence until current authority
  supports them.
- Do not make a Consequential Decision, implement, mutate project state, dispatch an agent, select
  runtime models, or declare the larger goal complete.
- Do not call the set complete while a goal criterion lacks both an owning execution node and an
  observing validation check.
- Return `PREREQUISITE` when missing authority, evidence, or an unresolved Consequential Decision
  prevents a trustworthy map. Include stable partial structure only when it is clearly marked
  non-dispatchable.

## Set validity

The mapped execution-node set must be:

- **Complete:** every goal criterion and required retirement outcome maps to at least one execution
  node, whether it is a shaped Luna contract or a `requires-higher-capability` escalation node.
- **Non-overlapping:** concurrent execution nodes have disjoint mutation ownership. Serial nodes
  that touch the same surface name the order, handoff state, and revalidation trigger.
- **Connected:** every dependency, produced artifact, consumer, and shared surface appears in the
  graph instead of remaining implicit in prose.
- **Closed:** node checks, cross-node seam checks, and final integration checks collectively
  prove the original goal rather than only the individual edits.

Add an edge, serialize work, or merge nodes when apparently separate outcomes cannot be accepted
independently. Keep uncertainties visible as reshape triggers instead of inventing details.

## Mapping workflow

1. **Establish goal closure.** Confirm the current fingerprint, completion criteria, authoritative
   sources, accepted decisions, baseline, protected areas, concurrent owners, and the caller's
   reason for accepting whole-map planning cost. Create one coverage row per criterion.
2. **Protect indivisible high-capability domains.** Apply the `shape-luna-contract` eligibility gate
   to each candidate domain before splitting it. Preserve state-chart and other escalated design or
   implementation as one high-capability node; do not partition it by state, transition, file, or
   implementation step to manufacture Luna contracts.
3. **Map eligible outcomes.** Identify the currently knowable implementation, migration, cleanup,
   compatibility, and evidence outcomes outside those protected domains. Prefer end-to-end
   behavior slices over file, layer, or setup-only partitions.
4. **Build the graph.** Give every outcome a stable node ID. Record prerequisite nodes,
   produced state, consumers, and earliest safe wave. Detect cycles and orphan nodes.
5. **Build the shared-surface ledger.** Record every file, API, type, schema, state owner, fixture,
   generated artifact, or operational boundary used by more than one node. Assign one mutation
   owner per wave or serialize mutation with an explicit compatibility rule.
6. **Classify and shape eligible nodes.** Apply `shape-luna-contract` only to outcomes whose named
   dependencies are satisfied now. Preserve outcomes with incomplete graph dependencies as
   unshaped `blocked-by-dependency` nodes. A map may contain many shaped contracts even though the
   component skill returns exactly one per application. Preserve `ESCALATE` outcomes as non-Luna
   nodes and mark other evidence-dependent outcomes for later reshaping.
7. **Unify validation.** Retain each shaped Luna contract's checks and each high-capability
   escalation node's acceptance and verification checks. Add shared-surface checks at producer and
   consumer boundaries, and map every goal criterion to a final observing check.
8. **Audit the set.** Reject missing criteria, nodes without goal value, hidden shared mutation,
   dependency cycles, duplicate work, missing cleanup, and closure checks that observe only local
   edits.

## Contract graph

Emit:

```text
NODE | OUTCOME | ROUTE | PROFILE | STATUS | DEPENDS ON | PRODUCES | MUTATES | SHARED SURFACES | WAVE
```

Use these statuses:

- `ready`: all dependencies and contract prerequisites are satisfied and the shaper returned
  `READY` against the current fingerprint.
- `blocked-by-dependency`: the outcome is provisionally mapped but must remain unshaped until all
  named graph dependencies are integrated and their produced state is current.
- `reshape-after-evidence`: the outcome is known, but later evidence must be integrated before
  applying `shape-luna-contract` again.
- `requires-higher-capability`: the outcome failed the Luna eligibility gate and requires the
  highest-capability implementation route with effort selected independently as `high`, `xhigh`,
  or `max`; `ultra` is forbidden.

Use `Compact` or `Full` for a shaped Luna node's `PROFILE`, `unshaped` for
`blocked-by-dependency` and `reshape-after-evidence`, and `n/a` for
`requires-higher-capability`.

Only `ready` contracts may be dispatched to Luna. Do not invent a Luna prompt for a
`blocked-by-dependency`, `reshape-after-evidence`, or `requires-higher-capability` node. An unshaped
node may record candidate shared surfaces for coordination, but it owns no mutation authority and
its profile, checks, and worker packet remain unset. Its `WAVE` is only the earliest candidate wave,
not dispatch authority, and must be recomputed after shaping. After its dependencies or named
evidence are integrated, reapply `shape-luna-contract` against the current fingerprint before
changing its status to `ready` or `requires-higher-capability`. Route the latter using its
escalation record and preserve it as a dependency for downstream nodes.

For example, a map that introduces a state-chart may contain one mechanical port adapter, one
indivisible high-capability state-chart node, and later mechanical caller and black-box test nodes.
The later nodes remain unshaped and blocked by dependency until the state-chart output is
integrated. They do not own its states, transitions, guards, actions, actors, or lifecycle
semantics.

## Shared-surface ledger

Emit:

```text
SURFACE | NODES | MUTATION OWNER/ORDER | INVARIANT | COMPATIBILITY CHECK | INVALIDATION TRIGGER
```

Sharing a surface does not authorize concurrent mutation. Prefer one producer with explicit
consumers. When serial mutation is unavoidable, later nodes receive the integrated fingerprint
and must revalidate the named invariant before editing.

## Unified validation plan

Use the smallest faithful set of checks across three levels:

1. **Node checks:** owned by every executable node. A shaped Luna contract contributes its
   `DONE WHEN` checks; a `requires-higher-capability` node contributes the acceptance and
   verification checks in its escalation record.
2. **Shared-surface checks:** run after the last producer and before dependent consumers rely on
   the surface. Exercise the relevant boundary invariant, such as direct/composed parity, write
   closure, lifecycle ordering, or schema compatibility.
3. **Goal-closure checks:** run after the final relevant wave and observe the original completion
   criteria end to end. Reuse lower-level evidence only when state and claim are unchanged.

Emit:

```text
CRITERION | PRODUCING NODES | OBSERVING CHECK | RUN AFTER | EVIDENCE OWNER
```

If the mapped work contains coordinated modes, events, guards, effects, retries, cancellation,
cleanup, or interacting processes, map the state transitions and failure paths across the relevant
nodes and validation rows. Flag the protocol to the caller. The worst state machine is the one you
don't know you're writing.

## Invalidation and replanning

Version the map against its authoritative fingerprints. Name invalidation triggers for decisions,
dependency outputs, shared surfaces, baselines, and goal scope.

After a trigger fires:

1. Freeze affected dispatches.
2. Preserve unaffected integrated evidence.
3. Recompute affected edges, waves, shared-surface ownership, and closure rows.
4. Reapply `shape-luna-contract` only to affected nodes.

Do not recreate the entire map when the changed evidence has a bounded downstream closure.

## Result

Return one of:

- `READY`: goal coverage matrix, complete graph, shared-surface ledger, dispatch waves, unified
  validation plan, shaped Luna contracts, preserved high-capability escalation nodes, and decisive
  evidence pointers.
- `PREREQUISITE`: the exact missing decision, evidence, authority, or dependency owner plus stable
  partial structure clearly marked non-dispatchable.
- `NO-OP`: evidence that no implementation outcomes remain.

When composed inside an orchestrator, add this set-level record. Keep each component skill's
parent-only contract record unchanged and never put either record in a Luna prompt:

```text
SET: ID, goal fingerprint, coverage, graph version, shared surfaces, validation plan
ORDER: dependency edges, dispatch waves, mutation ownership, and produced-state handoffs
INVALIDATE: triggers, affected downstream closure, and reshape checkpoints
```
