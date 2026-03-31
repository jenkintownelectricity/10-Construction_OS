# Manufacturer Hub — Surface Intent

## Dual-Surface Design

The Manufacturer Hub implements a **dual operational surface** that changes the cognitive posture of the workspace — not just the color scheme.

### WORK Surface (Light)
- **Purpose**: Office work, submittal review, admin cognition
- **Visual**: Light backgrounds, high-contrast readable text, card-based layouts
- **Panels**: Overview, Products list, Systems list with certification badges
- **Posture**: Document review, data entry, administrative workflow

### SYSTEM Surface (Dark)
- **Purpose**: System reasoning, visualization, inspection cognition
- **Visual**: Dark control-tower aesthetic matching Construction OS core
- **Panels**: System Inspector, Product Stack, Certification Status, Condition Compatibility, Rule Checklist
- **Posture**: Technical investigation, layer analysis, rule validation

## Why This Is Not a Theme Toggle

A theme toggle changes colors. This mode switch changes **what panels are shown** and **how the user thinks about the data**:

- WORK mode shows manufacturer-centric, office-friendly panels
- SYSTEM mode shows system-centric, inspection-focused panels
- The mode switch is explicitly labeled **WORK | SYSTEM**, never Light | Dark
- Both modes share the same selected manufacturer and system state

## Observer-Derived Projection Rule

All data displayed in the Manufacturer Hub is an **observer-derived projection** of manufacturer truth. The canonical truth lives in:

- `10-building-envelope-manufacturer-os` (manufacturer registry)
- `00-ValidKernel-Registry` (root registry)

The local projection file (`manufacturerHubObserverProjection.ts`) is explicitly marked as non-canonical and must not invent unsupported truth.

## No Runtime Engine in This Wave

Wave 1 builds the UI surface only. There is no:
- Certification execution engine
- Rule evaluation runtime
- Signal bus emission
- Schema mutation

All validation states (`certified`, `unverified`, `partial`, `blocked`) are observer-derived presentational states, not engine-executed truth.

## Governance vs Action Color Separation

- **Governance family** (gold/amber): certification state, projection state, truth debt, seed status
- **Action family** (blue): inspect, navigate, mode-switch, future actions

This color separation is **presentational only** — no new truth is invented by color.
