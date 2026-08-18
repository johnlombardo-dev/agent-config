# Review packet

Review this streaming subscription hook. Report only actionable defects supported by its lifecycle.

```tsx
export function useVisibleStream(source: { subscribe(fn: (value: number) => void): () => void }) {
  const targetRef = useRef<HTMLDivElement>(null);
  const [documentVisible, setDocumentVisible] = useState(() => !document.hidden);
  const [intersecting, setIntersecting] = useState(true);

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => setIntersecting(entry.isIntersecting));
    if (targetRef.current) observer.observe(targetRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!documentVisible || !intersecting) return;
    return source.subscribe(() => {});
  }, [documentVisible, intersecting, source]);

  return targetRef;
}
```

The observer callback is asynchronous. Offscreen components must not subscribe before visibility has been observed.
