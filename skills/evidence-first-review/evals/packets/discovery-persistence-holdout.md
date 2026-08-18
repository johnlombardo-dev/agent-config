# Review packet

Review this SQLite migration runner. Report only actionable defects.

```ts
export function migrate(database: Database, migrations: readonly Migration[]) {
  let version = database.query("PRAGMA user_version").get().user_version;
  for (const migration of migrations) {
    if (migration.version <= version) continue;
    migration.apply(database);
    database.exec(`PRAGMA user_version = ${migration.version}`);
    version = migration.version;
  }
}
```

Each migration may contain several DDL and data-copy statements. If any statement or version update fails, reopening the database must observe the complete prior schema and prior `user_version`, never a partially applied migration.
