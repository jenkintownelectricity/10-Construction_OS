# Chemistry Kernel Object Model Overview

## Core Object Graph

The chemistry kernel organizes truth into a directed graph of typed objects.

```
Chemical System
  ├── polymer_base → Polymer Family
  ├── additives[] → Additive
  ├── cure_mechanism_ref → Cure Mechanism
  ├── solvent_system_ref → Solvent System
  └── material_refs[] → (external: Material Kernel)

Adhesion Rule
  ├── chemistry_ref → Chemical System
  ├── primer_ref → Chemical System
  └── evidence_refs[] → Evidence Linkage

Incompatibility Rule
  ├── chemistry_a_ref → Chemical System
  ├── chemistry_b_ref → Chemical System
  └── evidence_refs[] → Evidence Linkage

Degradation Mechanism
  ├── chemistry_ref → Chemical System
  └── evidence_refs[] → Evidence Linkage

Chemical Hazard Record
  └── chemistry_ref → Chemical System
```

## Object Identity

Every object has a typed ID prefix:
- `CSYS-` — Chemical System
- `PFAM-` — Polymer Family
- `ADTV-` — Additive
- `CURE-` — Cure Mechanism
- `SOLV-` — Solvent System
- `ADHR-` — Adhesion Rule
- `INCP-` — Incompatibility Rule
- `DEGR-` — Degradation Mechanism
- `HAZR-` — Chemical Hazard Record

## Status Lifecycle

All objects follow: `draft` → `active` → `deprecated`

- **draft**: Under review, not consumable by downstream systems
- **active**: Verified, evidence-linked, available for consumption
- **deprecated**: Superseded or invalidated, retained for lineage

## Schema Validation

Every object type has a corresponding JSON Schema in `schemas/`. All schemas enforce `additionalProperties: false` and declare required fields. The shared `chemistry_family` enum is consistent across all schemas that reference it.

## Cross-Kernel References

References to objects in other kernels use string IDs with kernel-prefix convention:
- `MAT-xxx` — Material Kernel reference
- `SPEC-xxx` — Specification Kernel reference
- `ASSY-xxx` — Assembly Kernel reference
