---
name: product-unslop
description: Replace product hype with source-grounded explanation. Use when writing, editing, or reviewing product websites, landing or feature pages, onboarding, UI copy, technical documentation, comparisons, positioning, benefits, or calls to action.
---

# Product unslop

Explain the product from evidence. Hype often hides shallow understanding.

## Required foundation

Read and apply [`unslop`](../unslop/SKILL.md). It handles sentence-level clarity and voice. This skill decides what the product writing must say, prove, and help the reader do.

## Workflow

### 1. Understand before writing

Start with the closest sources of product truth. Prefer current product documents, shipped behavior, public APIs, types, tests, examples, and explicit roadmap status over existing marketing copy.

Identify:

- The product category and intended reader.
- The problem the reader already recognizes.
- The concrete actions the product supports.
- The mechanism behind each claimed benefit.
- The important constraints, prerequisites, and maturity limits.

Do not hide conflicts between sources. Resolve the conflict, qualify the copy, or ask for the missing product decision.

### 2. Write the product model

Complete this scratch model before drafting:

```text
[Product] is a [category] for [reader].
It lets them [concrete action] by [relevant mechanism].
It currently [important constraint or maturity status].
```

Replace every bracket with a specific answer. Inspect more source material if an answer remains generic. Model each product separately when a suite contains products with different users, problems, or responsibilities.

### 3. Choose the writing mode

- For homepages, landing pages, feature pages, and other first contact, read [first-contact-pages.md](references/first-contact-pages.md).
- For controls, labels, onboarding, empty states, errors, and settings, read [ui-copy.md](references/ui-copy.md).
- For guides, component documentation, API documentation, and technical explanations, read [technical-documentation.md](references/technical-documentation.md).

Read every applicable reference when an artifact combines modes.

### 4. Draft for information

Order the writing by what the reader needs to understand or do next. Explain concrete behavior before introducing product terms. Tie each technical detail to an outcome or constraint the user can observe.

Every sentence must do at least one job:

- Orient the reader.
- Differentiate with a supported fact.
- Set an expectation.
- Reduce uncertainty.
- Enable an action.

### 5. Apply `unslop`, then audit again

Run `unslop` after the product structure is sound. Then repeat the product audit to make sure sentence cleanup did not remove a necessary distinction, condition, or limit.

## Reject LinkedIn language

Treat hype as a warning that the writer does not yet understand the product. Reject copy that projects importance instead of explaining behavior.

Remove or rewrite:

- Unsupported claims that the product transforms, reinvents, revolutionizes, or changes the future.
- Generic benefits such as powerful, seamless, flexible, or innovative without a named mechanism.
- Verbs such as empower, unlock, elevate, supercharge, and reimagine when they replace the user's action.
- Grand problem statements that users or sources did not establish.
- Architecture presented as valuable without explaining its consequence.
- Competitive claims, social proof, or business outcomes without supporting evidence.
- Planned or partial capabilities presented as available.
- Sentences that could describe a competing product without changing a word.

Find the behavior or evidence behind every benefit claim. If none exists, inspect further, narrow the claim, or delete it.

## Final audit

Answer each question from the finished copy:

1. What is the product?
2. Who is it for?
3. What can that person do with it?
4. How does it produce the stated result?
5. What important limit or prerequisite applies?
6. What should the reader do next?
7. Which source supports each capability and maturity claim?

Rewrite copy that sells importance more clearly than it explains the product.
