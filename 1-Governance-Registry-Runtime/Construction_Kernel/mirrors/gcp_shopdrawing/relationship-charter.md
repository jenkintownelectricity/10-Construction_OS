# Relationship Charter: Construction OS and GCP

**Mirror ID:** `gcp_shopdrawing`
**Version:** 1.0.0
**Effective Date:** 2026-03-20
**Parties:** Construction OS Platform Team, GCP (General Contractor Platform)

---

## Doctrine

> Connected by mirrors, never hard-wired. Sold by capability, detachable by design. Cooperate without entanglement.

This charter defines the terms of the relationship between Construction OS and GCP as mediated through the `gcp_shopdrawing` mirror. It is not a legal contract. It is an architectural agreement that governs how these two systems cooperate without becoming entangled.

---

## 1. Nature of the Relationship

Construction OS and GCP are **independent systems** that cooperate through a mirror interface. The relationship is characterized by:

- **Cooperation, not integration.** The systems share capabilities through a defined boundary. Neither system reaches into the other's internals.
- **Reflection, not dependency.** Construction OS reflects GCP's shop drawing capabilities. It does not depend on GCP's availability, schema, or implementation choices for its own operation.
- **Symmetry of exit.** Either party can terminate the mirror relationship without causing damage to the other. Construction OS can replace the mirror source. GCP can revoke access. Neither action causes data loss or architectural collapse.

This is not a parent-child relationship. It is not a primary-replica relationship. It is a peer cooperation mediated by a controlled reflection boundary.

---

## 2. What Is Shared

The following capabilities are shared through the mirror, subject to trust boundary enforcement:

### 2.1 Shop Drawing Detail Normalization
GCP shares its ability to normalize shop drawing details across construction trades. Construction OS receives these as canonical detail records that are independent of GCP's internal representation.

**Shared:** Normalized detail records, trade classifications, detail type taxonomies, convention mappings.
**Not Shared:** GCP's normalization algorithms, internal processing pipelines, or proprietary heuristics.

### 2.2 Validation Rules
GCP shares its shop drawing validation rules in a declarative format. Construction OS receives these as vendor-neutral rule sets.

**Shared:** Rule definitions, rule categories, severity levels, applicability conditions.
**Not Shared:** GCP's rule execution engine, performance optimizations, or rule authoring tools.

### 2.3 Validation Results
GCP shares validation outcomes for shop drawing submissions. Construction OS receives these as conformance reports.

**Shared:** Pass/fail status, violation details, applicable rule references, remediation guidance.
**Not Shared:** GCP's validation execution internals, caching strategies, or partial evaluation states.

### 2.4 Artifact Inventory
GCP shares the inventory of shop drawing artifacts. Construction OS receives these as artifact manifest records.

**Shared:** Artifact identifiers, format metadata, version numbers, release states, file references.
**Not Shared:** GCP's file storage implementation, CDN configuration, or access control internals.

### 2.5 Revision Lineage
GCP shares the revision history and approval chain for shop drawings. Construction OS receives these as lineage records.

**Shared:** Revision identifiers, timestamps, actor references, approval states, change descriptions.
**Not Shared:** GCP's workflow engine state, notification history, or internal user profiles.

---

## 3. What Is Isolated

The following are explicitly isolated and never cross the mirror boundary:

| Isolated Concern | Rationale |
|-------------------|-----------|
| Authentication and authorization | Each system manages its own identity. No shared auth tokens, sessions, or identity providers. |
| Billing and payment | Financial data never crosses the mirror. Each system bills independently. |
| User interface and presentation | GCP's UI is not reflected. Construction OS presents data through its own interfaces. |
| Tenant configuration | GCP's multi-tenancy model is opaque to Construction OS. Tenant boundaries are respected but not imported. |
| Internal messaging and events | GCP's internal event bus, message queues, and notification systems are not exposed. |
| Performance and scaling internals | How GCP scales, caches, or optimizes is its own concern. |
| Error handling internals | GCP's error recovery, retry logic, and circuit breaker configurations are not shared. |

---

## 4. Obligations

### 4.1 Construction OS Obligations
- Treat reflected data as a capability snapshot, not a live database view.
- Never attempt to write back to GCP through the mirror. Mirrors are read-reflections.
- Maintain parity baselines and alert on drift. Do not silently consume degraded reflections.
- Honor the trust boundary. Do not attempt to extract data outside the defined scope.
- Maintain breakaway readiness at all times. Never build features that cannot survive mirror detachment.

### 4.2 GCP Obligations (as Source System)
- Provide data in the agreed ingress format at the agreed synchronization interval.
- Signal schema changes with reasonable lead time. Breaking changes require a deprecation period.
- Maintain data quality at the source. The mirror does not compensate for source data corruption.
- Respect the scope boundary. Do not push data outside the agreed reflection scope.

### 4.3 Mutual Obligations
- Neither party introduces hard-wired dependencies on the other's internals.
- Schema changes are communicated, not discovered through breakage.
- Both parties maintain independent operational capability. The failure of one system does not cascade to the other.

---

## 5. Dispute Resolution

If the mirror produces inconsistent, degraded, or unexpected results:

1. **Drift detection fires.** The drift monitoring system identifies the discrepancy.
2. **Parity check runs.** The parity verification system quantifies the deviation.
3. **Source investigation.** The platform team investigates whether the drift originates at GCP (source change), the trust boundary (mediation error), or Construction OS (consumer misinterpretation).
4. **Remediation.** The responsible party corrects the issue. If the issue is at the boundary, both parties collaborate on the fix.
5. **Baseline update.** If the drift represents an intentional change, the parity baseline is updated.

---

## 6. Relationship Lifecycle

| State | Description |
|-------|-------------|
| PROPOSED | Mirror relationship is under discussion. No data flows. |
| CHARTERED | This charter is agreed. Integration work begins. |
| STAGED | Mirror is defined, slices are being activated incrementally. **Current state.** |
| ACTIVE | All required slices are active and producing reflections. |
| DEGRADED | One or more slices have drifted beyond tolerance. Remediation underway. |
| SUSPENDED | Mirror is temporarily suspended. No data flows. State is preserved. |
| BREAKING_AWAY | Breakaway procedure is in progress. See `breakaway-conditions.md`. |
| DETACHED | Mirror is fully detached. No residual dependencies. |

---

## 7. Review Schedule

This charter is reviewed:
- When a new slice is promoted from STAGED to ACTIVE.
- When the mirror moves between lifecycle states.
- Quarterly, regardless of state changes.
- Immediately if a breakaway condition is triggered.

---

## 8. Signatories

This is an architectural agreement, recorded here for alignment:

- **Construction OS Platform Team** — Responsible for mirror definition, trust boundary, and consumer-side integrity.
- **GCP Integration Liaison** — Responsible for source-side data quality, schema stability, and access provision.
