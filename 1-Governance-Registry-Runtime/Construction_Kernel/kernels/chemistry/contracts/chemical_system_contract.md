# Chemical System Contract

## Purpose

Defines the validation rules and structural requirements for chemical system records in the Construction Chemistry Kernel. A chemical system record represents a formulated product or material system defined by its chemistry family, cure mechanism, and solvent system.

## Required Fields

- `schema_version` — Must be `"v1"`.
- `system_id` — Unique identifier, prefixed `CHEM-SYS-`.
- `title` — Human-readable name for the chemical system.
- `chemistry_family` — Must be one of the defined chemistry family enum values.
- `system_type` — Must be one of: sealant, adhesive, coating, primer, cleaner, membrane_component.
- `status` — Must be one of: active, draft, deprecated.

## Validation Rules

1. Every chemical system must validate against `schemas/chemical_system.schema.json`.
2. `system_id` must be unique across all chemical system records.
3. If `cure_mechanism_ref` is provided, it must reference a valid cure mechanism record.
4. If `solvent_system_ref` is provided, it must reference a valid solvent system record.
5. If `material_refs` are provided, each must reference a valid material entry in Construction_Material_Kernel.
6. `voc_g_per_l` must be a non-negative number when present.
7. No additional properties beyond those defined in the schema are permitted.

## Consumers

- Adhesion rule evaluation references chemical systems by `system_id`.
- Incompatibility checks cross-reference chemistry families.
- Inspection workflows verify that installed products match their declared chemical system.

## Change Policy

Schema changes require version increment. Deprecated records must not be deleted; set `status` to `"deprecated"`.
