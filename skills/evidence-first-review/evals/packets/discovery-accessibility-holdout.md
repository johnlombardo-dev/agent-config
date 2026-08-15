# Review packet

Review this detached choice popup inside a modal. Report only actionable defects supported by the code and stated layer tokens.

```tsx
const layers = { popover: 60, dialog: 80 };

function ChoicePopover({ children }: PropsWithChildren) {
  return createPortal(
    <div role="listbox" style={{ position: "fixed", zIndex: layers.popover }}>
      {children}
    </div>,
    document.body,
  );
}

export function SettingsDialog() {
  return (
    <div role="dialog" aria-modal="true" style={{ position: "fixed", zIndex: layers.dialog }}>
      <button>Choose value</button>
      <ChoicePopover><div role="option">One</div></ChoicePopover>
    </div>
  );
}
```

The popup is opened from the dialog and must remain visible and interactive above the overlay that opened it.
