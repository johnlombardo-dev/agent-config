# Repair verification packet

Original failure: an internal observer ref replaced the caller's forwarded ref.

The repair uses a callback that updates both refs:

```tsx
function setRef<T>(ref: ForwardedRef<T>, value: T | null) {
  if (typeof ref === "function") ref(value);
  else if (ref) ref.current = value;
}

export const Probe = forwardRef<HTMLDivElement>(function Probe(_, forwardedRef) {
  const internalRef = useRef<HTMLDivElement>(null);
  const mergedRef = useCallback((value: HTMLDivElement | null) => {
    internalRef.current = value;
    setRef(forwardedRef, value);
  }, [forwardedRef]);
  return <div ref={mergedRef} />;
});
```

Verify mount, forwarded-ref replacement, and unmount behavior.
