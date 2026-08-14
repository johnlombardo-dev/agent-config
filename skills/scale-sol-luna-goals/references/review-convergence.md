# Review convergence

Read this reference for every skill invocation that produces implementation changes. It owns review-stage mechanics, the external review-contract stack, and the returned manifest only. Role authority, delivery modes, dispatch validity, Luna schemas, runtime mappings, and metrics remain owned by their parent sources.

## Preconditions and authority

- Enter review convergence only after the implementation candidate is integrated and its proportionate owning checks pass.
- Apply the delivery mode selected by the parent skill. Default authority includes the Git and GitHub mutations required by that mode.
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

Repeat local cycles until the fresh reviewer returns `No findings.` for the exact candidate and the required broad local or CI-equivalent gates pass. A code change invalidates that result and requires a fresh cycle.

For no-PR mode, include the exact merge base, head, and declared dirty state in the candidate fingerprint, then stop after this gate. Do not push, create a pull request, run hosted review, or merge.

For every other mode, create or update a draft pull request with the exact local-clean head. Mark it ready before hosted review unless draft-PR mode applies.

## Hosted PR gate

For a ready pull request, wait for the configured Codex GitHub review bot's completed review. For a draft pull request, add a top-level comment containing exactly `@codex review` and wait for the completed review without marking the pull request ready. Give the PR, review, and exact-head pointers to a Sol `xhigh` contract writer using the hosted review-phase profile; the writer reads the findings directly.

Execute accepted contracts through the same dependency-aware cycle. Any code change invalidates the local gate: rerun it, push the new head, then request or await a new exact-head hosted review. In draft-PR mode, add a new top-level `@codex review` comment after each such push. Resolve a thread only after its accepted contract evidence is integrated. Adjudicate rejected or contract-conflicting findings explicitly; do not silently discard or resolve them.

Complete the hosted gate only when all of these describe the same exact head:

- the hosted reviewer reports no actionable findings;
- the local `No findings.` result covers the same head;
- every required CI check is green;
- no review thread remains unresolved; and
- the goal has no other required work.

A stale review, reviewer reaction without a completed result, green CI on another head, or a locally clean cycle cannot satisfy this gate.

## Merge gate

After the hosted gate passes, leave the pull request open when merge is forbidden. Otherwise mark a draft pull request ready, merge with the repository's required or default method, and verify that the merged commit contains the exact reviewed head. Do not report completion while the merge is queued, blocked, or incomplete.
