# Review packet

Review this retrying poller. Report only actionable defects.

```ts
export function startPoller(run: () => Promise<void>, signal: AbortSignal) {
  const poll = async () => {
    try {
      await run();
    } finally {
      setTimeout(poll, 1_000);
    }
  };
  signal.addEventListener("abort", () => undefined, { once: true });
  void poll();
}
```

Stopping the owner aborts `signal`. After stop resolves, no new poll may start and no retry timer may retain the owner. Aborting during `run()` may allow that invocation to finish, but it must not schedule another.
