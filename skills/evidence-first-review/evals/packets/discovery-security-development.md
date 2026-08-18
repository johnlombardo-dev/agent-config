# Review packet

Review this Agent Mail API authorization boundary. Report only actionable defects.

```ts
export function mayAccessApi(request: Request, ownerLogin: string, bearerValid: boolean) {
  if (bearerValid) return true;
  return request.headers.get("Tailscale-User-Login") === ownerLogin;
}
```

Every `/v1` API route requires a valid scoped bearer token, including requests received through Tailscale Serve. The exact Tailscale owner header may replace bearer authentication only for read-only `/reports` pages. The daemon binds to localhost because a non-local client can spoof that header.
