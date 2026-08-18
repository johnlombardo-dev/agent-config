# Sol task packets

Read the relevant section only when preparing that dispatch.

This reference owns Sol writer and evidence-check assignment schemas only. Dispatch validity, defined terms, and precedence remain governed by the parent `SKILL.md`. Use the sibling `shape-luna-contract` skill for next-dispatch Luna decomposition and worker contracts.

## Contents

- [Sol contract-writer assignment](#sol-contract-writer-assignment)
- [Retained writers and evidence checks](#retained-writers-and-evidence-checks)

## Sol contract-writer assignment

```text
PROBLEM: one bounded question or contract space
STATE: fingerprint plus relevant KNOWN, VERIFY, UNKNOWN, and AVOID facts
PRIOR: omit for a fresh writer; for resumption, prior task/fingerprint, selected reusable findings, material delta, and required revalidation
AUTHORITY: required sources and precedence; read scope; mutation scope, normally none
NESTED RESEARCH: none, or depth 1 plus child count, model/capability, read scope, and cost limit
SHAPING: none, or $shape-luna-contract at the orchestrator-resolved skill path after research
STOP: invalid assumptions, evidence gap, scope boundary, cost limit, or prerequisite
RETURN: MODE, STATUS, decision delta, evidence/confidence, result payload, successor/blocker
```

`PRIOR` never substitutes for current `STATE`, `AUTHORITY`, `STOP`, or `RETURN`. A resumed writer receives a new assignment and may rely only on the selected findings after the required revalidation.

Use exactly one return envelope:

```text
MODE: research or shaped
STATUS: mode-specific terminal status
DECISION DELTA: proposed decision change or none
EVIDENCE: decisive pointers, applicability, and confidence
RESULT: research finding, shaped contract, escalation, exact prerequisite, or no-op evidence
NEXT: at most one provisional successor, blocker, or none
```

When `SHAPING` is `none`, use `MODE: research` and `STATUS: GO`, `NO-GO`, or `PREREQUISITE`.
When `SHAPING` names the standalone skill, use `MODE: shaped` and `STATUS: READY`, `ESCALATE`,
`PREREQUISITE`, or `NO-OP`. Research may precede shaping, but it does not wrap or rename the final
shaper status. An early viability failure becomes an exact shaped-mode `PREREQUISITE`, or `NO-OP`
when evidence proves no implementation outcome remains.

When `SHAPING` is required, include the standalone skill's current path in `AUTHORITY` and explicitly invoke it in the writer assignment. The writer may research first within its granted budget, then must read and apply the skill completely to exactly one next-dispatch outcome. It returns the shaped envelope as a proposal. The orchestrator still owns contract acceptance, route selection, dispatch, integration, and replanning.

The orchestrator dispatches contract writers. A writer may dispatch a research child when the orchestrator records a depth-one budget in the assignment. This is internal assignment scope, not a separate user-authorization gate. Require all of the following:

- The child owns one objectively answerable, read-only question.
- The child makes no decision, writes no contract or implementation, and cannot dispatch another agent.
- Passing the question requires substantially less context than doing the research directly.
- One child is preferred; fanout requires independent questions and non-duplicated evidence ownership.
- The writer owns synthesis and returns only the decision-relevant result and evidence pointer.

Return the shortest sufficient response. Include technical detail that affects a decision; omit raw logs, source digests, dead ends, and repeated accepted facts. Put necessary long analysis in the external artifact path authorized by the parent skill, never in an unrequested repository file.

## Retained writers and evidence checks

Keep this retained-writer entry in the parent goal ledger whenever the parent reuse rule retains a writer. Do not put it in the writer prompt:

```text
RETAINED: writer ID and domain; last task/state fingerprint; selected evidence pointer and invalidation trigger; one anticipated next use
```

Reassess the entry at the next framing checkpoint. Resume only when the new assignment is valid and Worth. Otherwise close the writer, including when state or authority drift makes its context unreliable, the required runtime route is unavailable, or the domain is complete.

Shape an independent evidence check through the same Sol assignment schema. Bound `PROBLEM` to exact claims and their intended downstream use; make `AUTHORITY` read-only and name the governing sources. Use final `GO` only when every checked claim has a `supported`, `qualified`, `rejected`, or `duplicate` disposition with evidence, applicability limits, and invalidation triggers. Return `PREREQUISITE` for missing authority, unresolved conflicts, or material drift. The orchestrator decides which supported or qualified claims enter current `KNOWN` or `VERIFY` state.
