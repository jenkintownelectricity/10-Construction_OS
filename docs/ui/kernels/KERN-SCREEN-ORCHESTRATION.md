# KERN-SCREEN-ORCHESTRATION — Screen Orchestration Kernel

## Metadata
- **Kernel ID**: KERN-SCREEN-ORCHESTRATION
- **Version**: 1.0.0
- **Wave**: UI Kernel Foundation
- **Status**: Active

## Purpose

Governs the adaptation of the multi-panel workspace across device classes from ultrawide to phone. Ensures capability equivalence (not layout sameness) across all device classes.

## Doctrine

1. **Preserve capability, not layout sameness.** A phone user must have access to all five systems — just not simultaneously.
2. **Panel count adapts, panel power does not.** Compression reduces visible panels but never removes system functionality.
3. **Companion behavior is first-class.** On phone-class devices, the pinned companion and quick-switch mechanism are core navigation — not afterthoughts.
4. **Ultrawide must feel like a cockpit, not panel chaos.** More screen space means better composition, not more clutter.
5. **Saved-workspace readiness must be scaffolded.** The architecture must support named workspace presets without redesign.

## Truth Definition

Screen orchestration does not own truth. It governs the spatial arrangement and visibility of truth-presenting systems.

## Owned Scope

- Device class detection (ultrawide, desktop, laptop, tablet, phone)
- Panel visibility rules per device class
- Panel count limits
- Companion panel behavior
- Layout mode selection (full-cockpit, split, compact, single-companion)
- Workspace preset system (HERO_COCKPIT_DEFAULT)

## Non-Owned Scope

- Panel internal state (each panel owns its own)
- Active object identity (owned by KERN-CONTEXT-AND-TRUTH)
- Visual styling (owned by KERN-UI-PATTERN)

## Canonical Entities

- `DeviceOrchestrator` — device class detection and layout rules
- `DeviceLayout` — layout definition per device class
- `WorkspaceShell` — Dockview workspace implementation
- `CompanionSwitcher` — phone-class panel switching UI

## Invariants

1. Every device class must have a defined `DeviceLayout`.
2. `work` is always the primary panel across all device classes.
3. Phone-class layout must always have a companion panel defined.
4. Panel visibility changes must not destroy panel state.
5. Truth Echo must function across all device class transitions.

## Failure Conditions

- A device class has no defined layout → FAIL
- Phone has no companion switching mechanism → FAIL
- Ultrawide renders panels chaotically without composition → FAIL
- Device class change destroys active object identity → FAIL

## Success Definition

A user moving from desktop to phone (or vice versa) retains their active object context and can access all five systems with at most two actions. The workspace feels intentional at every screen size.

## Acceptance Tests

1. Five device classes are defined: ultrawide, desktop, laptop, tablet, phone
2. Ultrawide shows 5 panels in cockpit layout
3. Desktop shows 4 panels
4. Laptop shows 3 panels
5. Tablet shows 2 panels
6. Phone shows 1 panel with companion switcher
7. Active object survives device class changes
8. Phone companion switching works
