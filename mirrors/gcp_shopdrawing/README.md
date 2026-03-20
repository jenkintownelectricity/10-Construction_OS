# GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Version:** 1.0.0
**Lifecycle State:** STAGED (5 slices ACTIVE)
**Created:** 2026-03-20
**Owner:** construction_os_platform_team

---

## Doctrine

> Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

This mirror is the **first mirror instance** in the Construction Kernel. It establishes the architectural pattern that all subsequent mirrors will follow. Every design decision made here serves as precedent.

---

## What This Mirror Reflects

The GCP Shop Drawing Mirror reflects **shop drawing capabilities** from the General Contractor Platform (GCP) into Construction OS. Shop drawings are the detailed fabrication-level drawings produced by subcontractors and suppliers that show exactly how building components will be manufactured, assembled, and installed. They are the bridge between design intent and physical construction.

GCP maintains a mature shop drawing management pipeline that handles:

- Ingestion of shop drawings from dozens of trades and formats
- Normalization of detail conventions across disciplines (structural steel, mechanical, electrical, plumbing, fire protection)
- Rule-based validation against contract documents and building codes
- Approval workflow tracking with revision lineage
- Artifact packaging for fabrication release

This mirror does **not** import GCP's shop drawing system wholesale. It reflects specific capabilities through a controlled trust boundary, transforming them into Construction OS primitives that can be consumed by any downstream system, whether or not GCP remains the source.

---

## Active Slices

Five slices are currently **ACTIVE** and producing reflections:

| Slice | Purpose | Status |
|-------|---------|--------|
| `detail_normalization` | Normalizes shop drawing detail conventions across trades into a canonical Construction OS format | ACTIVE |
| `rules_engine` | Reflects GCP's shop drawing validation rules as declarative rule sets consumable by any validator | ACTIVE |
| `validation` | Provides validation results and conformance reports for shop drawing submissions | ACTIVE |
| `artifact_manifest` | Tracks the inventory of shop drawing artifacts, their formats, versions, and release states | ACTIVE |
| `lineage` | Maintains the revision history and approval chain for every shop drawing through its lifecycle | ACTIVE |

---

## Staged Slices

The following slices are defined but remain **STAGED** pending activation criteria:

| Slice | Purpose | Status |
|-------|---------|--------|
| `approval_workflow` | Reflects the multi-party approval process for shop drawings | STAGED |
| `rfi_linkage` | Links shop drawings to related Requests for Information | STAGED |
| `clash_detection` | Reflects spatial clash detection results involving shop drawing geometry | STAGED |
| `submittal_packaging` | Packages shop drawings into formal submittals with cover sheets and transmittals | STAGED |
| `trade_coordination` | Reflects cross-trade coordination status for interdependent shop drawings | STAGED |
| `fabrication_release` | Tracks the release-to-fabrication state of approved shop drawings | STAGED |
| `markup_capture` | Captures reviewer markups and annotations in a format-neutral representation | STAGED |
| `schedule_linkage` | Links shop drawing milestones to project schedule activities | STAGED |

---

## Architecture

```
+---------------------+          +---------------------------+          +-------------------+
|                     |          |   gcp_shopdrawing_boundary |          |                   |
|   GCP Source System |  ------> |   (Trust Boundary)         |  ------> |  Construction OS  |
|                     |          |                           |          |                   |
|  - Shop Drawings    |          |  detail_normalization     |          |  - Canonical Data |
|  - Rules            |          |  rules_engine             |          |  - OS Primitives  |
|  - Validations      |          |  validation               |          |  - Consumers      |
|  - Artifacts        |          |  artifact_manifest        |          |                   |
|  - History          |          |  lineage                  |          |                   |
+---------------------+          +---------------------------+          +-------------------+
```

Data flows left to right through the trust boundary. The trust boundary performs schema mediation: it accepts GCP-native formats on the ingress side and emits Construction OS canonical formats on the egress side. No GCP-native data structures leak past the boundary.

---

## Key Principles

1. **Reflection, Not Replication.** This mirror reflects capabilities, not raw data. GCP's internal schema, its database tables, its API contracts -- none of these are replicated. What crosses the boundary is a schema-mediated reflection of the capability.

2. **Detachable by Design.** If GCP is replaced tomorrow, every consumer of this mirror continues to function. The mirror contract is between Construction OS and the mirror interface, not between Construction OS and GCP.

3. **Non-Destructive Breakaway.** This mirror can be deactivated, detached, or replaced without data loss, service interruption, or schema migration on the Construction OS side. See `breakaway-conditions.md`.

4. **Sold by Capability.** Each slice represents a discrete capability that can be independently activated, deactivated, or replaced. Capabilities are not bundled.

5. **Trust Boundary Enforcement.** All data crossing the trust boundary is validated, transformed, and audited. There are no backdoors, no direct database connections, no shared-state shortcuts.

---

## File Index

| File | Purpose |
|------|---------|
| `mirror-manifest.yaml` | Machine-readable mirror definition |
| `relationship-charter.md` | Relationship terms between Construction OS and GCP |
| `source-system-profile.md` | Profile of the GCP source system |
| `scope.md` | What this mirror covers |
| `exclusions.md` | What this mirror explicitly excludes |
| `trust-boundary.md` | Trust boundary definition and data flow rules |
| `breakaway-conditions.md` | Conditions and procedures for mirror breakaway |
| `promotion-candidates.md` | Reflections that may be promoted to OS core |
| `sync-policy.md` | Data synchronization policy |
| `mirror-blueprint-notes.md` | Notes for blueprint visualization |
| `reflection-inventory.yaml` | Inventory of all reflections |
| `slice-dependency-graph.json` | Dependency graph between slices |
| `mirror-activation-checklist.md` | Activation checklist (L0.6 validity) |
| `parity-baseline.yaml` | Baseline parity measurements |

---

## Quick Start

1. Review the `mirror-manifest.yaml` for the machine-readable mirror definition.
2. Read `scope.md` and `exclusions.md` to understand boundaries.
3. Check `reflection-inventory.yaml` for the current state of all reflections.
4. Consult `trust-boundary.md` before designing any integration.
5. Run the activation checklist in `mirror-activation-checklist.md` before promoting any slice from STAGED to ACTIVE.
