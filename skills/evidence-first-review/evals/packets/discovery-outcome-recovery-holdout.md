# Review packet

Review these archive administration paths and their passing tests. Report only actionable defects.

```ts
export async function backup(archive: Archive, destination: string) {
  await archive.database.backup(`${destination}/archive.sqlite`);
  return { ok: true };
}

export async function uninstall(service: Service, run: (argv: string[]) => Promise<void>) {
  await run(["servicectl", "stop", service.label]);
  return { removed: true };
}
```

The archive retains canonical documents in SQLite and content-addressed files under `blobs/`. Restoring a backup into an empty archive root must reproduce every readable document. Installing the service writes a persistent definition at `service.definitionPath`; after uninstall, neither the running service nor that file may remain. Existing tests assert the database backup call, command arguments, and returned booleans, but do not restore into an empty root or inspect the installed definition afterward.
