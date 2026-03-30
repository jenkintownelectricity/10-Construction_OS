# Ontology: Mirror Kernel Nucleus

This document defines the key concepts used throughout the Mirror Kernel Nucleus. Every term listed here has a precise meaning within this kernel. These definitions are authoritative — if a term is used differently elsewhere, the definition here governs within the integration-mirror domain.

---

## Mirror

A **mirror** is a bounded, governed integration surface that connects Construction OS to exactly one external source system. A mirror is not a connector, adapter, or plugin — it is a governed boundary with its own lifecycle, trust rules, and evidence requirements.

A mirror reflects value from the source system into Construction OS without creating hard-wired dependencies. It is declared through a manifest (`mirror-manifest.yaml`), tracked in the registry, and subject to all kernel governance rules.

**Key properties:**
- Has exactly one source system
- Has a declared trust boundary
- Has a lifecycle state (PROPOSED through RETIRED)
- Contains one or more capability slices
- Must have parity evidence to be ACTIVE
- Can be broken away non-destructively at any time

**A mirror is NOT:**
- A raw API wrapper
- A database synchronization channel
- A shared library
- An embedded SDK
- A direct code dependency

---

## Reflection

A **reflection** is the mechanism by which a mirror surfaces value from a source system into the Construction OS ecosystem. A reflection carries compatible truth — information that has been translated from the source system's concepts into Construction OS-compatible forms.

Reflections are read-directional from the perspective of Construction OS core. A reflection makes external information available for use, but it does not write to or mutate Construction OS canonical core truth. If a reflection proves valuable enough to become part of core, it must go through the promotion gate.

**Key properties:**
- Carries compatible truth, not identical truth
- Is read-only from core's perspective
- Has a declared status (ACTIVE, STALE, UNAVAILABLE, SUSPENDED)
- Is verifiable through parity fixtures
- May be promoted into core through the promotion gate

---

## Capability Slice

A **capability slice** (or simply "slice") is a discrete, declared unit of functionality exposed by a mirror. Slices are the atomic unit of capability governance. Each slice has its own identity, purpose, inputs, outputs, dependencies, trust class, transfer class, and detachability level.

Slices are how mirrors are sold, enabled, disabled, and detached. A customer may purchase or enable individual slices without taking the entire mirror. A slice may be detached without affecting other slices in the same mirror, provided dependency declarations are honored.

**Key properties:**
- Has a unique slice ID within its mirror
- Declares all dependencies explicitly
- Has a detachability level
- Has a transfer class
- May be independently enabled or disabled
- Must be individually governable

---

## Parity

**Parity** is the verified state in which a mirror's reflection faithfully represents the source system's truth within declared tolerances. Parity is not identity — a mirror does not need to be a perfect copy of the source system. It needs to accurately reflect the aspects it claims to reflect, within the tolerances it declares.

Parity is measured through fixtures — structured test artifacts that compare the mirror's reflection against the source system's actual state. Parity is not assumed; it is proven.

**Parity levels:**
- **FULL_PARITY** — All declared reflection points verified within tolerance
- **PARTIAL_PARITY** — Some reflection points verified, others pending or out of tolerance
- **NO_PARITY** — No parity evidence exists or all fixtures are failing
- **PARITY_UNKNOWN** — Parity has not been assessed

---

## Drift

**Drift** is the condition in which a mirror's reflection diverges from its source system's actual state beyond declared tolerances. Drift is not inherently a failure — source systems change, and some temporary drift is expected. However, drift must be detected, recorded, and responded to within governed timeframes.

Drift is the opposite of parity. Where parity says "the reflection matches the source," drift says "the reflection no longer matches the source." Drift detection is continuous; parity verification is periodic.

**Drift severity levels:**
- **CRITICAL** — Core business decisions may be affected by the divergence
- **HIGH** — Significant divergence that requires prompt attention
- **MEDIUM** — Noticeable divergence within operational tolerance
- **LOW** — Minor divergence with no immediate business impact
- **INFORMATIONAL** — Detected change that may or may not constitute meaningful drift

---

## Breakaway

**Breakaway** is the process of disconnecting a mirror from Construction OS. Breakaway is always non-destructive — it must never corrupt, delete, or render unusable any Construction OS core data, functionality, or configuration.

Breakaway is not an emergency procedure. It is a designed-in capability that every mirror must support from day one. The ability to break away is a first-class requirement, not an afterthought.

**Key properties:**
- Always non-destructive to Construction OS core
- Must be documented with specific steps and fallback paths
- Must have a bounded cost (time, effort, risk)
- Must be testable before execution
- May be partial (individual slices) or complete (entire mirror)

