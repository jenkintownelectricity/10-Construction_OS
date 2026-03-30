# Entity Relationship Map

## Purpose

Documents all chemistry kernel entities and their relationships.

## Entities

1. **Chemical System** — The central entity. A formulated product or material system.
2. **Chemistry Entry** — A general-purpose chemistry fact record.
3. **Polymer Family** — Classification of polymer chemistry groups.
4. **Additive** — Chemical additives used in formulated systems.
5. **Cure Mechanism** — The curing process for a chemical system.
6. **Solvent System** — The carrier or solvent classification for a chemical system.
7. **Adhesion Rule** — Adhesion relationship between a chemistry and a substrate.
8. **Incompatibility Rule** — Adverse interaction between two chemistries.
9. **Degradation Mechanism** — Deterioration process for a chemistry under environmental stress.
10. **Chemical Hazard Record** — Hazard classification for a chemistry system.

## Relationships

```
Chemical System
  ├── chemistry_family ──> Polymer Family (by enum value)
  ├── cure_mechanism_ref ──> Cure Mechanism (by mechanism_id)
  ├── solvent_system_ref ──> Solvent System (by system_id)
  ├── additives ──> Additive (by additive_id, array)
  └── material_refs ──> [External] Construction_Material_Kernel

Adhesion Rule
  ├── chemistry_ref ──> Chemical System (by system_id)
  ├── primer_ref ──> Chemical System (by system_id)
  └── test_method_ref ──> [External] Standards reference

Incompatibility Rule
  ├── chemistry_a_ref ──> Chemical System (by system_id)
  └── chemistry_b_ref ──> Chemical System (by system_id)

Degradation Mechanism
  └── chemistry_ref ──> Chemical System (by system_id)

Chemical Hazard Record
  └── chemistry_ref ──> Chemical System (by system_id)
```

## Reference Conventions

- All cross-references use string IDs, never embedded objects.
- External references point to sibling kernels or standards by convention.
- Evidence references (`evidence_refs`) link to lab tests, field observations, or manufacturer data.

## Cardinality

- A chemical system may have zero or one cure mechanism reference.
- A chemical system may have zero or one solvent system reference.
- A chemical system may have zero or many additive references.
- Multiple adhesion rules may reference the same chemical system.
- Incompatibility rules always reference exactly two chemistry systems.
- Multiple degradation mechanisms may reference the same chemistry.
