# Review packet

Review this HTTP retry integration. Report only actionable defects.

```ts
export async function requestWithRetry(request: () => Promise<Response>) {
  const response = await request();
  if (response.status !== 429) return response;
  const retryAfter = Number(response.headers.get("Retry-After") ?? "1");
  await new Promise((resolve) => setTimeout(resolve, retryAfter));
  return request();
}
```

For this API, a numeric `Retry-After` value is a non-negative delay in seconds. The client must not retry earlier than requested. Date-form values are unsupported and must produce a stable refusal rather than an immediate retry.
