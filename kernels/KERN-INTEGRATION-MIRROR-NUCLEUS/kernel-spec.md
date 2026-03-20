# Kernel Specification: KERN-INTEGRATION-MIRROR-NUCLEUS

## Identification

| Field | Value |
|---|---|
| **Kernel ID** | KERN-INTEGRATION-MIRROR-NUCLEUS |
| **Version** | 1.0.0 |
| **Domain** | integration-mirror |
| **Created** | 2026-03-20 |
| **Status** | Active |
| **Owner** | Construction OS Platform Architecture |

## Purpose

This kernel exists to govern how Construction OS integrates with external systems. It establishes the mirror pattern as the sole sanctioned integration seam for external system connections where the mirror pattern is applicable. It defines the rules, structures, lifecycles, and constraints that ensure all integrations remain detachable, governed, and non-entangling.

The kernel prevents Construction OS from becoming dependent on any external system in a way that cannot be reversed. It ensures that external value can be reflected into the platform without corrupting or coupling with core truth.

## Scope

### In Scope

- Definition and governance of mirrors as integration surfaces
- Capability slice structure, declaration, and dependency management
- Reflection mechanics between source systems and Construction OS
- Parity verification through fixture-based evidence
- Drift detection, recording, and response
- Non-destructive breakaway processes
- Promotion of mirror reflections into Construction OS core
- Transfer classification and handoff readiness
- Trust boundary definition and enforcement
- Truth ownership assignment and tracking
- Mirror lifecycle state management
- Mirror validity enforcement
- Forbidden pattern detection and prevention

### Out of Scope

- Construction OS core domain model definitions (governed by domain kernels)
- Billing logic, tenant UI, authentication shell, customer dashboard behavior
- Application-layer presentation logic
- Infrastructure provisioning and deployment mechanics
- Source system internals (the mirror governs the boundary, not the source)

## Governed Entities

### Primary Entities

1. **Mirror** — A bounded, governed integration surface connecting Construction OS to an external source system. Each mirror has a manifest, lifecycle state, trust boundary, and set of enabled capability slices.

2. **Capability Slice** — A discrete, declared unit of functionality exposed by a mirror. Each slice has explicit inputs, outputs, dependencies, trust class, transfer class, and detachability level.

3. **Reflection** — The mechanism by which a mirror surfaces value from a source system. Reflections carry compatible truth but never directly mutate Construction OS canonical core truth.

4. **Parity Fixture** — A structured evidence artifact that verifies a mirror's reflection faithfully represents the source system's truth within declared tolerances.

5. **Drift Record** — A structured record documenting divergence between a mirror's reflection and its source system, including severity, detection method, and response.

6. **Trust Boundary** — An isolation barrier that separates mirror logic from Construction OS core internals, preventing contamination and coupling.

7. **Truth Ownership Assignment** — A machine-readable declaration of who owns truth for a specific domain area (Construction OS core, mirror, or shared).

8. **Mirror Manifest** — The machine-readable declaration file (`mirror-manifest.yaml`) that defines a mirror's identity, configuration, slices, and governance metadata.

### Secondary Entities

9. **Promotion Gate Record** — A record documenting a promotion decision, including all gate conditions and their pass/fail status.

10. **Transfer Gate Record** — A record documenting a transfer readiness assessment, including all gate conditions and their pass/fail status.

11. **Breakaway Plan** — A documented plan for non-destructive disconnection of a mirror, including fallback paths and reverse operations.

12. **Registry Entry** — The mirror's entry in the Construction OS integration registry, tracking lifecycle state transitions and governance events.

## Interfaces

### Inbound Interfaces

| Interface | Source | Purpose |
|---|---|---|
| Mirror Registration | Integration teams | Register new mirrors and update existing ones |
| Slice Declaration | Mirror developers | Declare capability slices with full dependency graphs |
| Parity Evidence Submission | QA / Integration teams | Submit fixture results proving parity |
| Drift Report Submission | Monitoring systems | Report detected drift between mirror and source |
| Promotion Request | Architecture team | Request promotion of a reflection into core |
| Transfer Assessment Request | Business / Legal team | Request transfer readiness assessment |

### Outbound Interfaces

