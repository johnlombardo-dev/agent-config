# Review packet

Review this artifact download boundary. Report only actionable defects.

```ts
export async function writeArtifact(root: string, relativeName: string, body: Uint8Array) {
  const destination = resolve(root, relativeName);
  if (!destination.startsWith(root)) throw new Error("outside artifact root");
  await writeFile(destination, body, { flag: "wx", mode: 0o600 });
}
```

Callers may choose a nested relative filename. The operation must remain inside `root`, must not follow a symlink at any path segment, and must not overwrite an existing file. Existing directories inside the root may be attacker-controlled.
