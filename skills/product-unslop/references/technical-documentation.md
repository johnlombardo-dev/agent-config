# Technical documentation

Help the reader use the product correctly. Treat documentation as a technical tool, not a sales page.

## Information order

1. Describe the entity's purpose in one factual sentence before introducing internal terminology.
2. State when to use it and any prerequisites.
3. Show the smallest realistic, runnable example.
4. Explain the behavior the example demonstrates.
5. Document constraints, failure modes, maturity, and relevant alternatives.
6. Put exhaustive options, schema details, and debug metadata in reference sections.

## Requirements

- Describe behavior in terms of what the reader can do and observe.
- Connect implementation details to their practical outcome or constraint.
- Use examples based on a concrete task. Do not use abstract demos or placeholder entities when a realistic example is available.
- Keep identifiers, signatures, defaults, and status claims consistent with current source and tests.
- Distinguish shipped, partial, experimental, deprecated, and planned behavior.
- State important limits directly. Do not bury them in promotional framing.
- Avoid marketing claims, invented ease, and unsupported performance language.
- Explain unfamiliar product terms on first use.

## Audit

- Can the reader tell what the documented entity does from its first sentence?
- Can the example run with the stated prerequisites?
- Does the explanation cover the observable result and relevant failure cases?
- Can a technical claim be traced to current source, tests, or an authoritative product decision?
- Does any paragraph try to persuade the reader that the product matters instead of teaching them to use it? Remove or rewrite it.
