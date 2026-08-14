# Global Agent Operating Guide

## Project Setup and Frontend Conventions

- Prefer Bun and Vite+ (`vp`) when setting up a new project.
- Expose Vite+ formatting and linting through the project's `package.json` scripts. Use `format` for
  `vp fmt` and `lint` for `vp lint`, and configure the lint script to apply safe automatic fixes.
- For every app or package that uses Tailwind CSS, install and configure the
  `oxlint-tailwindcss` plugin. Enable `tailwindcss/enforce-canonical` so linting can automatically
  replace non-canonical classes such as `tracking-[-0.05em]` with `tracking-tighter`.
- Before scaffolding a new React site, ask which framework to use and which shadcn/ui React Aria
  preset to start from. Prefer shadcn/ui components built on React Aria Components.
- Prefer `tailwind-variants` over `cva` for variant-based component styling.
- Never compose `className` strings with string interpolation. Use the project's `cn` helper for
  conditional or composed classes.

## Writing

- Apply the `unslop` skill to every piece of prose you write or edit, including agent responses,
  documentation, UI copy, code comments, commit messages, and pull request text.
- Also apply the `product-unslop` skill when creating, editing, or reviewing product copy, UI text,
  product documentation, product claims, positioning, benefits, or calls to action.
