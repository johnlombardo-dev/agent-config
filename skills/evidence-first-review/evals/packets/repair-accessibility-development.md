# Repair verification packet

Original failure: read-only slider thumbs remained focusable but did not communicate read-only state.

The repair changes the wrapper:

```tsx
export function Slider({ value }: { value: number }) {
  return (
    <div role="group" aria-label="Volume" aria-describedby="read-only-note">
      <input type="range" value={value} readOnly />
      <span id="read-only-note" hidden>Read only.</span>
    </div>
  );
}
```

Verify the original keyboard and accessibility path against the actual focus target.
