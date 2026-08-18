# Review packet

Review this external-content FTS update. Report only actionable defects.

```ts
export function suppressMessage(database: Database, messageId: string) {
  database.transaction(() => {
    database.query("UPDATE classification SET lane = 'suppress' WHERE message_id = ?").run(messageId);
    const row = database
      .query("SELECT rowid, subject, body FROM indexed_message_content WHERE message_id = ?")
      .get(messageId);
    if (row) {
      database.query(
        "INSERT INTO search_index(search_index, rowid, subject, body) VALUES ('delete', ?, ?, ?)",
      ).run(row.rowid, row.subject, row.body);
    }
  })();
}
```

`search_index` is an FTS5 external-content table. `indexed_message_content` excludes rows whose lane is `suppress`. Suppression must remove the message's prior terms from FTS in the same transaction as the classification change.
