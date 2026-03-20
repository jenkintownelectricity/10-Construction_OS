# Mirror Architecture — Blueprint Overview

> **MASTER DOCTRINE:** Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

---

## What Is the Mirror Architecture?

The Mirror Architecture is Construction OS's structural pattern for extending platform capabilities to external partners, clients, and systems **without creating hard dependencies**. Instead of integrating directly into a partner's stack or allowing partners to integrate directly into ours, we project **mirrors** — controlled, versioned, contractually-bound reflections of kernel capabilities that can be attached, measured, transferred, or detached cleanly.

A mirror is not a copy. It is not a fork. It is a **governed projection** — a living reflection of specific kernel capabilities that maintains parity with its source while remaining structurally independent.

---

## Why It Exists

Construction technology platforms face a fundamental tension:

1. **Partners need deep capability** — validation engines, governance rules, generation pipelines — to deliver value.
2. **Hard integration creates entanglement** — when a partner's system depends on internal kernel APIs, schema internals, or undocumented behaviors, both sides lose autonomy.
3. **Clean exits must be possible** — business relationships change; the architecture must support graceful detachment without catastrophic failure on either side.

The Mirror Architecture resolves this tension. It provides deep capability through **slices**, maintains quality through **parity testing**, and guarantees clean separation through **transfer and breakaway** protocols.

---

## How It Works

### The Layered Model

```
Construction OS Core
  └── Mirror Kernel Nucleus
        └── Mirror Instance (per partner/project/domain)
              └── Slice (per capability area)
                    └── Reflection (per contract/schema/rule/fixture)
```

1. **Construction OS Core** contains the canonical implementations — the source of truth for all governance, validation, generation, and engine logic.

2. **Mirror Kernel Nucleus** is the control plane that governs mirror lifecycle, enforces parity, manages drift, and controls promotion/breakaway decisions.

3. **Mirror Instances** are partner- or domain-specific projections. Each mirror contains a curated subset of kernel capabilities relevant to that engagement.

4. **Slices** are the unit of attachment. A client can take one slice (e.g., validation only) or many (governance + engine + generation). Slices are independently attachable and detachable.

5. **Reflections** are the atomic elements within a slice — individual contracts, schemas, rules, and fixtures that define exact behavior expectations.

### The Lifecycle

Every mirror follows a governed lifecycle:

| State | Meaning |
|-------|---------|
| **PROPOSED** | Mirror requested; scope under review |
| **CHARTERED** | Scope approved; slices defined; contracts drafted |
| **STAGED** | Reflections loaded; parity testing in progress |
| **ACTIVE** | Mirror live; parity maintained; drift monitored |
| **FROZEN** | Mirror locked; no new reflections; maintenance only |
| **RETIRED** | Mirror decommissioned; transfer complete or breakaway executed |

### The Parity Loop

Every active mirror runs a continuous parity loop:

1. **Fixture Input** — canonical test fixtures from the kernel
2. **Source Behavior** — kernel produces expected output
3. **Mirror Behavior** — mirror produces its output
4. **Compare** — behavioral diff analysis
5. **Parity Result** — PASS, DRIFT, or BREAK
6. **Drift Record** — logged, measured, reviewed
7. **Decision** — promote stable reflections inward, or break away incompatible ones outward

---

## Key Concepts

### Mirror
A governed projection of kernel capabilities scoped to a specific partner, project, or domain. Not a fork — a living, measured reflection.

### Reflection
The atomic unit within a mirror. A single contract, schema, rule, or fixture that defines an exact behavioral expectation. Reflections are versioned, tested, and tracked.

### Slice
The unit of commercial and technical attachment. A slice groups related reflections into a capability area (e.g., "validation," "governance," "generation"). Clients attach at the slice level.

### Parity
The measure of behavioral equivalence between a kernel capability and its mirror reflection. Parity is tested continuously using fixtures. 100% parity means the mirror behaves identically to the source.

### Drift
When parity degrades — when a mirror's behavior diverges from its source. Drift is not inherently bad; it is **measured, recorded, and governed**. Small drift may be acceptable. Large drift triggers review.

### Breakaway
The controlled separation of a mirror reflection that has diverged too far from its source, or that serves a partner-specific need incompatible with the kernel. Breakaway freezes the reflection and detaches it cleanly.

### Promotion
The opposite of breakaway. When a mirror reflection proves stable, reusable, and valuable, it may be promoted **inward** — absorbed into the kernel as a canonical capability available to all mirrors.

### Transfer
The governed handoff of mirror capabilities to a partner. Transfer classes range from NON_TRANSFERABLE (core IP, never leaves) to FULL_HANDOFF_READY (partner can take it and run independently).

---

## How to Read the Blueprints

The blueprint package contains:

| Document | Purpose |
|----------|---------|
| **blueprint-legend.md** | Color, shape, and line definitions for all diagrams |
| **blueprint-system-context.svg** | Highest-level view: core, nucleus, mirrors, external systems |
| **blueprint-kernel-to-mirror.svg** | Hierarchical relationship: nucleus → mirrors → slices → reflections |
| **blueprint-slice-attachment-model.svg** | Mix-and-match capability attachment |
| **blueprint-parity-drift-loop.svg** | Continuous parity testing cycle |
| **blueprint-registry-control-plane.svg** | Lifecycle state machine and control plane |
| **blueprint-promotion-vs-breakaway.svg** | Two paths: inward promotion vs outward breakaway |
| **blueprint-transfer-buyout-path.svg** | Transfer classes and clean exit protocol |
| **blueprint-gcp-mirror-instance.svg** | Concrete example: GCP Shop Drawing mirror |
| **mirror-architecture-one-page.html** | All-in-one viewable summary |

**Reading order for newcomers:**
1. This overview
2. The legend
3. System context diagram
4. Kernel-to-mirror hierarchy
5. Slice attachment model
6. Everything else in any order

**Reading order for partners:**
1. This overview
2. Slice attachment model
3. Transfer/buyout path
4. Parity drift loop
5. GCP mirror instance (as concrete example)

---

## Governing Principles

1. **Mirrors, not wires.** We never expose internal kernel APIs. We project governed reflections.
2. **Slices, not monoliths.** Clients take exactly what they need. Nothing more.
3. **Parity, not trust.** We don't assume mirrors behave correctly. We measure continuously.
4. **Drift, not failure.** Divergence is expected. It is governed, not punished.
5. **Exits, not traps.** Every attachment has a clean detachment path. Always.
6. **Promotion, not accumulation.** Good ideas flow inward. The kernel gets better from every engagement.

---

*Blueprint Package — Construction OS Mirror Architecture*
*Master Doctrine: Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.*
