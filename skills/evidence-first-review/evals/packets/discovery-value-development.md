# Review packet

Review this controlled React input. Report only actionable defects supported by the code.

```tsx
type Props = {
  value: number;
  onChange(value: number): void;
  maximumFractionDigits?: number;
};

export function NumberEditor({ value, onChange, maximumFractionDigits = 3 }: Props) {
  const formatted = new Intl.NumberFormat("en", { maximumFractionDigits }).format(value);
  const [draft, setDraft] = useState(formatted);

  useEffect(() => setDraft(formatted), [formatted]);

  return (
    <input
      aria-label="Number"
      value={draft}
      onChange={(event) => setDraft(event.currentTarget.value)}
      onBlur={() => onChange(Number(draft))}
    />
  );
}
```

The host passes canonical value `1.234567`. A focus followed by blur is a supported interaction even when the user does not edit.
