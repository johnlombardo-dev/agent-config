# Review packet

Review this ImapFlow mailbox scan. Report only actionable defects.

```ts
export async function scan(client: ImapFlow) {
  const lock = await client.getMailboxLock("INBOX");
  try {
    for await (const item of client.fetch("1:*", { uid: true, flags: true })) {
      const full = await client.fetchOne(item.uid, { source: true }, { uid: true });
      await ingest(full.source);
    }
  } finally {
    lock.release();
  }
}
```

ImapFlow's `fetch()` returns an async generator that owns the connection until iteration completes. Its contract forbids running another IMAP command inside that loop. The scan must remain bounded and download complete messages without setting `\\Seen`.