---

## Promotion

**Promotion** is the controlled process by which a proven mirror reflection is elevated into Construction OS canonical core truth. Promotion moves a concept from "external value reflected through a mirror" to "native Construction OS capability."

Promotion is irreversible in the sense that once something becomes core, it is governed by core rules, not mirror rules. However, promotion is gated — it requires passing all 7 promotion gate conditions. Promotion is never automatic; it is always an explicit, recorded decision.

**Key properties:**
- Requires passing all 7 promotion gate conditions
- Must be explicitly approved and recorded
- Transfers ownership from mirror to core
- Is irreversible (promoted concepts become core-governed)
- Must document breakaway cost and reverse-path even after promotion

---

## Transfer

**Transfer** is the classification and potential handoff of a mirror or slice to another party. Transfer classes range from NON_TRANSFERABLE (cannot be handed off) to FULL_HANDOFF_READY (can be completely handed over to another party with all necessary documentation, tests, and isolation).

Transfer readiness is gated — a slice may only be classified as BUYOUT_READY or FULL_HANDOFF_READY after passing all 9 transfer gate conditions.

**Transfer classes:**
- **NON_TRANSFERABLE** — Cannot be handed off to another party
- **LICENSE_ONLY** — May be licensed for use but not transferred
- **WHITE_LABELABLE** — May be rebranded and resold under another name
- **BUYOUT_READY** — May be purchased and owned by another party
- **FULL_HANDOFF_READY** — May be completely handed over with all artifacts

---

## Trust Boundary

A **trust boundary** is an isolation barrier that separates mirror logic from Construction OS core internals. Trust boundaries prevent contamination (mirror concepts leaking into core) and coupling (core depending on mirror internals).

Trust boundaries are not just conceptual — they must be enforced through architecture, code structure, and runtime isolation. A trust boundary defines what a mirror can access, what it cannot access, and how data crosses the boundary.

**Key properties:**
- Defines the isolation perimeter around a mirror
- Specifies what data may cross the boundary and in what direction
- Must be documented in the mirror manifest
- Must be verifiable through inspection or automated checks
- Prevents both inward contamination (mirror to core) and outward leakage (core internals to mirror)

---

## Registry

The **registry** is the central record of all mirrors, their lifecycle states, and their governance events. The registry is the system of record for mirror existence and state. If a mirror is not in the registry, it does not officially exist within Construction OS governance.

**Key properties:**
- Tracks all mirror lifecycle state transitions
- Records governance events (promotion decisions, transfer assessments, breakaway executions)
- Is the authoritative source for "what mirrors exist and what state are they in"
- Must be updated for every state transition with timestamp, actor, and evidence reference

---

## Fixture

A **fixture** is a structured test artifact used to verify parity between a mirror's reflection and its source system. Fixtures are the evidence that a mirror works correctly. They are not unit tests or integration tests in the traditional sense — they are parity verification instruments.

**Key properties:**
- Compares mirror reflection against source system state
- Has a declared tolerance (how much divergence is acceptable)
- Produces a pass/fail result with details
- Must exist for every ACTIVE mirror (no ACTIVE mirror without parity fixtures)
- Are versioned and tracked alongside the mirror

---

## Shield

A **shield** is a protective mechanism within a trust boundary that prevents specific categories of violation. Shields are the enforcement layer of trust boundaries. Where a trust boundary defines the perimeter, shields enforce specific rules at that perimeter.

Examples of shields:
- **Write shield** — Prevents a mirror from writing to core tables
- **Import shield** — Prevents core code from importing mirror modules
- **Dependency shield** — Prevents undeclared dependencies from crossing the boundary
- **Logic shield** — Prevents forbidden logic categories (billing, auth, tenant UI) from existing in the mirror

---

## Summary Table

| Concept | One-Line Definition |
|---|---|
| Mirror | Governed integration boundary connecting Construction OS to one external system |
| Reflection | Mechanism by which a mirror surfaces compatible truth from a source system |
| Capability Slice | Discrete, declared unit of functionality exposed by a mirror |
| Parity | Verified state where reflection faithfully represents source within tolerance |
| Drift | Divergence between reflection and source beyond declared tolerance |
| Breakaway | Non-destructive disconnection of a mirror from Construction OS |
| Promotion | Controlled elevation of a mirror reflection into Construction OS core |
| Transfer | Classification and potential handoff of a mirror or slice to another party |
| Trust Boundary | Isolation barrier separating mirror logic from core internals |
| Registry | Central record of all mirrors, states, and governance events |
| Fixture | Structured test artifact for parity verification |
| Shield | Protective enforcement mechanism within a trust boundary |
