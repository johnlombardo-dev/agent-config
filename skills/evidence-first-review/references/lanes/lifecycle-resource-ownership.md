# Lifecycle and resource ownership

## Select when

The target acquires or releases refs, observers, subscriptions, timers, streams, files, locks, sockets, processes, actors, caches, or other resources across mount, start, update, hide, stop, abort, or failure.

## Review

- Name the owner of every resource and every terminal path that must release it.
- Cover first observation, update, replacement, hide/reveal, abort, failure, unmount/stop, restart, and idempotent repeated cleanup.
- Confirm internal ownership does not overwrite caller refs or ambient realm/document ownership.
- Prove partially initialized resources close in reverse ownership order and stopped work cannot publish late results.

## Evidence

Inject cleanup counters, deterministic observers, aborts, owner documents, streams, and failures after each acquisition step. Escalate to concurrency for ordering races or performance for retained/unbounded resources.
