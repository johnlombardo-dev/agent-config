---
name: evidence-first-review
description: >-
  Review a code change or existing system by mapping behavioral seams, selecting
  only the applicable defect-finding lanes, and requiring executable evidence
  where the risk can be exercised. Use for code review, regression hunts,
  pre-merge audits, large integrated changes, or system-wide bug hunts across
  UI, backend, storage, security, workflows, protocols, performance, and
  operations.
---

# Evidence-first review

Find and batch demonstrated defects before anyone starts repairing them.

## Set the target

Choose one mode and record it in the result.

- **Change mode:** review the exact diff, its changed behavior, and adjacent consumers. Classify findings as introduced, pre-existing, fix-induced, or unknown.
- **System mode:** review a named behavior or subsystem without limiting findings to one diff. Do not describe a defect as introduced unless history proves it.

Freeze the target fingerprint, repository instructions, allowed tools, time or token budget, and checks that may run. Treat dirty state as part of the target. Review read-only. Do not implement fixes, change Git or PR state, or write metrics.

## Build the target manifest

Before reading line by line, map:

- the claimed behavior and its owning boundary;
- changed files, generated artifacts, dependencies, configuration, and documentation;
- direct consumers, equivalent entrypoints, durable state, external systems, and deployment surfaces;
- modes, events, guards, effects, retries, cancellation, cleanup, scale limits, and trust boundaries;
- relevant tests, acceptance criteria, and prior demonstrated failures.

Use the manifest to route the review. A path or keyword alone is a locator, not evidence that a lane applies.
Give each manifested seam an owning lane, distinct invariants, and an evidence status: `exercised`, `gap`, or `not applicable`. A finding settles only its violated invariant; continue through the rest. Do not call a lane complete until every owned invariant has a status and reason.

## Route only applicable lanes

Select a lane immediately when the target directly changes its owning boundary, the acceptance criteria explicitly name its risk, or a prior demonstrated defect exists at the same seam. Otherwise select it only when two independent signal groups agree: a risky construct, an affected consumer or contract, failure or scale behavior, and a technology or path marker.

Read only the playbooks for selected lanes:

1. **Domain and value integrity:** canonical identity, transformations, calculations, business rules, routing, and round trips. Read [domain-value-integrity.md](references/lanes/domain-value-integrity.md).
2. **Accessibility and interaction:** rendered controls, focus, keyboard, pointer, portals, names, and states. Read [accessibility-interaction.md](references/lanes/accessibility-interaction.md).
3. **Public contract:** exports, schemas, API and CLI shapes, runtime guards, packages, and compatibility. Read [public-contract.md](references/lanes/public-contract.md).
4. **Lifecycle and resource ownership:** acquisition, cleanup, streams, handles, observers, subscriptions, and mount or start/stop behavior. Read [lifecycle-resource-ownership.md](references/lanes/lifecycle-resource-ownership.md).
5. **Security, privacy, and trust:** authentication, authorization, secrets, untrusted data, sensitive output, and filesystem or network boundaries. Read [security-privacy-trust.md](references/lanes/security-privacy-trust.md).
6. **Persistence, migration, and recovery:** schemas, transactions, indexes, checkpoints, backups, atomic files, crashes, and restarts. Read [persistence-migration-recovery.md](references/lanes/persistence-migration-recovery.md).
7. **Concurrency, workflow, and ordering:** locks, queues, actors, retries, cancellation, idempotency, races, and partial failures. Read [concurrency-workflow-ordering.md](references/lanes/concurrency-workflow-ordering.md).
8. **Performance, capacity, and backpressure:** unbounded inputs, buffering, queries, batching, pagination, caches, and resource ceilings. Read [performance-capacity-backpressure.md](references/lanes/performance-capacity-backpressure.md).
9. **External protocol and integration:** vendor APIs, SDK runtime behavior, wire protocols, capabilities, parsers, and fallbacks. Read [external-protocol-integration.md](references/lanes/external-protocol-integration.md).
10. **Operations, configuration, and deployment:** ports, paths, environment, service managers, CI, build, release, and documentation parity. Read [operations-configuration-deployment.md](references/lanes/operations-configuration-deployment.md).

Run selected lanes independently. Do not select a lane merely to be comprehensive. More than three lanes requires a concrete cross-cutting justification. Selecting all lanes is appropriate only for an explicitly broad system or release audit whose manifest demonstrates every surface.

A running lane may escalate to another lane only after identifying a concrete seam owned there. Record the evidence for the escalation. Read [evidence-techniques.md](references/evidence-techniques.md) once after routing, then choose the cheapest faithful probes. A passing broad suite is context, not proof of an uncovered interaction.

## Keep only demonstrated findings

Keep a finding only when it has all of these:

- an owning lane and a violated invariant or user-visible failure;
- a minimal reproduction, executable probe, or direct source proof;
- a narrow location and affected behavior;
- a severity and provenance classification;
- enough evidence that an implementer can verify the repair.

Do not repair while lanes are active. Deduplicate after every selected lane returns, then publish one batch.

## Report

Return:

```text
TARGET: mode, fingerprint, budget, checks run
MANIFEST: seam, owner, invariant, durable/external/operational surfaces, evidence status + reason
ROUTING: selected lane + triggers; skipped lane + reason; escalations
FINDINGS: lane, severity, provenance, invariant, reproduction, location, evidence
GAPS: manifested invariants marked gap and the missing evidence
RESULT: findings | no confirmed findings
```

Write `no confirmed findings`, never `clean` or `proved correct`. Stop after this batch. A later repair belongs to `verify-repair-seam`, not another whole-target pass.

This skill does not own implementation, repair scheduling, Git delivery, hosted review, merge decisions, or persistence.
