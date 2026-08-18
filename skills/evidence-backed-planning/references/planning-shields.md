# Planning shields learned from compared implementations and escaped defects

These shields generalize beyond any one product. Route each shield as `required`, `not applicable`, or `gap`; do not add it mechanically when the project has no owning seam.

## S01: Evidence provenance and precedence

Freeze source identity, repository state, date, claim, and limitation. Define how conflicts are resolved. Demonstrated failures outrank green broad suites. Current decisions outrank prototype defaults. Token use, elapsed time, file counts, and test counts are context, not quality verdicts.

## S02: Behavioral-seam manifest

Map the user-visible behavior and its owners before splitting phases. Include public entrypoints, durable state, external effects, state/workflow, cancellation, cleanup, trust boundaries, scale limits, recovery, operations, documentation, and delivery where applicable. A path list is not a behavior map.

## S03: Write/read and transformation closure

For every accepted write, prove the value survives validation, transformation, persistence, retrieval, rendering or serialization, restart, and migration. Include narrowed domains, missing/empty values, and direct versus composed callers.

## S04: Effect/persistence/recovery closure

When an external effect and local record cannot commit atomically, model the uncertainty. Persist intent and attempts, inject failure after the effect but before the record, restart, reconcile, and prove retry does not blindly duplicate the effect.

## S05: Workflow truth and control/state closure

Name modes, events, guards, effects, retries, cancellation, and cleanup. A public control reports success only after observing the owning workflow's accepted transition. States must describe active work, not labels emitted before or after hidden work.

## S06: Full recovery closure

Define the complete recoverable product, not only the primary database. Include blobs, indexes or rebuild inputs, metadata, configuration, audit history, and secrets policy as applicable. Restore into an empty target and exercise public behavior.

## S07: Duplicated-path parity

Inventory direct/composed, existing/future, API/CLI/UI, storage/route, sync/async, local/remote, and actor/status paths. For applicable pairs, define one matrix covering values, errors, empty/not-found semantics, permissions, state reporting, streaming, and round trips.

## S08: Production-faithful test boundaries

Make fakes obey production shapes, optionality, normal completion, errors, cancellation, ordering, backpressure, and cleanup. Run one adapter contract against fake and production boundary when safe. Confirm installed SDK or protocol behavior rather than relying on fields invented by the fake.

## S09: Capacity and backpressure inventory

Test the boundaries that grow: sparse identifiers, large individual records, large total datasets, selected subsets, pagination, journals, slow consumers, whole-response timeouts, retries, caches, and queues. Measure at the public boundary and retain hardware/runtime/fixture fingerprints.

## S10: Trust and authority closure

Identify untrusted input, secrets, identity provenance, public versus internal capabilities, replay, expiry, tampering, least authority, sensitive output, logging, filesystem, and network boundaries. A partial security review stays an explicit gap.

## S11: Outcome-based operations and usability

Define operations by postconditions: data restored, service absent, health diagnosis preserved, exact configuration active, permissions correct, rollback possible. Walk the README against runnable commands. Repository history and reproducible setup are part of maintainability evidence.

## S12: Evidence-tiered promotion and delivery

Keep evidence states separate:

- `specified`: requirement and proof are defined;
- `implemented`: source exists, proof not yet passed;
- `locally verified`: required static, isolated, composed, and capacity gates pass;
- `live verified`: authorized external behavior passes;
- `deployed verified`: target operations and recovery pass;
- `security reviewed`: the declared security scope passes with gaps stated;
- `delivered`: exact intended commit is present on the named remote or release channel;
- `release-ready`: every applicable promotion gate passes and no required gap is hidden.

One state never implies another.

## Structural encoding matrix

For each recurring lesson, select the strongest available carrier:

| Strength | Carrier | Example |
|---|---|---|
| 1 | Type/schema | Invalid lifecycle combinations cannot be constructed. |
| 2 | Lint/policy | A dangerous API or dependency direction fails CI. |
| 3 | Canonical boundary | All consumers share one parser, contract, or transition function. |
| 4 | Runtime invariant | Startup, migration, or mutation fails closed on invalid durable state. |
| 5 | Executable outcome probe | Failure injection, parity, capacity, restore, or operations postcondition. |
| 6 | Decision prose | A judgment-heavy rule includes its evidence and counterexample. |

Do not keep a repeated instruction when a stronger structural carrier is practical.

