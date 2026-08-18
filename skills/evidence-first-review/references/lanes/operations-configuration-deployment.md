# Operations, configuration, and deployment

## Select when

The target changes ports, paths, environment variables, configuration files, service managers, containers, CI, build tooling, package/runtime versions, release artifacts, health checks, or operational documentation.

## Review

- Build a configuration closure across allocator/registry, defaults, validators, CLI, generated contracts, service definitions, proxies, tests, examples, and troubleshooting docs.
- Verify production and test resources are isolated and collision-free.
- Exercise install, upgrade/reinstall, start, health check, restart, stop, uninstall, rollback, and dry-run behavior where applicable.
- Check absolute paths, permissions, quoting/argument boundaries, secret placement, runtime resolution, platform assumptions, and failure redaction.
- Compare source, built artifact, documented command, and deployed invocation.

## Evidence

Use isolated config roots, resource-allocation checks, clean-environment builds, and outcome probes. Dry-run plans, generated artifacts, and exact argv assertions prove invocation, not resulting operational state. Escalate to security for trust/secret boundaries or public contract for user-facing configuration.
