# Repair verification packet

Original failure: extracted component props accepted fields with the wrong value domain.

The repair makes the unspecialized generic fail closed:

```tsx
type Field<T> = { key: string; readonly __value?: T };
type Props<F extends Field<unknown> = never> = {
  field: F;
};

function Inner<F extends Field<unknown>>(props: Props<F>) {
  return <div>{props.field.key}</div>;
}

export const NumberControl = forwardRef(Inner) as <F extends Field<number> = never>(
  props: Props<F> & RefAttributes<HTMLDivElement>,
) => ReactElement;

const field: Field<number> = { key: "count" };
createElement(NumberControl, { field });
```

Supported consumers use direct JSX, `createElement`, explicit prop aliases, wrappers, and `ComponentProps`. Verify the repair across those forms.
