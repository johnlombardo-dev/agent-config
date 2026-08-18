# Review packet

Review this streamed message ingestion. Report only actionable defects.

```ts
export async function storeRawMessage(source: AsyncIterable<Uint8Array>, blobs: BlobStore) {
  const chunks: Uint8Array[] = [];
  for await (const chunk of source) chunks.push(chunk);
  return blobs.put(new Blob(chunks).stream());
}
```

The source may be a 250 MiB message. Attachment size must not determine process memory, and producer or consumer failure must close the transfer without retaining accumulated chunks.
