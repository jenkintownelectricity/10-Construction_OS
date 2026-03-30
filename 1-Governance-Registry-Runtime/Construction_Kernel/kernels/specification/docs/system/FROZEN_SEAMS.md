# Frozen Seams — Construction Specification Kernel

## Frozen Schema Versions

All schemas in this kernel are versioned and frozen per baseline. The current baseline is `construction-kernel-pass-2` with schema version `v1`.

## What Is Frozen

### Schema Definitions

Every JSON Schema file in `schemas/` is frozen at the current baseline version. Changes to schema structure (adding required fields, modifying enums, changing type constraints) require a new schema version and a new baseline.

| Schema File | Version | Status |
|---|---|---|
| specification_entry.schema.json | v1 | frozen |
| specification_document.schema.json | v1 | frozen |
| specification_section.schema.json | v1 | frozen |
| source_pointer.schema.json | v1 | frozen |
| requirement.schema.json | v1 | frozen |
| prohibition.schema.json | v1 | frozen |
| allowance.schema.json | v1 | frozen |
| requirement_condition.schema.json | v1 | frozen |
| reference_standard.schema.json | v1 | frozen |
| submittal_requirement.schema.json | v1 | frozen |
| qualification_requirement.schema.json | v1 | frozen |
| warranty_requirement.schema.json | v1 | frozen |
| testing_requirement.schema.json | v1 | frozen |
| specification_revision.schema.json | v1 | frozen |

### Shared Artifact References

The shared artifacts consumed from `Construction_Reference_Intelligence/shared/` are treated as immutable at the time of baseline freeze. If shared artifacts are updated in the intelligence layer, this kernel's baseline must be re-evaluated and potentially re-frozen.

Frozen shared artifact references:
- `control_layers.json` — 11 control layers
- `interface_zones.json` — 10 interface zones
- `shared_enum_registry.json` — lifecycle stages, climate flags, geometry contexts, evidence types, control layer IDs, interface zone IDs
- `shared_standards_registry.json` — IBC, ASTM, AAMA, NFPA_285, ASHRAE_90_1, WBDG, UFGS, CSI_MASTERFORMAT, ISO_13788
- `shared_taxonomy.json` — shared taxonomy fields

## Versioning Rules

1. Schema version is a `const` field in every schema — records self-declare their version
2. Adding optional fields to a schema is a minor change and may be done within the same version with documentation
3. Adding required fields, removing fields, or changing enum values requires a version increment
4. Version increments freeze the previous version — old records remain valid under their declared version
5. No schema version is ever deleted

## Baseline Advancement

A new baseline is created when schema versions advance. The baseline freeze process:

1. All schemas are finalized and validated
2. `state/BASELINE_STATE.json` is updated with new baseline identifier
3. Previous baseline schemas are archived
4. All existing records must validate against their declared schema version
