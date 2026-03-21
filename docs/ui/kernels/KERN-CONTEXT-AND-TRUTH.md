# KERN-CONTEXT-AND-TRUTH — Context and Truth Kernel

## Metadata
- **Kernel ID**: KERN-CONTEXT-AND-TRUTH
- **Version**: 1.0.0
- **Wave**: UI Kernel Foundation
- **Status**: Active

## Purpose

Governs active object identity, source basis, compare state, lineage visibility, and context propagation across the cockpit. Owns Truth Echo semantics. Forbids UI truth drift and ambiguous selection state.

## Doctrine

1. **One active object identity at a time, or fail closed.** The cockpit must always be oriented around exactly one active object, or explicitly report failure.
2. **Truth Echo is governed context synchronization, not decorative highlighting.** When the active object changes, all subscribed panels reorient around that object through the event bus.
3. **UI may not invent truth.** All canonical data flows through adapters. Panels may derive local state but must never present derived data as canonical.
4. **Source basis must be visible.** Every piece of data shown must be traceable to its basis: canonical, derived, draft, compare, or mock.
5. **Compare state is explicit.** When comparing two objects, both identities and the compare mode must be clearly visible.
6. **Ambiguity fails closed.** If the active object is null, has no id, or cannot be resolved, Truth Echo reports failure rather than propagating bad state.

## Truth Definition

This kernel governs the *identity* of truth in the UI, not the truth itself. Canonical truth lives in upstream systems (Construction_Kernel, Construction_Runtime). The UI consumes truth through adapters. This kernel ensures the UI's *reference to truth* is unambiguous and stable.

## Owned Scope

- Active object identity (`ActiveObjectIdentity`)
- Active object source panel
- Active object source basis
- Truth Echo propagation semantics
- Truth Echo failure semantics
- Compare object identity
- State ownership model (6 state layers)
- Context propagation contracts

## Non-Owned Scope

- Canonical data content (owned by upstream kernels via adapters)
- Panel-local derived state (each panel owns its own)
- Event bus mechanics (owned by event system)
- Visual presentation of truth (owned by KERN-UI-PATTERN)

## Canonical Entities

- `ActiveObjectIdentity` — typed identity: id, type, name
- `ActiveObjectState` — full state shape: object, basis, source, compare, mode
- `activeObjectStore` — singleton state store
- `TruthEcho` — orchestration module
- `SourceBasis` — enum: canonical, derived, draft, compare, mock
- `SourcedData<T>` — wrapper for adapter outputs with basis metadata

## Invariants

1. `activeObject` is either a valid `ActiveObjectIdentity` with a non-empty `id`, or `null`.
2. When `activeObject` is `null`, no panel may claim to be oriented around an object.
3. `sourcePanel` always reflects which panel last set the active object.
4. Truth Echo propagation excludes the source panel.
5. Truth Echo failure emits `truth-echo.failed` with a reason.
6. Active object identity must remain stable across panel moves, layout changes, and device class transitions.
7. Draft state must never be visually confused with canonical or validated state.

## Failure Conditions

- Active object set to null without echoFailure being recorded → FAIL
- Active object has empty id → FAIL (fail closed)
- Two panels disagree on active object identity → FAIL
- Truth Echo propagates to the source panel → FAIL
- Draft data presented without draft indicator → FAIL
- Mock data presented without mock indicator → FAIL

## Success Definition

At any point in time, any observer can determine: (1) which object the cockpit is oriented around, (2) which panel set it, (3) what the source basis is, (4) whether Truth Echo is healthy or failed. There is never ambiguity.

## Acceptance Tests

1. Setting a valid object updates activeObjectStore
2. Setting null fails closed with echoFailure message
3. Setting empty-id object fails closed
4. Truth Echo propagates to all following panels except source
5. Truth Echo fails closed on ambiguous object
6. Explorer → Work + Reference + System propagation works
7. Spatial → Explorer + Work + Reference + System propagation works
8. Unfollowing panels are excluded from propagation
9. Compare state is tracked separately from active object
10. Workspace mode changes are tracked
