# Runtime routing

Read this before model-specific dispatch. Treat the logical role as stable and the concrete mapping as current installation detail that must be checked against the active tool surface.

This reference owns logical-to-runtime mappings and degraded-capability behavior only. Dispatch validity, defined terms, and precedence remain governed by the parent `SKILL.md`.

## Logical role

The execution worker is a bounded implementation model operating from frozen decisions and executable checks.

## Current mapping

- Map execution to the named `luna_worker` agent type, whose active configuration must pin `gpt-5.6-luna`.
- Do not pass a direct Luna model override when the client rejects that route.
- Pass the selected task effort with a `none` or positive bounded context fork when the worker must differ from the parent.
- Never ask Luna to verify or report its own runtime metadata.

Use the lowest adequate effort:

| Work | Effort |
| --- | --- |
| Exact transformation or mechanical check | `low` |
| Several local steps without strategic decisions | `medium` |
| Branchy logic or edge-case-heavy regression work | `high` |
| Exceptionally demanding but still fully bounded work | `xhigh` |

## Degraded capability

- Never claim a model or effort that cannot be verified.
- Treat an unverified exact route as unavailable whenever the user or task requires that route.
- When the user's route requires exact Luna and it is unavailable, continue safe research, shaping, review, or other independent work; keep execution pending and report the capability gap.
- Use an alternative model only after an explicit Sol decision permitted by the user and state the new assignment. Never silently substitute Terra or another model.
- If ordinary instructions authorize direct execution and orchestration would cost more, exit the specialized route instead of pretending the work was Luna execution.

## Failure remediation

Do not treat higher effort as a cure for an oversized or ambiguous task. On failure:

1. Separate contract ambiguity, implementation error, and environmental failure.
2. Split or reduce the task when its outcome or Failure Domain is too broad.
3. Retry only when the contract remains valid and evidence supports another attempt.
4. Consider another model class only after reshaping and an explicit routing decision.
