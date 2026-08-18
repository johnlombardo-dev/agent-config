# Review packet

Review this search endpoint. Report only actionable defects.

```ts
export async function search(query: string, limit: number, store: Store) {
  const ids = await store.matchingIds(query);
  const hydrated = await Promise.all(ids.map((id) => store.loadDocument(id)));
  hydrated.sort((left, right) => right.score - left.score);
  return hydrated.slice(0, limit);
}
```

`matchingIds()` may return hundreds of thousands of IDs. `loadDocument()` reads several related rows and generates a snippet. The endpoint promises bounded top-100 requests and should rank lightweight candidates before hydrating only the returned page.
