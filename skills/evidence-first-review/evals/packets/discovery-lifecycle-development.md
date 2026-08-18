# Review packet

Review this forwarded-ref component. Report only actionable defects supported by the code.

```tsx
type Props = { onVisibleChange(visible: boolean): void };

export const VisibilityProbe = forwardRef<HTMLDivElement, Props>(function VisibilityProbe(
  { onVisibleChange },
  forwardedRef,
) {
  const targetRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => onVisibleChange(entry.isIntersecting));
    if (targetRef.current) observer.observe(targetRef.current);
    return () => observer.disconnect();
  }, [onVisibleChange]);

  return <div ref={targetRef} data-probe />;
});
```

The ref is public and consumers use it to measure the rendered element.
