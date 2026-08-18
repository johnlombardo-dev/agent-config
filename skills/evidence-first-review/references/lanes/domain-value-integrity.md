# Domain and value integrity

## Select when

The target transforms, normalizes, classifies, calculates, identifies, orders, routes, formats, serializes, or reconciles domain values.

## Review

- State canonical identities and business invariants before examples.
- Build the full write/read closure across validation, normalization, persistence, formatting, serialization, and round trip.
- Include missing, unavailable, duplicate, narrowed, boundary, invalid, non-finite, precision, ordering, and partial values that the contract permits.
- Compare direct entrypoints and composed wrappers that claim equivalent behavior.
- Exercise eligibility, precedence, defaulting, and rejection rules without silently coercing one domain into another.

## Evidence

Prefer property checks, round trips, boundary tables, and differential probes against the canonical implementation. Escalate to persistence when durable representation participates, or public contract when callers can observe the mismatch.
