# Review packet

Review this notification publication path and its passing tests. Report only actionable defects.

```ts
export async function publish(id: string, store: Store, broker: Broker) {
  const notification = await store.load(id);
  await store.markPublished(id);
  await broker.send(notification);
}
```

Tests use a broker fake whose `send()` either resolves or rejects before accepting the notification. Production delivery can instead accept a notification and then report a timeout before acknowledging it. The worker retries `publish()` after any thrown error. A stored `published` state must mean the notification was delivered, and retry or restart must not duplicate an accepted delivery.
