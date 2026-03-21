# TRIAD-01 — Boundary Rules

## Principle

Each kernel owns a clearly bounded scope. No kernel may override, duplicate, or contradict another kernel's owned scope.

## Boundary Definitions

### KERN-UI-PATTERN owns:
- Visual composition and quality standards
- Color, typography, spacing tokens
- Dashboard drift prevention
- First-frame impression standards
- Truth Echo visual language (animation, indicators)
- **Does NOT own**: which panels are visible, what data is shown, or when ingredients appear

### KERN-SCREEN-ORCHESTRATION owns:
- Device class detection and definitions
- Panel count and visibility per device class
- Layout modes (full-cockpit, split, compact, single-companion)
- Companion panel assignment
- Workspace preset system
- **Does NOT own**: panel internal state, visual quality, or active object identity

### KERN-CONTEXT-AND-TRUTH owns:
- Active object identity (one at a time, or fail closed)
- Truth Echo propagation and failure semantics
- Source basis tracking (canonical, derived, draft, compare, mock)
- Compare state
- State ownership model (6 layers)
- **Does NOT own**: visual presentation of truth, panel layout, or ingredient placement

### KERN-INGREDIENT-PLACEMENT-OPTIONALITY owns:
- Ingredient classification (persistent, contextual, system, optional)
- Placement rules per ingredient class
- Clutter prevention rules
- **Does NOT own**: ingredient content, visual styling, or layout mechanics

## Conflict Resolution

If two kernels appear to govern the same concept:
1. Determine which kernel *owns* the concept per the boundary definitions above.
2. The owning kernel's rules take precedence.
3. The non-owning kernel must defer and adapt.

## Cross-Boundary Contracts

Kernels communicate through:
- **Typed event contracts** (EventMap in `src/ui/contracts/events.ts`)
- **Typed adapter contracts** (in `src/ui/contracts/adapters.ts`)
- **State store interface** (activeObjectStore)
- **Panel registry** (PanelRegistry with declared subscriptions and emissions)

No kernel may communicate through undocumented side channels.
