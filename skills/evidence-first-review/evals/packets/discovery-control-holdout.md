# Review packet

Review this typed selection reconciliation. Report only actionable defects.

```tsx
type Choice = string | number;

const keyOf = (value: Choice) => `${typeof value}:${String(value)}`;

export function reconcile(
  declared: readonly Choice[],
  previous: readonly Choice[],
  selectedKeys: ReadonlySet<string>,
) {
  const declaredKeys = new Set(declared.map(keyOf));
  const configured = declared.filter((value) => selectedKeys.has(keyOf(value)));
  const unavailable = previous.filter(
    (value) => !declaredKeys.has(keyOf(value)) && selectedKeys.has(keyOf(value)),
  );
  return [...configured, ...unavailable];
}
```

The contract preserves string-versus-number identity, uses JavaScript Set semantics within one primitive type, keeps declared order for configured choices, and retains prior relative order for unavailable choices.
