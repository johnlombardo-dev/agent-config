# Shared evidence techniques

Read this once after routing. Read only the selected lane playbooks.

## Evidence order

Start with the cheapest faithful proof: direct source proof, type or schema fixture, focused unit test, deterministic integration test, browser or external-system probe, then a broader gate. Decide each manifested invariant, then continue until all are `exercised`, `gap`, or `not applicable`.

## Reusable methods

- Build a closure matrix when one fact or operation crosses validators, writers, effects, durable state, serializers, readers, documentation, or deployment configuration.
- For a state-changing seam, trace accepted input through its durable or external effect to the observable read. Inject failure between non-atomic steps and prove retry or restart reaches one correct outcome.
- Treat a fake, stub, or recorded fixture as evidence only after comparing its material success, absence, failure, completion, timing, and mutation semantics with production. Otherwise probe the composed production boundary.
- Use property or metamorphic checks for round trips, idempotency, ordering, representation changes, retries, and recovery.
- Use differential probes and shared-oracle parity matrices when a wrapper, adapter, generated contract, index, cache, external implementation, or equivalent entrypoint should agree with its source of truth.
- Use covering arrays for interacting dimensions instead of every possible combination.
- Inject deterministic clocks, failures, aborts, observers, locks, streams, filesystems, and external responses.
- Use targeted mutations to prove the evidence detects a removed guard, swapped comparison, skipped cleanup, broken transaction, ignored backpressure signal, or altered capability. Restore every mutation before reporting.

## State paths

When behavior has modes, events, guards, effects, retries, cancellation, or interacting processes, write the state paths before selecting examples. Cover every relevant transition, rejection, retry, cancellation, partial result, and cleanup edge at least once. Flag the informal state machine even when the review does not refactor it.

## Evidence discipline

Prefer public boundaries over private implementation details. Use broad suites only as supporting context. Keep a claim only when its reproduction or direct proof would let a repair verifier distinguish fixed, still broken, and moved elsewhere.
