# Review packet

Review this webhook ingestion boundary. Report only actionable defects.

```ts
export async function ingest(request: Request, context: AuthContext) {
  if (!context.authenticated) return new Response("unauthorized", { status: 401 });

  const body = await request.clone().json();
  if (!context.scopes.includes("events:write")) {
    return new Response("forbidden", { status: 403 });
  }

  const event = EventSchema.parse(body);
  await saveEvent(event);
  return new Response(null, { status: 204 });
}
```

Authenticated callers may send arbitrary request bodies, including chunked bodies without `Content-Length`. The endpoint contract limits encoded bodies to 256 KiB. Declared oversize requests should be rejected before reading, and streaming requests must stop at the same ceiling without fully materializing or parsing the JSON. Callers lacking `events:write` must not be able to force that work merely because their bearer is otherwise valid.
