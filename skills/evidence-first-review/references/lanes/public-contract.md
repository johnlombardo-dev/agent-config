# Public contract

## Select when

The target changes exported types, schemas, commands, routes, payloads, configuration, package entrypoints, generated contracts, compatibility promises, or runtime validation.

## Review

- Pair static types with runtime guards and positive cases with wrong-domain, malformed, unknown, duplicate, missing, and runtime-erased inputs.
- Exercise direct construction, wrappers, extracted aliases, public entrypoints, and source versus built artifacts.
- Compare CLI, API, schema, documentation, and generated representations for the same operation.
- Check backward compatibility, defaults, versioning, optional dependencies, SSR or platform entrypoints, and error shapes that callers depend on.

## Evidence

Use compile fixtures, schema probes, golden request/response shapes, package-isolation builds, and differential checks between generated and runtime contracts. Escalate to protocol for vendor semantics or operations for deployed configuration.