| Interface | Target | Purpose |
|---|---|---|
| Registry State Updates | Construction OS Registry | Publish lifecycle state transitions |
| Validity Assessments | Integration teams | Return validity status per mirror |
| Parity Reports | QA dashboards | Publish parity verification results |
| Drift Alerts | Operations teams | Notify of detected drift events |
| Gate Decision Records | Audit trail | Publish promotion and transfer gate outcomes |

### Internal Interfaces

| Interface | Purpose |
|---|---|
| Manifest Validation | Validate mirror-manifest.yaml against schema |
| Dependency Graph Validation | Validate slice dependency graphs for completeness and forbidden references |
| Trust Boundary Verification | Verify isolation between mirror and core |
| Lifecycle State Machine | Enforce valid state transitions |

## Global Hard Constraints

The following constraints are absolute. No mirror, slice, process, or team may override them.

### GHC-01: Mirrors Are the Default Integration Seam
Mirrors are the default integration seam for external systems when the mirror pattern is applicable. Any external integration must use the mirror pattern unless a documented exception exists with architectural approval.

### GHC-02: No Direct Hard Coupling
Direct hard coupling that bypasses a mirror is forbidden. No code, configuration, or process may create a direct dependency between Construction OS core and an external system outside of a governed mirror boundary.

### GHC-03: Reflections May Not Mutate Core Truth
Mirrors may reflect compatible truth but may not directly mutate Construction OS canonical core truth. Reflections are read-project surfaces. Any write to core truth must go through a governed promotion gate.

### GHC-04: Non-Destructive Breakaway
Breakaway must always be non-destructive. Removing a mirror must never corrupt, delete, or render unusable any Construction OS core data, functionality, or configuration.

### GHC-05: Explicit Dependency Declaration
Capability slices must declare dependencies explicitly. No slice may have hidden, implicit, or undocumented dependencies on any system, service, or data source.

### GHC-06: Forbidden Internal Logic
Billing, tenant UI, auth shell, customer dashboard behavior, and presentation logic may never exist inside mirrors. These concerns belong exclusively to Construction OS core or its dedicated application layer.

### GHC-07: Promotion Requires Gate Pass
Promotion into core requires a promotion gate pass. All 7 promotion conditions must be met and recorded before any reflection may become part of Construction OS canonical core.

### GHC-08: Transfer Requires Gate Pass
Transfer or buyout classification requires a transfer gate pass. All 9 transfer conditions must be met and recorded before any slice may be classified as BUYOUT_READY or FULL_HANDOFF_READY.

### GHC-09: Machine-Readable Ownership
All ownership assignments must exist in machine-readable form. Human-only documentation of ownership is insufficient. The truth-ownership-matrix.yaml is the canonical source.

### GHC-10: Registry Lifecycle Tracking
Registry must track mirror lifecycle state transitions. Every transition from one lifecycle state to another must be recorded in the registry with timestamp, actor, and evidence reference.

### GHC-11: No Raw Code Sync
No raw code sync between systems is allowed. Code must flow through governed channels (mirrors, reflections) with declared contracts, never through direct repository synchronization or copy-paste.

### GHC-12: Parity Evidence Required for Active Mirrors
No ACTIVE mirror may exist without parity evidence. A mirror in ACTIVE state must have at least one passing parity fixture set.

### GHC-13: No Undeclared Mandatory Dependencies
No slice may create undeclared mandatory dependency outside its declared slice boundary. Any dependency that crosses the slice boundary must be listed in the slice declaration.

### GHC-14: Self-Contained Documentation
All docs and diagrams must be understandable without prior chat context. Every document in this kernel must be readable and comprehensible by someone who has not participated in any prior discussion about the kernel's creation.

## Versioning

This kernel follows semantic versioning:
- **Major** version changes indicate breaking changes to the kernel's governance model, constraint set, or entity definitions.
- **Minor** version changes indicate additions to the kernel that do not break existing compliance.
- **Patch** version changes indicate clarifications, typo fixes, or documentation improvements that do not change governance semantics.

## Amendment Process

Changes to this kernel require:
1. A written amendment proposal identifying the specific section(s) to change.
2. Impact assessment against all 14 global hard constraints.
3. Review by the Construction OS Platform Architecture team.
4. Verification that no existing ACTIVE mirror is invalidated without a migration path.
5. Version increment appropriate to the change scope.
6. Registry notification of the kernel version change.
