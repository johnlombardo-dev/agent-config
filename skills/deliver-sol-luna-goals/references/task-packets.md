# Luna task packets

This reference owns Luna profile selection and packet schemas only. Dispatch validity, defined terms, and precedence remain governed by the parent `SKILL.md`.

## Profile selection

**Compact** is the default Luna profile for one bounded, independently reviewable outcome using only the core contract sections below.

**Full** is Compact plus only the risk-specific additions needed when the task changes a public boundary, security or data behavior, migration or deletion, several integration seams, a known red baseline inside its Failure Domain, or another invariant governed by a Consequential Decision.

If the Full additions make the task incoherent, split it rather than expanding the contract.

## Compact contract

```text
GOAL
One independently reviewable outcome.

STATE
Relevant fingerprint and accepted facts. Include only verification that does not change a Consequential Decision; unresolved decisions remain with Sol.

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

## Full additions

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
