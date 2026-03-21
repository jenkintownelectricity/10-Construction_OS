# KERN-INGREDIENT-PLACEMENT-OPTIONALITY — Ingredient Placement Kernel

## Metadata
- **Kernel ID**: KERN-INGREDIENT-PLACEMENT-OPTIONALITY
- **Version**: 1.0.0
- **Wave**: UI Kernel Foundation
- **Status**: Active

## Purpose

Governs what must persist, what may be contextual, what belongs in mailbox/system surfaces, and what should remain optional. Prevents clutter and bad ingredient placement.

## Doctrine

1. **Not everything belongs on screen at all times.** Persistent ingredients must earn their place by being operationally essential.
2. **Context-sensitive ingredients appear when relevant.** Reference data, validation results, and spatial context should intensify when the active object warrants them — and recede when it doesn't.
3. **Mailbox/system ingredients live in the System panel.** Tasks, proposals, alerts, and activity logs have a home — they must not leak into other panels as clutter.
4. **Optional ingredients must not masquerade as essential.** Voice, artifact generation, and compare mode are powerful but optional — they should be available but not default-visible.

## Truth Definition

This kernel does not own truth. It governs where truth-presenting ingredients are placed within the cockpit layout.

## Owned Scope

- Classification of UI ingredients as persistent, contextual, system, or optional
- Placement rules for each ingredient class
- Clutter prevention rules

## Non-Owned Scope

- Ingredient content (owned by adapters and panels)
- Layout mechanics (owned by KERN-SCREEN-ORCHESTRATION)
- Visual treatment (owned by KERN-UI-PATTERN)

## Ingredient Classification

### Persistent (always visible when workspace is open)
- Active object identity bar
- Explorer tree (or quick-access on phone)
- Work surface
- System status indicator (header bar)
- MOCK adapter warning

### Contextual (visible when relevant to active object)
- Reference entries for active object
- Validation status for active object
- Spatial highlight for active object
- Compare view (only in compare mode)

### System (lives in System panel)
- Validation history
- Tasks
- Proposals
- Activity log
- Alerts
- Truth Echo failures

### Optional (available but not default-visible)
- Voice adapter interface
- Artifact generation
- Compare mode
- Layer visibility toggles (Spatial)

## Invariants

1. No persistent ingredient may be hidden on any device class.
2. Contextual ingredients must not persist when no object is selected.
3. System ingredients must not leak outside the System panel.
4. Optional ingredients must be reachable within two actions.

## Failure Conditions

- Persistent ingredient missing from any device class → FAIL
- System notifications appearing in Work or Explorer → FAIL
- Optional feature consuming default screen space → FAIL
- Contextual data persisting after object deselection → FAIL

## Success Definition

The workspace feels calm and structured. The right information appears at the right time. Nothing fights for attention that shouldn't be there.

## Acceptance Tests

1. Active object bar is visible when an object is selected
2. MOCK indicator is visible when mock adapters are used
3. Reference panel shows references only for the active object
4. System panel contains all system-level ingredients
5. Compare mode is not visible by default
6. Voice adapter is available but not default-visible
