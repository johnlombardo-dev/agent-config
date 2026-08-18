# External protocol and integration

## Select when

The target changes a network or file protocol, vendor API, SDK, parser, capability negotiation, runtime dependency behavior, external identity, or compatibility fallback.

## Review

- Read the current primary specification or vendor documentation for the exact operation.
- Compare compile-time types with installed runtime exports and actual response shapes.
- Exercise capability present, absent, ambiguous, downgraded, malformed, reordered, throttled, disconnected, and partially successful responses.
- Check protocol sequencing, locking, cursor/checkpoint semantics, retries, idempotency, and forbidden compatibility fallbacks.
- Keep live probes read-only or disposable and opt-in when credentials or mutations are involved.

## Evidence

Use adapter contract tests, recorded protocol fixtures, capability matrices, differential probes against the installed library, and narrowly scoped live smoke tests. Escalate to security for trusted headers or credentials and concurrency for protocol ordering.
