# KERN-UI-PATTERN — UI Pattern Kernel

## Metadata
- **Kernel ID**: KERN-UI-PATTERN
- **Version**: 1.0.0
- **Wave**: UI Kernel Foundation
- **Status**: Active
- **Owner**: Construction OS UI Foundation

## Purpose

Governs the visible interface patterns of Construction OS. Enforces live-system framing, premium workstation aesthetics, and sought-after presentation quality. Forbids generic dashboard drift.

## Doctrine

1. **Panels are live systems, not passive views.** Every visible panel must contain real state, real interactions, and real event participation.
2. **The workspace is a cockpit, not a dashboard.** The composition must convey operational command, not administrative overview.
3. **Clarity, seriousness, and desirability are non-negotiable.** Every surface must feel premium, structured, and technically potent.
4. **Generic dashboard drift is forbidden.** No card grids, no metric tiles, no fake AI sparkle, no decorative motion.
5. **The Hero Cockpit principle governs first-frame impression.** When the workspace loads, it must immediately communicate power and structure.
6. **Work/Context/Intelligence depth hierarchy must be visible.** The strongest live systems (Work, Spatial) visually dominate. Context systems (Explorer, Reference) support. Intelligence systems (System) persist.

## Truth Definition

The UI Pattern Kernel does not own canonical truth. It governs how truth is *presented* — ensuring that mock data is visually distinguished from canonical data, draft state is never confused with validated state, and source basis is always visible.

## Owned Scope

- Visual composition patterns
- Panel framing rules
- First-frame impression standard
- Dashboard drift prevention
- Premium presentation enforcement
- Work/Context/Intelligence depth hierarchy

## Non-Owned Scope

- Canonical data truth (owned by truth-source adapters)
- Event routing (owned by Event Bus)
- Active object identity (owned by KERN-CONTEXT-AND-TRUTH)
- Panel layout rules (owned by KERN-SCREEN-ORCHESTRATION)

## Canonical Entities

- `PanelShell` — common panel wrapper enforcing visual standards
- `tokens` — design token system
- `GlobalStyles` — CSS foundation

## Invariants

1. No panel may render without a PanelShell wrapper showing its identity, source basis, and mock status.
2. No panel may use generic card-grid or tile composition as its primary layout.
3. Mock data must always display a visible MOCK indicator.
4. Source basis (canonical, derived, draft, compare, mock) must be visible in panel chrome.
5. The workspace must never resemble a generic admin SaaS application.

## Failure Conditions

- A panel renders without source basis visibility → FAIL
- A mock adapter is used without MOCK label → FAIL
- The workspace composition looks like a generic dashboard → FAIL
- Decorative elements without functional value are added → FAIL

## Success Definition

The workspace immediately communicates: "This is a professional construction operating environment where real work happens in live interconnected systems." A new user should feel operational capability, not administrative overview.

## Acceptance Tests

1. Each panel shows its identity and source basis in the header
2. Mock adapters display MOCK labels
3. The workspace uses dark, structured, premium visual treatment
4. Work panel is visually dominant (center-of-gravity)
5. No generic card grids or dashboard tiles exist
6. Typography uses the Inter/JetBrains Mono system
7. Color palette conveys technical seriousness (dark blue-gray base)
