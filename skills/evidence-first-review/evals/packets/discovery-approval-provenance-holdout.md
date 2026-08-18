# Review packet

Review this production deployment approval flow. Report only actionable defects.

```ts
export async function authorize(request: Request, context: AuthContext, store: Store) {
  if (!context.scopes.includes("deploy:authorize")) throw new Error("forbidden");
  const input = await request.json();
  await store.saveApproval({
    changeId: input.changeId,
    digest: input.digest,
    approvedBy: input.actor,
  });
}

export async function commit(change: Change, context: AuthContext, store: Store) {
  if (!context.scopes.includes("deploy:commit")) throw new Error("forbidden");
  const approval = await store.loadApproval(change.id);
  if (!approval) throw new Error("approval required");
  await deploy(change);
}
```

Production policy requires a separate approver credential from the credential that commits a deployment. The default agent credential currently holds both scopes. Authenticated identity is `context.principal`; request fields are untrusted. An approval is valid for one exact change digest and target set for ten minutes, and it may authorize only one commit. Approval records survive restart.
