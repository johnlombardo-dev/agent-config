# Review packet

Review this remote-action worker. Report only actionable defects.

```ts
export async function executePending(store: Store, remote: Remote) {
  const plan = await store.findPendingPlan();
  if (!plan) return;
  for (const target of plan.targets) await remote.apply(plan.kind, target);
  await store.markExecuting(plan.id);
  await store.markSucceeded(plan.id);
}
```

Multiple worker wakeups may overlap. A plan must be claimed once before any remote effect. Completed target results are durable, and a retry must skip them rather than repeat an already successful remote change.
