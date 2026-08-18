# Review packet

Review this public field-bound wrapper. Report only actionable defects supported by React and TypeScript behavior.

```tsx
type Field<T> = { key: string; value: T };

type ShellProps = Omit<HTMLAttributes<HTMLDivElement>, "children"> & {
  label: ReactNode;
};

export type ToggleProps = ShellProps & {
  field: Field<boolean>;
};

export function Toggle({ field, label, ...shellProps }: ToggleProps) {
  return (
    <div {...shellProps}>
      <label>{label}<input type="checkbox" checked={field.value} readOnly /></label>
    </div>
  );
}
```

The field is the only accepted value authority. Consumers use JSX, `createElement`, prop aliases, and extracted component props.
