# Accessibility and interaction

## Select when

The target changes rendered controls, focus targets, overlays, labels, errors, keyboard or pointer handling, disabled/read-only behavior, responsive interaction, direction, or visual accessibility state.

## Review

- Inventory rendered interaction targets rather than component names.
- Cover accessible names, descriptions, errors, roles, states, focus movement and return, keyboard, pointer, touch targets, disabled/read-only behavior, portals, RTL, and forced colors where applicable.
- Compare direct controls with composed wrappers and detached overlays.
- Pair input method, state, placement, direction, and color mode with a covering array when they share code.

## Evidence

Use a real browser for focus, hit testing, geometry, portals, computed styles, and accessibility-tree behavior. Escalate to lifecycle when observers or hidden state own the failure, or public contract when composition drops required props.
