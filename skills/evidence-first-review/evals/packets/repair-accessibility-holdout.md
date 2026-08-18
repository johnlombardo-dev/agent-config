# Repair verification packet

Original failure: another panel covered a newly added panel and intercepted its controls.

The repair sets a fixed inline layer:

```tsx
export function ToolPanels() {
  return (
    <PanelProvider>
      <Panel id="basics" style={{ zIndex: 100 }}>Basics</Panel>
      <Panel id="choices" style={{ zIndex: 100 }}>Choices</Panel>
    </PanelProvider>
  );
}
```

The provider marks the most recently activated panel with `data-active`. Package CSS gives an active panel a raised z-index. Verify the original overlap and activation paths.
