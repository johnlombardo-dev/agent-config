# Performance, capacity, and backpressure

## Select when

The target processes unbounded or large input, streams data, queries growing datasets, hydrates collections, batches work, paginates, caches, allocates buffers, or promises latency/memory limits.

## Review

- Identify each independent scale variable, including input shape, selectivity, consumer speed, and deadline where relevant. Prove CPU, memory, I/O, storage, and external-call growth against them.
- Check that streams preserve backpressure and close on producer, consumer, and cancellation failure.
- Rank/filter before expensive hydration, bound queues and payloads, and make pagination stable under ties and concurrent changes.
- Distinguish cold/warm behavior and measure promised percentiles and timeouts at the public boundary on representative hardware or an isolated process.
- Confirm tests do not retain the fixture they claim the product streams.

## Evidence

Use measured benchmarks, RSS ceilings, query plans, call counters, adversarial sizes, and isolated child processes. Do not infer performance from code shape alone. Escalate to security for attacker-controlled consumption or persistence for index/query consistency.
