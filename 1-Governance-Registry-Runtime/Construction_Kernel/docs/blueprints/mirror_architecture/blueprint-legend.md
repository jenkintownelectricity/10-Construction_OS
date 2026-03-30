# Mirror Architecture — Blueprint Legend

> **MASTER DOCTRINE:** Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

---

## Color Definitions

| Color | Hex Code | Element | Meaning |
|-------|----------|---------|---------|
| **Blue** | `#2563EB` | Construction OS Core | The canonical platform — source of truth for all capabilities |
| **Purple** | `#7C3AED` | Mirror Kernel Nucleus | The control plane governing mirror lifecycle, parity, and drift |
| **Green** | `#059669` | Mirror Instances | Partner/domain-specific projections of kernel capabilities |
| **Orange** | `#D97706` | External Systems | Client systems, partner platforms, third-party integrations |
| **Red (dashed)** | `#DC2626` | Shield Boundary | Security and governance perimeter — nothing crosses unexamined |
| **Teal** | `#0D9488` | Slices | Capability units — the granularity of commercial attachment |
| **Light Blue** | `#7DD3FC` | Reflections | Atomic behavioral contracts — schemas, rules, fixtures |
| **Dark Gray** | `#374151` | Infrastructure | Supporting systems — registries, stores, pipelines |
| **Amber** | `#F59E0B` | Warnings/Drift | Parity degradation, drift alerts, review triggers |
| **Rose** | `#F43F5E` | Breakaway/Frozen | Detached or frozen elements — no longer actively maintained |

---

## Shape Definitions

| Shape | Element | Usage |
|-------|---------|-------|
| **Rounded Rectangle** | Systems & Services | Core platform, nucleus, registries, engines |
| **Rectangle** | Data & Artifacts | Schemas, contracts, fixtures, records |
| **Circle** | States & Decisions | Lifecycle states, decision points |
| **Diamond** | Decision Gates | Parity checks, promotion reviews, transfer gates |
| **Hexagon** | Slices | Capability groupings — emphasizes modularity |
| **Cylinder** | Data Stores | Registries, drift logs, parity databases |
| **Rounded Pill** | Actions & Processes | Compare, measure, promote, detach |
| **Dashed Rectangle** | Boundaries | Trust perimeters, shield zones, scope areas |

---

## Line Style Definitions

| Style | Meaning |
|-------|---------|
| **Solid Arrow** (`-->`) | Data flow — information moves in the arrow direction |
| **Dashed Arrow** (`--->`) | Control flow — governance, commands, lifecycle signals |
| **Thick Red Line** | Trust boundary — separates governed from ungoverned space |
| **Dotted Line** (`....>`) | Optional / conditional flow — may or may not be active |
| **Double Line** (`==>`) | Parity channel — continuous behavioral comparison |
| **Wavy Line** (`~~~>`) | Drift signal — parity degradation detected |

---

## Arrow Definitions

| Arrow Type | Meaning |
|------------|---------|
| **Filled Triangle (solid)** | Primary data flow |
| **Open Triangle (dashed)** | Control/governance signal |
| **Diamond Head** | Decision output — branch point |
| **Circle Head** | State transition — lifecycle movement |
| **Bar Head (`-|`)** | Termination — end of flow, boundary enforcement |

---

## Annotation Conventions

| Annotation | Meaning |
|------------|---------|
| `[P]` | Parity-tested — this reflection is under continuous behavioral comparison |
| `[D]` | Drift detected — parity has degraded; under review |
| `[F]` | Frozen — no longer actively maintained; read-only |
| `[T:class]` | Transfer class — e.g., `[T:HANDOFF_READY]` indicates transfer eligibility |
| `[S:state]` | Lifecycle state — e.g., `[S:ACTIVE]` indicates current mirror state |
| `v1.2.3` | Version tag — semantic version of a reflection or contract |

---

## Diagram Layout Conventions

1. **Core at center** — Construction OS Core always appears at the center or top of diagrams.
2. **Nucleus wraps core** — The Mirror Kernel Nucleus is shown as a layer around or adjacent to core.
3. **Mirrors at periphery** — Mirror instances appear around the outside, connected through the shield boundary.
4. **External systems beyond boundary** — Client/partner systems are always outside the trust boundary.
5. **Flow direction** — Primary flow reads left-to-right or top-to-bottom.
6. **State machines** — Read left-to-right for progression, with branches for alternate paths.

---

## Quick Reference Card

```
BLUE rounded-rect     = Construction OS Core
PURPLE rounded-rect   = Mirror Kernel Nucleus
GREEN rounded-rect    = Mirror Instance
ORANGE rounded-rect   = External System
RED dashed border     = Shield Boundary
TEAL hexagon          = Slice
LIGHT BLUE rectangle  = Reflection
SOLID arrow           = Data flows this way
DASHED arrow          = Control/governance signal
THICK RED line        = Trust boundary (do not cross ungoverned)
DIAMOND               = Decision gate
CIRCLE                = State node
CYLINDER              = Data store
```

---

*Blueprint Package — Construction OS Mirror Architecture*
*Master Doctrine: Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.*
