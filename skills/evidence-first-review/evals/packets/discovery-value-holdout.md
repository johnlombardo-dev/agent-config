# Review packet

Review this controlled multi-select reconciliation. Report only actionable defects supported by the code.

```tsx
type Choice = string | number;
type Option = { value: Choice; label: string };

function reconcile(options: Option[], controlled: Choice[], selectedKeys: Set<Choice>) {
  return options
    .filter((option) => selectedKeys.has(option.value))
    .map((option) => option.value);
}

export function MultiSelect({ options, value, onChange }: {
  options: Option[];
  value: Choice[];
  onChange(value: Choice[]): void;
}) {
  return (
    <ChoicePopup
      selectedKeys={new Set(value)}
      onSelectionChange={(keys) => onChange(reconcile(options, value, keys))}
    />
  );
}
```

Controlled values may remain valid while temporarily absent from the current option collection. Selecting a configured option must not silently rewrite unrelated canonical values.
