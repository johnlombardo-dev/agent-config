# Review packet

Review the public TypeScript contract. Report only actionable defects that can be demonstrated through a supported construction form.

```tsx
type Field<T> = { readonly key: string; readonly __value?: T };
type AnyField = Field<any>;
type FieldValue<F> = F extends Field<infer T> ? T : never;

export type NumberDashletProps<F extends AnyField = AnyField> = {
  field: FieldValue<F> extends number ? F : never;
  formatValue?(value: FieldValue<F>): ReactNode;
};

function NumberDashletInner<F extends AnyField>(props: NumberDashletProps<F>) {
  return <div>{props.field.key}</div>;
}

export const NumberDashlet = forwardRef(NumberDashletInner) as <F extends AnyField>(
  props: NumberDashletProps<F> & RefAttributes<HTMLDivElement>,
) => ReactElement;

type Extracted = ComponentProps<typeof NumberDashlet>;
```

Consumers use direct JSX, `createElement`, explicit prop aliases, generic wrappers, and `ComponentProps` extraction.
