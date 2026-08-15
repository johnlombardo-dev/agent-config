# Evidence techniques

Read this after mapping the target's seams. Choose methods that can falsify the relevant claim. Do not run every method by default.

## Value integrity

- Build a write-closure matrix. Every value a public control can emit must survive the bound validator, canonical write, formatter, serializer, and round trip.
- Compare direct controls with every composed wrapper that claims the same behavior.
- Include unavailable values, narrowed unions, tuples, readonly arrays, compound objects, non-finite numbers, signed zero, precision limits, and runtime-erased inputs where applicable.
- Use property or metamorphic checks when many values share one invariant. Useful relations include serialize then parse, format then edit, reorder then restore, and change representation without changing meaning.
- Use differential probes when a wrapper and its underlying library should agree.

## Accessibility and interaction

- Inventory rendered interaction targets, not component names. Include closed triggers, popup options, selected tags, thumbs, date segments, help buttons, fallback shells, and detached overlays.
- Test keyboard, pointer, touch-sized targets, focus movement and return, disabled and read-only behavior, accessible names, descriptions, errors, RTL, and forced colors where each target applies.
- Prefer a real browser for focus, hit testing, geometry, portals, computed styles, and accessibility-tree behavior.
- Use a covering array for interacting conditions instead of every possible combination. Pair input method, state, placement, direction, and color mode at minimum when they can affect the same code.

## Public contract

- Test direct JSX, unannotated construction, explicit prop aliases, generic wrappers, extracted component props, runtime-erased inputs, and package entrypoints when they are public.
- Pair positive inference cases with wrong-domain, union-wide, `any`, `never`, malformed configuration, and duplicate or unknown value cases.
- Compare source and built-package exports. Confirm optional peers and experimental entrypoints do not enter stable module graphs.
- Exercise SSR and hydration when a component reads browser state, creates identifiers, portals content, or changes its first rendered shape.

## Lifecycle and rendering

- Inject deterministic observers, timers, visibility, owner documents, resize events, subscription sources, and cleanup counters.
- Cover mount, first callback, update, hide, reveal, unmount, remount, StrictMode replay, and changed-owner cases that apply.
- Check forwarded and merged refs. Confirm internal observers do not replace caller refs.
- Bound streaming or retained data and prove that hidden or unmounted components stop work.
- Compare owner-document behavior with ambient globals for portals, iframes, and multiple realms.

## State paths and mutations

When behavior has modes, events, guards, and effects, write its state paths before selecting examples. Cover each transition, rejection, cancellation, retry, and cleanup edge at least once. Flag the informal state machine even if the review does not refactor it.

Use targeted mutations to test whether the evidence can detect a broken invariant. Good mutations remove a guard, swap a comparison, drop cleanup, replace a typed identity with string coercion, skip one wrapper, or change a controlled value. Restore every mutation before reporting.

## Evidence order

Start with the cheapest faithful proof: type fixture, focused unit test, deterministic component test, browser probe, then broader integration check. Stop when the invariant is demonstrated or record the unavailable evidence as a gap. Never use a broad passing suite to erase a specific uncovered risk.
