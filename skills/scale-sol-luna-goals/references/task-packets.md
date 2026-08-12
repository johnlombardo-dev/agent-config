# Task packets

Read the relevant section only when preparing that dispatch.

This reference owns assignment schemas and Luna profile selection only. Dispatch validity, defined terms, and precedence remain governed by the parent `SKILL.md`.

## Contents

- [Sol contract-writer assignment](#sol-contract-writer-assignment)
- [Retained writers and evidence review](#retained-writers-and-evidence-review)
- [Review-phase xhigh contract-writer profile](#review-phase-xhigh-contract-writer-profile)
- [Luna contract selection](#luna-contract-selection)
- [Compact Luna contract](#compact-luna-contract)
- [Full Luna additions](#full-luna-additions)
- [Parent dispatch record](#parent-dispatch-record)

## Sol contract-writer assignment

```text
PROBLEM: one bounded question or contract space
STATE: fingerprint plus relevant KNOWN, VERIFY, UNKNOWN, and AVOID facts
PRIOR: omit for a fresh writer; for resumption, prior task/fingerprint, selected reusable findings, material delta, and required revalidation
AUTHORITY: required sources and precedence; read scope; mutation scope, normally none
NESTED RESEARCH: none, or depth 1 plus child count, model/capability, read scope, and cost limit
STOP: invalid assumptions, evidence gap, scope boundary, cost limit, or prerequisite
RETURN: GO, NO-GO, or PREREQUISITE; decision delta, evidence/confidence, next contract or reason none, successor/blocker
```

`PRIOR` never substitutes for current `STATE`, `AUTHORITY`, `STOP`, or `RETURN`. A resumed writer receives a new assignment and may rely only on the selected findings after the required revalidation.

The orchestrator dispatches contract writers. A contract writer using the review-phase `xhigh` profile may dispatch the required local reviewer only under the review schema below. A writer may separately dispatch a research child only when the assignment explicitly grants it and:

- The child owns one objectively answerable, read-only question.
- The child makes no decision, writes no contract or implementation, and cannot dispatch another agent.
- Passing the question requires substantially less context than doing the research directly.
- One child is preferred; fanout requires independent questions and non-duplicated evidence ownership.
- The writer owns synthesis and returns only the decision-relevant result and evidence pointer.

Return the shortest sufficient response. Include technical detail that affects a decision; omit raw logs, source digests, dead ends, and repeated accepted facts. Put necessary long analysis in an explicitly authorized shared session artifact, never an unrequested repository file.

## Retained writers and evidence review

Keep this optional retained-writer entry in the parent goal ledger, not in the writer prompt:

```text
RETAINED: writer ID and domain; last task/state fingerprint; selected evidence pointer and invalidation trigger; one anticipated next use
```

Reassess the entry at the next framing checkpoint. Resume only when the new assignment is valid and Worth. Otherwise close the writer, including when state or authority drift makes its context unreliable, the required runtime route is unavailable, or the domain is complete.

Shape independent evidence review through the same Sol assignment schema. Bound `PROBLEM` to exact claims and their intended downstream use; make `AUTHORITY` read-only and name the governing sources. Use final `GO` only when every reviewed claim has a `supported`, `qualified`, `rejected`, or `duplicate` disposition with evidence, applicability limits, and invalidation triggers. Return `PREREQUISITE` for missing authority, unresolved conflicts, or material drift. The orchestrator decides which supported or qualified claims enter current `KNOWN` or `VERIFY` state.

## Review-phase xhigh contract-writer profile

Use this schema only for a cycle governed by [review-convergence.md](review-convergence.md):

```text
STAGE: local or hosted-pr; cycle ID; exact base and head; review source
SOURCE: local merge target and head, or hosted PR/review pointer and exact reviewed head
STATE: relevant fingerprint, accepted decisions, prior cycle delta, owned dirty state, and known checks
AUTHORITY: governing sources and precedence; repository read scope; mutation limited to one external JSONL stack
REVIEWER CHILD: local requires one fresh Sol xhigh child using review-agent; hosted-pr normally none because the writer reads the hosted source directly
NESTED RESEARCH: none, or depth 1 plus child count, exact question/read scope, capability, and cost limit
STACK: assigned path, prior tail fingerprint, and append-only entry types permitted
STOP: stale head, incomplete findings, authority conflict, consequential decision, unsafe ownership overlap, or unavailable exact route
RETURN: GO, NO-GO, or PREREQUISITE; normalized finding index and dispositions; proposed Luna contracts; dependency/conflict graph; manifest; residual risks; stack pointer
```

For a local cycle, require the writer to spawn a fresh reviewer with only the exact review target, applicable instructions, and the `review-agent` skill. The reviewer cannot inherit candidate dispositions or prior review conclusions. For a hosted cycle, give the writer the PR and exact-head review pointer; the writer reads every actionable hosted finding directly. Use research children only when the existing dispatch test makes them Worth.

Normalize and append every finding before shaping contracts. The writer must then examine related findings, combine those that share an inseparable Failure Domain, and split those with independently acceptable mutation and rollback surfaces. Every proposed contract must use the Luna Compact or Full schema below and name finding IDs, dependencies, conflicts, mutation ownership, checks, and a split trigger. Persistence records candidate dispositions and proposals, not acceptance. The orchestrator accepts, rejects, schedules, and appends state transitions.

## Luna contract selection

**Compact** is the default Luna profile for one bounded, independently reviewable outcome using only the core contract sections below.

**Full** is Compact plus only the risk-specific additions needed when the task changes a public boundary, security or data behavior, migration or deletion, several integration seams, a known red baseline inside its Failure Domain, or another invariant governed by a Consequential Decision.

If the Full additions make the task incoherent, split it rather than expanding the contract.

## Compact Luna contract

```text
GOAL
One independently reviewable outcome.

STATE
Relevant fingerprint, KNOWN facts, and AVOID facts. Include only verification that does not change a Consequential Decision; unresolved decisions remain with the orchestrator.

AUTHORITY
Read: sources Luna may inspect.
Mutate: exact files, data, or actions Luna may change; protected and concurrently owned areas.

DECISIONS AND CONSTRAINTS
Frozen interfaces, behavior, policy, and invariants.

DONE WHEN
Cheapest faithful checks and required artifacts.

STOP AND RETURN
False assumptions, scope or decision changes, ownership conflicts, or evidence outside authority.

HANDOFF
Shortest sufficient summary; artifacts; commands with concise results; deviations and unresolved risks.
```

## Full Luna additions

Add only the sections required by risk:

```text
RISKS AND CASES
Relevant invariants, hostile inputs, rollback boundaries, or failure cases.

BASELINE
Relevant known failures before the task; evidence pointer instead of full logs.

INTEGRATION RATCHET
Cheapest check that detects a new failure in the owned blast radius.

RETIREMENT ACCOUNTING
Artifacts removed, moved, renamed, or replaced; callers/evidence preserved; focused reference scan.
```

## Parent dispatch record

Keep this in the goal ledger and omit it from the Luna prompt:

```text
TASK: ID, profile, outcome/Failure Domain, split trigger
ROUTE: logical role, current runtime mapping, effort, context fork, verification evidence
OWNERSHIP: mutation reservation and concurrent tasks
REVIEW: why independent verification is or is not required
```
