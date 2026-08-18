---
name: evidence-backed-planning
description: Create, revise, or assess rigorous project and initiative plans from comparisons, prototypes, audits, incidents, prior implementations, and verification results. Use when planning a new project, consolidating lessons from competing executions, converting defects into acceptance gates, deciding which prototype ideas to adopt, or preventing green isolated checks from masking composed-system, recovery, parity, capacity, security, operations, usability, and delivery gaps.
---

# Evidence-backed planning

Turn past execution evidence into a plan whose risky claims have named owners and faithful proofs. Do not choose an entire prototype when the evidence supports different designs at different seams.

## Workflow

1. Freeze inputs. Record source IDs or links, repository fingerprints, dirty state, dates, claimed outcomes, failed checks, and unverified surfaces.
2. Rank evidence. A demonstrated user-visible failure outranks broad green gates. Current product decisions outrank prototype choices. Cost and elapsed time are constraints, not quality evidence.
3. Build a behavioral-seam manifest before phasing work. Include durable writes, external effects, public contracts, state/workflow, recovery, trust boundaries, scale, operations, documentation, and delivery as applicable.
4. Create an applicability ledger using shields S01-S12 from [references/planning-shields.md](references/planning-shields.md). Mark each `required`, `not applicable`, or `gap` with concrete evidence or a reason.
5. Record decisions per seam: chosen design, supporting evidence, rejected alternative, consequence, and verification obligation. Prefer a hybrid only when ownership remains coherent.
6. Convert prior findings into traceability rows: finding or risk, violated invariant, planned control, faithful proof, phase owner, and status. Do not silently drop inconvenient defects.
7. Plan vertical outcome slices. A phase closes a behavior across its relevant domain, persistence, effect, public surface, failure path, and recovery; package or file completion alone is not an exit gate.
8. Separate evidence tiers and promotion language. Static, isolated, composed, capacity, live, security, deployed operations, documentation, and delivery evidence never imply one another.
9. Use [assets/plan-template.md](assets/plan-template.md) when creating a new plan. Run `python3 scripts/check_plan.py PLAN.md [supporting evidence files...]` from this skill directory or pass absolute paths.

## Planning rules

- Specify the highest faithful observable outcome before implementation tasks.
- Require write/read closure for every writable value or durable mutation.
- Require effect/persistence/recovery closure when local state records an external effect.
- Require control/state closure when an API, CLI, UI, or job reports a workflow transition.
- Require backup/full-restore closure for durable products; a backup command is not recovery evidence.
- Inventory duplicated paths and create parity matrices rather than testing each path independently.
- Make fakes preserve production return shapes, optionality, completion, errors, ordering, cancellation, backpressure, and resource ownership. Add production-adapter contract probes when feasible.
- Derive capacity gates from adversarial input shapes and public-boundary behavior, not only hot inner loops.
- Define operational success as an observed postcondition. Command lists and mocked call counts are weak evidence.
- Name state machines and actor-like protocols. States describe work that is currently active; owners hold retries, cancellation, effects, and cleanup.
- Treat README, runnable commands, repository history, rollback, and truthful delivery state as product usability and maintainability evidence.
- Preserve explicit gaps. Never convert `not run`, `not authorized`, `no remote`, or `partial review` into a passing claim.

## Structural encoding

Choose the strongest practical mechanism for each lesson:

1. Make invalid states unrepresentable in types or schemas.
2. Add a lint, banned API, or policy check.
3. Centralize the behavior in one canonical helper or contract.
4. Add a runtime invariant or migration guard.
5. Add an executable composed-path, parity, failure-injection, capacity, or operations probe.
6. Use prose only for judgment that cannot be enforced structurally, and include the failure example that justifies it.

The final plan must state which mechanism carries each recurring lesson.

## Completion standard

A plan is implementation-ready only when:

- evidence sources and limits are explicit;
- S01-S12 are routed with reasons;
- consequential architecture decisions are settled or named blockers;
- prior findings map to controls and executable proofs;
- every phase has observable exit evidence and failure-path coverage;
- promotion states distinguish local, live, deployed, security, and delivery evidence;
- gaps remain visible rather than being averaged into a general readiness claim.
