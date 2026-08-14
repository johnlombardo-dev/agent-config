---
name: product-unslop
description: Replace product hype with source-grounded explanation. Use when writing, editing, or reviewing product websites, landing and feature pages, onboarding, UI text, component or API documentation, product comparisons, calls to action, positioning, benefits, or any prose that explains what a product is and why it matters.
---

# Product unslop

Explain the product from evidence. Do not use enthusiasm to hide shallow understanding.

## Required foundation

Read and apply [`unslop`](../unslop/SKILL.md). Use `unslop` for sentence-level clarity and human voice. Use this skill to decide what the product writing must say, prove, and help the reader do.

## Workflow

### 1. Understand before writing

Inspect the closest sources of product truth. Prefer current product documents, shipped behavior, public APIs, types, tests, examples, and explicit roadmap status over existing marketing copy.

Identify:

- The product category and intended reader.
- The problem the reader already recognizes.
- The concrete actions the product supports.
- The mechanism that produces each claimed benefit.
- The important constraints, prerequisites, and maturity limits.

Do not smooth over conflicting sources. Resolve the conflict, qualify the copy, or ask for missing product decisions.

### 2. Write the product model

Complete this scratch model before drafting copy:

```text
[Product] is a [category] for [reader].
It lets them [concrete action] by [relevant mechanism].
It currently [important constraint or maturity status].
```

Replace every bracket with a specific answer. Inspect more source material if the answers remain generic. Model each product separately when a suite contains products with different customer problems or responsibilities.

### 3. Choose the writing mode

- For homepages, landing pages, feature pages, and other first contact, read [first-contact-pages.md](references/first-contact-pages.md).
- For controls, labels, onboarding, empty states, errors, and settings, read [ui-copy.md](references/ui-copy.md).
- For guides, component documentation, API documentation, and technical explanations, read [technical-documentation.md](references/technical-documentation.md).

Read every applicable reference when an artifact combines modes.

### 4. Draft for information

Order information by what the reader needs to understand or do next. Introduce product terms only after explaining their concrete behavior. Connect each technical detail to a user-visible outcome or constraint.

Make every claim earn its place. Keep a sentence only when it does at least one job:

- Orient the reader.
- Differentiate with a supported fact.
- Set an expectation.
- Reduce uncertainty.
- Enable an action.

### 5. Apply `unslop`, then audit again

Apply `unslop` after the product structure is sound. Re-run the product audit after rewriting so sentence cleanup does not remove a necessary distinction, condition, or limitation.

## Reject LinkedIn language

Treat hype as a warning that the writer does not yet understand the product. Reject copy that projects importance instead of explaining behavior.

Remove or rewrite:

- Claims that the product transforms, reinvents, revolutionizes, or changes the future without evidence.
- Generic benefits such as powerful, seamless, flexible, or innovative without a named mechanism.
- Verbs such as empower, unlock, elevate, supercharge, and reimagine when they replace the action a user takes.
- Grand problem statements that users or sources did not establish.
- Architecture presented as inherently valuable without explaining its consequence.
- Competitive claims, social proof, or business outcomes that no source supports.
- Planned or partial capabilities written as available.
- Sentences that could describe a competing product without changing a word.

For every benefit claim, identify the supporting behavior or evidence. If none exists, inspect further, narrow the claim, or delete it.

## Final audit

Answer each question from the finished copy:

1. What is the product?
2. Who is it for?
3. What can that person do with it?
4. How does it produce the stated result?
5. What important limit or prerequisite applies?
6. What should the reader do next?
7. Which source supports each capability and maturity claim?

Rewrite when the copy sells importance more clearly than it explains the product.
