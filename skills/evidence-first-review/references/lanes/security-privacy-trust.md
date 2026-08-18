# Security, privacy, and trust

## Select when

The target crosses an untrusted input, identity, authorization, secret, sensitive-data, filesystem, process, network, renderer, log, or administrative boundary.

## Review

- Trace sources, validation, authorization decisions, transformations, sinks, logs, and error responses across every trust zone.
- Separate authentication from object, property, and function authorization. Verify default deny and the exact sensitive operation at every entrypoint.
- Check injection, traversal, symlinks, unsafe deserialization, command execution, output encoding, secret lifecycle, token comparison, permissions, and redaction.
- Exercise abuse paths, spoofed identity, replay, stale authorization, oversized input, and partial failure without trusting client or provider claims. Treat public validation algorithms as attacker-known and recompute dependent fields after tampering.

## Evidence

Prefer boundary tests, threat-derived abuse cases, static analysis, fuzzing of parsers and validators, and source-to-sink probes. Never expose real credentials or production data. Escalate to operations for deployment trust assumptions or protocol for third-party input semantics.
