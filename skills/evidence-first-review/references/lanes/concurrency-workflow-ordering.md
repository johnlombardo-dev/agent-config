# Concurrency, workflow, and ordering

## Select when

The target coordinates async tasks, queues, actors, locks, claims, retries, cancellation, timeouts, idempotency, partial results, or state transitions.

## Review

- Write explicit states, events, guards, effects, and ownership before testing paths.
- Cover simultaneous starts, duplicate delivery, stale work, reordered completion, cancellation at each await, retry after partial success, and restart from durable state.
- Verify claims and preconditions become authoritative before external effects.
- Prove queues serialize only what must serialize, locks always release, late results cannot overwrite newer state, and retries do not repeat completed effects.
- Check every failure classification and terminal outcome, including cleanup failure.

## Evidence

Use barriers, deterministic schedulers, fake clocks, abort injection, duplicate events, and state-path coverage. Escalate to persistence when workflow truth survives restart or lifecycle when child resources outlive their owner.
