# Review packet

Review this generic React TypeScript subscription hook. Report only actionable defects.

```tsx
export function useSubscription<T>(source: { subscribe(fn: (value: T) => void): () => void }) {
  const [value, setValue] = useState<T | undefined>();

  useEffect(() => source.subscribe(setValue), [source]);

  return value;
}
```

The source contract returns its cleanup function. React invokes an effect's returned function before a changed source and on unmount.
