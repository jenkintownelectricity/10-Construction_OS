# KERN-INTEGRATION-MIRROR-NUCLEUS

**Kernel ID:** KERN-INTEGRATION-MIRROR-NUCLEUS
**Version:** 1.0.0
**Domain:** integration-mirror
**Status:** Active
**Created:** 2026-03-20

---

## Purpose

The Mirror Kernel Nucleus is the foundational governance kernel for all external system integrations within Construction OS. It defines how Construction OS connects to, reflects value from, and detaches from external systems without ever creating hard-wired dependencies.

Every external integration in Construction OS is modeled as a **mirror** — a bounded, governed, detachable integration surface that reflects compatible truth from a source system into the Construction OS ecosystem. Mirrors are never hard-wired. They are sold by capability, detachable by design, and cooperate with Construction OS without entanglement.

## Master Doctrine

> Connected by mirrors, never hard-wired.
> Sold by capability, detachable by design.
> Cooperate without entanglement.

This doctrine governs every decision made within this kernel's scope. Any integration pattern, architecture choice, or operational decision that violates this doctrine is invalid.

## What This Kernel Governs

1. **Mirror Lifecycle** — The full lifecycle of mirrors from proposal through retirement, including all state transitions and evidence requirements.
2. **Capability Slices** — The discrete units of functionality that mirrors expose, including their dependency declarations, trust classifications, and detachability guarantees.
3. **Reflections** — The mechanism by which mirrors surface value from source systems into Construction OS without mutating core truth.
4. **Parity** — The verification system that ensures mirrors faithfully represent their source systems, measured through fixtures.
5. **Drift Detection** — The system for identifying when a mirror's reflection diverges from its source of truth.
6. **Breakaway** — The non-destructive disconnection process that allows any mirror to be removed without damaging Construction OS core.
7. **Promotion Gates** — The controlled process by which proven mirror reflections may be elevated into Construction OS core.
8. **Transfer Gates** — The classification and validation system for mirrors or slices that may be handed off, licensed, or sold.
9. **Trust Boundaries** — The isolation barriers that prevent mirror logic from contaminating or coupling with Construction OS core internals.
10. **Truth Ownership** — The explicit assignment of who owns truth for each domain area, preventing ownership ambiguity.

## What This Kernel Does NOT Govern

- Billing logic, tenant UI, auth shell, customer dashboard behavior, and presentation logic. These are explicitly forbidden from existing inside mirrors.
- Application-local UX logic.
- Core Construction OS domain models (those are governed by their respective domain kernels).

## Key Artifacts

| Artifact | Purpose |
|---|---|
| `kernel-spec.md` | Full kernel specification |
| `doctrine.md` | Master doctrine with rationale and anti-patterns |
| `ontology.md` | Definitions of all key concepts |
| `mirror-lifecycle.md` | Lifecycle states and transition rules |
| `status-model.md` | Status model for mirrors and slices |
| `capability-slice-model.md` | Capability slice structure and attachment rules |
| `reflection-model.md` | Reflection mechanics and statuses |
| `parity-model.md` | Parity measurement and fixture system |
| `drift-model.md` | Drift detection and response |
| `breakaway-model.md` | Non-destructive breakaway process |
| `promotion-model.md` | Promotion gate rules and process |
| `transfer-model.md` | Transfer classifications and gate rules |
| `trust-boundary-model.md` | Trust boundary isolation model |
| `mirror-blueprint-principles.md` | Visual and conceptual diagram principles |
| `mirror-manifest.schema.json` | JSON Schema for mirror manifests |
| `truth-ownership-matrix.yaml` | Truth ownership assignments |
| `mirror-validity-rules.md` | 12 invalidity rules |
| `promotion-gate.md` | 7 promotion conditions |
| `transfer-gate.md` | 9 transfer conditions |
| `forbidden-patterns.md` | 10 forbidden patterns |

## Global Hard Constraints

This kernel enforces 14 global hard constraints that apply to all mirrors, slices, reflections, and related artifacts. These constraints are non-negotiable and cannot be overridden by any mirror, team, or process. They are documented in full in `kernel-spec.md` and referenced throughout all subordinate documents.

## How to Read This Kernel

1. Start with this README for orientation.
2. Read `doctrine.md` to understand the governing philosophy.
3. Read `ontology.md` to learn the vocabulary.
4. Read `kernel-spec.md` for the complete specification.
5. Read the model files (`mirror-lifecycle.md`, `capability-slice-model.md`, etc.) for detailed mechanics.
6. Review `mirror-validity-rules.md`, `promotion-gate.md`, `transfer-gate.md`, and `forbidden-patterns.md` for enforcement rules.
7. Use `mirror-manifest.schema.json` and `truth-ownership-matrix.yaml` as machine-readable references when building or validating mirrors.

## Ownership

This kernel is owned by the Construction OS Platform Architecture team. Changes to this kernel require a kernel amendment review. Mirror-specific decisions are owned by the mirror's declared owner as recorded in the mirror manifest.
