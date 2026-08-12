# Runtime routing

Read this before model-specific dispatch. Treat logical roles as stable and the concrete mapping as current installation detail that must be checked against the active tool surface.

This reference owns logical-to-runtime mappings and degraded-capability behavior only. Dispatch validity, defined terms, and precedence remain governed by the parent `SKILL.md`.

## Logical roles

- **Contract writer:** high-capability model for bounded research, synthesis, tradeoffs, and contract shaping.
- **Local reviewer:** fresh read-only model that applies the installed `review-agent` skill to one exact branch target.
- **Research assistant:** lowest adequate model for one read-only, objectively answerable question.
- **Execution worker:** bounded implementation model operating from frozen decisions and executable checks.

## Current mapping

### Contract writer

- Map to GPT-5.6 Sol with callable `high` or `xhigh` effort.
- Use `high` for contract writing.
- Use `xhigh` only when an otherwise valid, bounded assignment has a correctness-critical interaction among states or time, authority boundaries, failure/recovery paths, or public consumers, and splitting would prevent faithful adjudication of that interaction.
- A topic label such as state machine, migration, persistence, concurrency, or public API does not independently qualify for `xhigh`.
- Use `fork_turns = "none"` or a positive bounded count and provide the explicit task-local source pack.
- Verify effective model and effort from parent-visible runtime evidence when available.
- Require a resumed writer to satisfy the new assignment's current route. Resumption does not verify or preserve model or effort. If the retained runtime cannot provide the required verified route, dispatch fresh or keep the assignment pending.

### Review-phase profile

- Map both the contract writer using this profile and the local reviewer to GPT-5.6 Sol with verified `xhigh` effort.
- Give each a `fork_turns = "none"` or a positive bounded count and an explicit task-local source pack.
- Require the contract writer to spawn a fresh local reviewer for every local cycle. The reviewer must invoke the installed `review-agent` skill, inspect the exact merge-base diff, remain read-only, and return all actionable findings or `No findings.`
- Do not substitute the contract writer's own inspection for the required independent local reviewer. The writer owns finding normalization and disposition, related-work analysis, contract shaping, and the manifest.
- Hosted PR findings come from the configured Codex GitHub review bot. Do not spawn a duplicate local reviewer inside the hosted cycle unless new evidence makes a separate independent review Worth.
- Treat an unavailable or unverified exact Sol xhigh route, missing `review-agent` skill, stale hosted review, or unavailable hosted reviewer as a capability gap. Keep the review gate pending rather than silently lowering effort or changing model class.

### Execution worker

- Map to the named `luna_worker` agent type, whose active configuration must pin `gpt-5.6-luna`.
- Do not pass a direct Luna model override when the client rejects that route.
- Pass the selected task effort with a `none` or positive bounded context fork when the worker must differ from the parent.
- Never ask Luna to verify or report its own runtime metadata.

Use the lowest adequate Luna effort:

| Work | Effort |
| --- | --- |
| Exact transformation or mechanical check | `low` |
| Several local steps without strategic decisions | `medium` |
| Branchy logic or edge-case-heavy regression work | `high` |
| Exceptionally demanding but still fully bounded work | `xhigh` |

## Degraded capability

- Never claim a model or effort that cannot be verified.
- Record model or effort as unknown when parent-visible verification evidence is unavailable.
- Treat an unverified exact route as unavailable whenever the user or task requires that route.
- When the user's route requires exact Sol or Luna and it is unavailable, continue safe research, shaping, review, or other independent work; keep execution pending and report the capability gap.
- Use an alternative model only after an explicit orchestrator decision permitted by the user and state the new assignment. Never silently substitute Terra or another model.
- If ordinary instructions authorize direct execution and orchestration would cost more, exit the specialized route instead of pretending the work was Luna execution.

## Failure remediation

Do not treat higher effort as a cure for an oversized or ambiguous task. On failure:

1. Separate contract ambiguity, implementation error, and environmental failure.
2. Split or reduce the task when its outcome or Failure Domain is too broad.
3. Retry only when the contract remains valid and evidence supports another attempt.
4. Consider another model class only after reshaping and an explicit routing decision.
