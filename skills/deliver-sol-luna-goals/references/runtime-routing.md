# Runtime routing

Read this before model-specific dispatch. Treat the logical role as stable and the concrete mapping as current installation detail that must be checked against the active tool surface.

This reference owns logical-to-runtime mappings and degraded-capability behavior only. Dispatch validity, defined terms, and precedence remain governed by the parent `SKILL.md`.

## Logical roles

- **Execution worker:** bounded implementation model operating from frozen decisions and executable checks.
- **High-capability implementer:** highest-capability model with independently selected `high`,
  `xhigh`, or `max` effort for an
  indivisible `ESCALATE` outcome that must not be delegated to Luna.

## Current mapping

### Execution worker

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

### High-capability implementer

- Map to GPT-5.6 Sol with `high`, `xhigh`, or `max` effort when the selected exact route is callable
  and parent-verifiable.
- Never use `ultra` for this route.
- Use `high` only to implement a fully frozen state-chart as faithful translation with bounded
  checks and no protocol design.
- Use `xhigh` by default to design or semantically verify a state-chart or materially change its
  protocol.
- Use `max` only for a named irreducible interaction across nested or parallel states, multiple
  actors, time, cancellation, retry or recovery, persistence, authority, security, migration, or
  public consumers. A state-chart label or task size alone does not qualify.
- When selecting `max`, record the trigger and why `xhigh` is insufficient. Do not use `max` when it
  is likely to reopen frozen decisions, expand scope, or encourage speculative redesign.
- Preserve design and implementation ownership together when the escalation says separating them
  would break the invariant.
- State-chart design or implementation is a hard member of this route. Luna may handle adjacent
  mechanical work only when it does not alter states, events, transitions, guards, actions,
  actors, context ownership, persistence, cancellation, or lifecycle semantics.
- If the selected exact route is unavailable, keep the outcome pending. Do not silently substitute
  another model, another effort, or a set of Luna contracts.

## Degraded capability

- Never claim a model or effort that cannot be verified.
- Treat an unverified exact route as unavailable whenever the user or task requires that route.
- Treat every `ESCALATE` outcome as requiring an exact verified high-capability route.
- When the user's route requires exact Luna and it is unavailable, continue safe research, shaping, review, or other independent work; keep execution pending and report the capability gap.
- Use an alternative model only after an explicit Sol decision permitted by the user and state the new assignment. Never silently substitute Terra or another model.
- If ordinary instructions authorize direct execution and orchestration would cost more, exit the specialized route instead of pretending the work was Luna execution.

## Failure remediation

Do not treat higher effort as a cure for an oversized or ambiguous task. On failure:

1. Separate contract ambiguity, implementation error, and environmental failure.
2. Split or reduce the task when its outcome or Failure Domain is too broad.
3. Retry only when the contract remains valid and evidence supports another attempt.
4. Consider another model class only after reshaping and an explicit routing decision.
