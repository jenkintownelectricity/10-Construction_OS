# Family Dependency Posture — Construction Scope Kernel

## Purpose

This map documents the Construction Scope Kernel's dependencies on shared artifacts and sibling kernels within the construction-kernel family.

## Dependency Classification

Dependencies are classified as:
- **Owns** — This kernel is the authoritative source.
- **Reads** — This kernel references but does not own.
- **None** — No dependency exists.

## Shared Artifact Dependencies

| Artifact | Dependency | Source |
|----------|------------|--------|
| Interface zone identifiers | Reads | Shared registry |
| Control layer taxonomy | Reads | Shared registry |
| CSI MasterFormat sections | Reads | Industry standard |
| ASTM/AAMA test method refs | Reads | Standards Kernel |

## Sibling Kernel Dependencies

| Sibling Kernel | Dependency | Nature |
|----------------|------------|--------|
| Construction Detail Kernel | Reads | Scope references detail assemblies by ID |
| Construction QA Kernel | Reads | Scope references test methods by ID |
| Construction Standards Kernel | Reads | Scope references code sections by number |
| Construction Scheduling Kernel | None | Scope defines sequence; scheduling owns calendar |

## What This Kernel Owns

- Scope boundary definitions (inclusions, exclusions).
- Trade responsibility assignments.
- Work operation definitions within scope.
- Inspection step requirements and hold points.
- Commissioning step definitions.
- Closeout requirement definitions.
- Warranty handoff records.

## Dependency Rules

- This kernel MUST NOT import runtime logic from any dependency.
- This kernel MUST NOT embed objects from sibling kernels; it references by ID only.
- Shared artifact changes MUST be coordinated across all consuming kernels.
- If a shared artifact is unavailable, scope records remain valid but unresolved references are flagged.

## Versioning Posture

- Schema version "v1" is the current version across the family.
- Version upgrades MUST be coordinated with sibling kernels to maintain reference compatibility.
- Breaking changes require a new schema_version value and migration documentation.

## Isolation Guarantee

- The scope kernel can operate independently of all sibling kernels.
- Missing sibling kernel data does not invalidate scope truth records.
- Cross-kernel validation is performed at integration time, not at record creation time.
