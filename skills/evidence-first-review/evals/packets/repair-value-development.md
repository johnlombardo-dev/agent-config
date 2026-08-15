# Repair verification packet

Original failure: a controlled number input rounded and emitted its canonical value during focus and blur without a user edit.

The repair adds a suppression flag:

```tsx
const suppressNextChange = useRef(false);

useEffect(() => {
  suppressNextChange.current = true;
  setDraft(format(value));
}, [value]);

function handleChange(next: string) {
  setDraft(next);
  if (suppressNextChange.current) {
    suppressNextChange.current = false;
    return;
  }
  onChange(Number(next));
}
```

The underlying input does not always emit a change when a controlled prop changes. Verify the repair and adjacent user-edit paths.
