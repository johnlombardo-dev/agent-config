# Review packet

Review this durable remote-action workflow and its passing normal-path tests. Report only actionable defects.

```ts
type Attempt = {
  planId: string;
  expiresAt: number;
  dispatchCrossed: boolean;
};

export async function start(plan: Attempt, now: number, store: Store, executor: Executor) {
  if (now >= plan.expiresAt) throw new Error("expired");
  await store.save(plan);
  return resume(plan, now, store, executor);
}

export async function resume(
  attempt: Attempt,
  now: number,
  store: Store,
  executor: Executor,
) {
  const result = attempt.dispatchCrossed
    ? await executor.reconcile(attempt.planId)
    : await executor.apply(attempt.planId);
  await store.saveResult(attempt.planId, result);
}
```

The store survives process crashes. Recovery loads every attempt without a result and calls `resume()` with the current time. It serializes recovery per attempt, and the durable `dispatchCrossed` value correctly records whether the remote-effect boundary was crossed. An action plan authorizes remote mutation only until `expiresAt`. If dispatch began before expiry, recovery may reconcile that effect without issuing another command. If a crash happened after `store.save()` but before dispatch and recovery occurs after expiry, recovery must not begin the remote effect.
