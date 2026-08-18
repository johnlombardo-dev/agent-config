# Repair verification packet

Original failure: a multi-select dropped controlled values that were absent from the configured options.

The repair preserves unknown values through string keys:

```tsx
type Choice = string | number;

function reconcile(options: Choice[], previous: Choice[], selected: Choice[]) {
  const selectedKeys = new Set(selected.map(String));
  const configured = options.filter((value) => selectedKeys.has(String(value)));
  const optionKeys = new Set(options.map(String));
  const unavailable = previous.filter(
    (value) => !optionKeys.has(String(value)) && selectedKeys.has(String(value)),
  );
  return [...configured, ...unavailable];
}
```

The component accepts both string and number choices. Verify the repair and adjacent identity cases.
