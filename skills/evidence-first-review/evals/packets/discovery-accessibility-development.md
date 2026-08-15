# Review packet

Review this read-only range control. Report only actionable defects supported by the rendered behavior.

```tsx
export function Range({ value }: { value: [number, number] }) {
  return (
    <div role="group" aria-label="Range" aria-readonly="true">
      <input type="range" min="0" max="100" value={value[0]} readOnly />
      <input type="range" min="0" max="100" value={value[1]} readOnly />
    </div>
  );
}
```

Both native inputs remain keyboard-focusable so users can inspect their values. The product contract requires read-only state to be communicated on the focusable interaction target without allowing writes.
