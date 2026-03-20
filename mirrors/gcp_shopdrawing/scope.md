# Scope: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Version:** 1.0.0
**Last Updated:** 2026-03-20

---

## Doctrine

> Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

---

## 1. Purpose of This Document

This document defines what the `gcp_shopdrawing` mirror covers. Anything not explicitly listed here is out of scope. When in doubt, check `exclusions.md` for items that are explicitly excluded. If something appears in neither document, it is out of scope by default.

---

## 2. Scope Summary

This mirror reflects **shop drawing management capabilities** from GCP into Construction OS. It covers the normalization, validation, tracking, and lineage of shop drawings as construction documents. It does not cover GCP's broader project management capabilities, and it does not cover the business processes that surround shop drawings (procurement, scheduling, cost allocation).

---

## 3. In-Scope Capabilities

### 3.1 Detail Normalization (ACTIVE)

The mirror reflects GCP's ability to normalize shop drawing details across construction trades.

**Included:**
- Canonical detail records with trade-neutral structure and trade-specific extensions
- Trade classification taxonomy (structural, mechanical, electrical, plumbing, fire protection, architectural, civil)
- Detail type classification (connection detail, schedule, layout, section, elevation, isometric, diagram, schematic)
- Convention mappings that translate trade-specific notation into canonical form
- Normalization confidence scores indicating extraction reliability
- Format metadata for source drawings (file type, resolution, scale, sheet size)

**Boundary:** Normalization produces canonical records. The algorithms and heuristics that produce them are not reflected. Construction OS receives the output, not the process.

### 3.2 Rules Engine (ACTIVE)

The mirror reflects GCP's shop drawing validation rules as declarative, vendor-neutral rule sets.

**Included:**
- Rule definitions expressed in a declarative format (condition-action pairs)
- Rule categorization by trade, severity (critical, major, minor, advisory), and phase
- Rule applicability conditions (which drawings, trades, and project types a rule applies to)
- Rule versioning with effective dates and deprecation markers
- Rule groupings (code-based, specification-based, standard-based, project-specific)
- Rule metadata (source reference, rationale, remediation guidance)

**Boundary:** Rules are reflected as declarative definitions. GCP's rule execution engine, optimization strategies, and evaluation ordering are not reflected. Any compliant rule evaluator can consume these rules.

### 3.3 Validation (ACTIVE)

The mirror reflects validation results and conformance reports for shop drawing submissions.

**Included:**
- Validation result records (pass, fail, warning, info) per drawing per rule
- Conformance reports aggregating results by drawing, by trade, by severity
- Violation details including the specific rule violated, the location in the drawing, and the nature of the violation
- Remediation guidance attached to violations
- Validation timestamps and the rule version used for evaluation
- Batch validation summaries for submittal packages

**Boundary:** Validation results are reflected as structured data. The validation execution pipeline, its performance characteristics, and its internal state are not reflected.

### 3.4 Artifact Manifest (ACTIVE)

The mirror reflects the inventory of shop drawing artifacts managed by GCP.

**Included:**
- Artifact identifiers (unique within the mirror scope)
- Artifact type classification (drawing, calculation, certification, data sheet, transmittal, markup)
- Format metadata (file type, file size, page count, resolution)
- Version numbers and version history
- Release state (draft, submitted, under_review, approved, approved_as_noted, revise_and_resubmit, rejected, released_for_fabrication)
- Relationships between artifacts (drawing-to-calculation, drawing-to-certification, drawing-to-markup)
- Artifact groupings (submittal packages, revision sets)

**Boundary:** The manifest tracks metadata about artifacts. The artifacts themselves (the actual files) are referenced by URI but not stored within the mirror. File storage, CDN, and access control for the actual files remain GCP's responsibility.

### 3.5 Lineage (ACTIVE)

The mirror reflects the revision history and approval chain for shop drawings.

**Included:**
- Revision chain records (ordered sequence of revisions per drawing)
- Revision metadata (timestamp, change description, change trigger)
- Approval chain records (who reviewed, decision, timestamp, comments)
- Approval roles (architect, engineer of record, owner's representative, general contractor, subcontractor)
- Change provenance (what caused the revision: markup, RFI, design change, code violation, coordination issue)
- Lineage graph relationships (supersedes, split_from, merged_into, derived_from)
- Drawing lifecycle state transitions with timestamps

**Boundary:** Lineage records are reflected as structured data. GCP's workflow engine, notification system, and approval routing logic are not reflected.

---

## 4. Cross-Cutting Scope Elements

These elements apply across all in-scope capabilities:

### 4.1 Trade Coverage
All construction trades supported by GCP's shop drawing system are in scope for reflection:
- Structural steel and concrete
- Mechanical (HVAC, piping)
- Electrical (power, low-voltage, communications)
- Plumbing
- Fire protection
- Architectural (envelope, interiors, finishes)
- Civil and sitework

### 4.2 Project Types
Shop drawings from all GCP project types are in scope:
- Commercial (office, retail, hospitality)
- Institutional (healthcare, education, government)
- Industrial (manufacturing, warehousing, data centers)
- Residential (multi-family)
- Infrastructure (transportation, utilities)

### 4.3 Data Granularity
Reflections operate at the **individual shop drawing** level. Every distinct drawing in GCP's system is a distinct record in the mirror. Aggregations (by project, by trade, by phase) are computed on the Construction OS side from individual records.

### 4.4 Temporal Scope
- **Historical data:** The mirror can reflect historical shop drawings from active and archived GCP projects, subject to GCP's data retention policies.
- **Current data:** Active shop drawings are reflected on the sync schedule defined in `sync-policy.md`.
- **Future data:** New shop drawings are captured at the next sync cycle after they appear in GCP.

---

## 5. Scope Boundaries

| Boundary | Inside | Outside |
|----------|--------|---------|
| Data type | Shop drawing metadata and structured records | Raw drawing files (referenced by URI only) |
| Process | Normalization outputs, validation results, lineage records | Normalization algorithms, validation execution, workflow engines |
| Trades | All trades with shop drawing activity | Trades without shop drawing conventions (e.g., landscaping soft costs) |
| Lifecycle | From submission through fabrication release | Pre-submission drafting, post-fabrication field verification |
| Systems | GCP shop drawing subsystem only | GCP scheduling, cost, field ops, or other subsystems |

---

## 6. Scope Change Process

To expand or contract the scope of this mirror:

1. **Propose** the scope change with rationale in a scope amendment document.
2. **Assess** the impact on existing slices, trust boundary, and downstream consumers.
3. **Review** with the Construction OS platform team and GCP integration liaison.
4. **Update** this document, the `mirror-manifest.yaml`, and the `reflection-inventory.yaml`.
5. **Validate** that the trust boundary configuration accommodates the change.
6. **Communicate** the change to all registered consumers of this mirror's reflections.

Scope changes that add new slices follow the standard slice activation process documented in `mirror-activation-checklist.md`.
