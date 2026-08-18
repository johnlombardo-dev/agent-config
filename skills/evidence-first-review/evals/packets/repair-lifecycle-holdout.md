# Repair verification packet

Original failure: a component rendered in an iframe listened to ambient document visibility instead of its owner document.

The repair changes document ownership:

```tsx
useEffect(() => {
  const target = ref.current;
  if (!target) return;
  const ownerDocument = target.ownerDocument;
  const updateVisibility = () => setVisible(!ownerDocument.hidden);
  ownerDocument.addEventListener("visibilitychange", updateVisibility);

  const observer = new IntersectionObserver(([entry]) => setIntersecting(entry.isIntersecting));
  observer.observe(target);

  return () => {
    ownerDocument.removeEventListener("visibilitychange", updateVisibility);
    observer.disconnect();
  };
}, []);
```

The iframe window has its own `IntersectionObserver`. Verify visibility, observation, and cleanup in the owner realm.
