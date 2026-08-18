# Security, privacy, and trust

## Select when

The target crosses an untrusted input, identity, authorization, secret, sensitive-data, filesystem, process, network, renderer, log, or administrative boundary.

## Review

### Authority and capability

- Trace untrusted sources, authenticated context, validation, authorization, durable records, effects, results, logs, and errors across every trust zone. Separate authentication from object, property, and function authorization; verify default deny and the exact sensitive operation at every entrypoint.
- Write the authority state paths. At every transition that can begin a durable or external effect, including retry and recovery, revalidate the principal, operation or scope, object and targets, version or claim, and expiry. Distinguish a new effect from reconciliation after an effect crossed its boundary; expiry must block the former, while the latter needs its own read-only authority.
- When approval is intended to be independent, require a single-use authority artifact that the acting credential cannot mint for itself. Bind it to the authenticated approver, intent, operation, object version or digest, exact targets, issue and expiry times, nonce, and consumption receipt.
- Derive identity and role only from authenticated context, then persist and compare that provenance on consequential authorization and effect records. Treat loopback, proxy, or provider headers as data until a verified intermediary establishes them and strips or rejects direct-client copies.
- Audit raw effect and result-finalization capability reachability through schemas, routes, CLI commands, package entrypoints, imports, exports, aliases, and re-exports. Recompute keyed commitments or content digests before reusing content or authority; treat public validation algorithms as attacker-known and recompute dependent fields after tampering.

### Untrusted work and output

- Enforce byte, item, and time budgets before full parsing, buffering, decompression, decoding, or schema construction. Reject oversized declared lengths early and enforce incremental ceilings for chunked or streaming input.
- Budget raw bytes, decoded bytes, counts, nesting depth, fan-out, and retained metadata independently. Check injection, traversal, symlinks, unsafe deserialization, command execution, secret lifecycle, token comparison, permissions, and redaction.
- Define separate output policies for human terminals, structured JSON, HTML or Markdown, logs, filenames, and exact binary output. Test controls and metacharacters at the final renderer or sink instead of assuming one shared input policy fits every context.
- For a manifested advisory or security-sensitive dependency, verify the exact affected version, runtime reachability, compensating controls, owner, and removal condition. A green advisory scan alone does not close a reachable dependency risk.

## Evidence

For each manifested invariant, prefer boundary tests, threat-derived abuse cases, source-to-sink probes, static analysis, and parser or validator fuzzing. Useful counterexamples include:

- Persist authority before expiry, interrupt before dispatch, then recover after expiry: no new external effect. A dispatch-crossed attempt may reconcile without repeating the effect.
- Try self-approval, replay, client-supplied attribution, a capability hidden behind a re-export, and a forged intermediary header. None may acquire or misattribute authority.
- Send oversized declared and chunked bodies plus independently amplified decoded, count, depth, fan-out, and metadata fixtures. Rejection must occur with bounded materialization before the expensive transformation.
- Exercise terminal escape families, carriage return, backspace, bidirectional controls, hostile links, and filenames at human sinks while exact-binary paths remain byte-exact. Tampered bytes or canonical fields must fail commitment checks.

Never expose real credentials or production data. Escalate a demonstrated seam to concurrency for workflow ordering, performance for measured ceilings, public contract for exposed entrypoints, protocol for decoding or provider semantics, or operations for deployment trust. Keep security as the owner of authority, provenance, intentional attacker-controlled consumption, and sensitive-output invariants.
