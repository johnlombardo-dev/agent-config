# Review convergence

Read this reference when pull-request delivery is part of the authorized goal. It owns review-stage mechanics, the external review-contract stack, and the returned manifest only. Role authority, dispatch validity, Luna schemas, runtime mappings, and metrics remain owned by their parent sources.

## Preconditions and authority

- Enter review convergence only after the implementation candidate is integrated and its proportionate owning checks pass.
- Open, publish, update, or mark a pull request ready only when the user goal authorizes those external mutations. Otherwise run any authorized local review, report `requires-new-authority`, and leave the hosted gate pending.
- Resolve the intended base branch, merge base, exact head, dirty state, required CI, configured hosted reviewer, and applicable repository instructions before the first cycle.
- Use one reusable cycle below. The local gate supplies findings from a fresh `review-agent`; the hosted gate supplies findings from the GitHub review bot.
- Review-contract stack persistence is authorized by this skill only while review convergence is active.

## Review-contract stack

Persist review contracts outside repositories and worktrees at:

```text
~/.codex/subagent-contracts/scale-sol-luna-goals/<host>/<owner>/<repository>/<skill-use-id>/<stage>.jsonl
```

Treat the stack as a redacted, reconstructible, non-authoritative coordination cache. Never store secrets, credentials, raw reasoning, or unbounded logs. Use append-only entries:

```text
review_cycle: cycle_id, stage, source, base, head, finding IDs and severity counts
finding: finding_id, cycle_id, source ID/URL, severity, title, path/range, affected scenario, evidence, candidate disposition, related finding IDs
contract: contract_id, cycle_id, finding_ids, profile, Failure Domain, mutation scope, depends_on, conflicts_with, checks, full proposed Luna packet, status=proposed
decision: finding|contract, target_id, accepted|rejected|superseded, reason, orchestrator fingerprint
result: contract_id, landed|no-change|failed|aborted, evidence, resulting head, rework attribution
cycle_outcome: cycle_id, clean|findings|stale|blocked, unresolved IDs, checks, resulting head
```

The stack is an event log, not a LIFO scheduler. Dispatch order comes only from orchestrator-accepted dependencies, conflicts, and mutation reservations in the current manifest.

Give the contract writer using the review-phase `xhigh` profile temporary ownership to append only `review_cycle`, normalized `finding`, and proposed `contract` entries to the assigned file. After it returns, transfer stack ownership to the orchestrator for decisions, results, and cycle outcome. Luna workers and reviewers never write the stack. Missing or corrupt stack state is a cache miss; reconstruct from Git, hosted review evidence, and accepted contracts.

The writer returns a compact manifest containing the cycle and exact head, every finding ID and candidate disposition, finding counts, contract IDs, Luna profiles, mutation scopes, dependencies, conflicts, ready and blocked sets, residual risks, and the stack pointer. The manifest is an index, not a second copy of findings or packets.

## One review cycle

1. Fingerprint the exact base, head, dirty state, accepted decisions, review source, and prior cycle delta.
2. Dispatch a Sol `xhigh` contract writer using the review-phase profile in [task-packets.md](task-packets.md).
3. For a local cycle, the writer spawns one fresh Sol `xhigh` reviewer using `review-agent`. For a hosted cycle, it reads every actionable finding directly from the exact PR review pointer and may dispatch only Worth, depth-one read-only research.
4. The writer normalizes and appends every finding, proposes dispositions, analyzes related and dependent work, appends proposed Luna packets, and returns the manifest.
5. The orchestrator rechecks authority and drift, accepts or rejects proposals, reserves mutation surfaces, and dispatches only a dependency-ready set whose Failure Domains are independently acceptable and non-overlapping.
6. Integrate settled work, append results, run focused checks, and invalidate stale contracts. Run broad gates only at convergence checkpoints, not after every worker.
7. Start a new cycle at the resulting exact head. Never infer cleanliness from the prior review.

Do not create one contract per finding mechanically. Combine findings when partial fixes could leave one behavior inconsistent; separate them when ownership, checks, and rollback are independent. If the same Failure Domain reopens twice, a fix expands the dependent failure surface, or safe concurrency becomes unclear, stop fanout and send one bounded system-level shaping assignment back to the orchestrator.

## Local gate

Open or reuse a draft pull request when authorized so the merge target and CI surface are explicit. Repeat local cycles until the fresh reviewer returns `No findings.` for the exact head. Then run the required broad local/CI-equivalent gates. Advance only when the no-findings result is current and those checks are green; mark the pull request ready for review only after this gate.

## Hosted PR gate

Wait for the configured Codex GitHub review bot's completed review of the exact ready-for-review head. Give its PR, review, and exact-head pointers to a Sol `xhigh` contract writer using the hosted review-phase profile; the writer reads the findings directly. Execute accepted contracts through the same dependency-aware cycle, push the integrated head, and request or await a new exact-head review. Resolve a thread only after its accepted contract evidence is integrated. Adjudicate rejected or contract-conflicting findings explicitly; do not silently discard or resolve them.

Complete the hosted gate only when all of these describe the same exact head:

- the hosted reviewer reports no actionable findings;
- every required CI check is green;
- no review thread remains unresolved; and
- the goal has no other required work.

A stale review, reviewer reaction without a completed result, green CI on another head, or a locally clean cycle cannot satisfy this gate.
