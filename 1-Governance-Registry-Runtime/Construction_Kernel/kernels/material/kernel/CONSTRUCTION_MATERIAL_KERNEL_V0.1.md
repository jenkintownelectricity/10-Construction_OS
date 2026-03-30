# Construction Material Kernel — V0.1

## Kernel Identity

| Field | Value |
|---|---|
| Kernel ID | KERN-CONST-MATL |
| Version | 0.1 |
| Family | construction-kernel |
| Role | material-kernel |
| Domain | CSI Division 07 — Building Envelope Systems |
| Status | Active |
| Baseline | construction-kernel-pass-2 |

## Purpose

The Construction Material Kernel is the canonical source of material-domain truth for the construction-kernel family. It characterizes building envelope materials by their physical properties, tested performance, compatibility relationships, weathering behavior, and hygrothermal properties.

## Object Registry

| Object Type | Schema | Description |
|---|---|---|
| Material Class | material_class.schema.json | Taxonomy classification by composition family |
| Material Form | material_form.schema.json | Physical delivery form of a material class |
| Material Property | material_property.schema.json | Single measured physical property |
| Material Performance | material_performance.schema.json | Aggregate performance record |
| Compatibility Record | material_compatibility_record.schema.json | Pairwise material compatibility |
| Weathering Behavior | weathering_behavior.schema.json | Degradation under environmental exposure |
| Hygrothermal Property | hygrothermal_property.schema.json | Moisture transport and thermal-moisture properties |
| Standards Reference | material_standard_reference.schema.json | ASTM test method citation |
| Material Entry | material_entry.schema.json | General material fact record |

## Governance Rules

1. All records conform to JSON Schema 2020-12 with `additionalProperties: false`
2. All property values require test method references and evidence pointers
3. Active records are immutable; changes create new revisions
4. Materials are characterized by physical properties, never by brand name
5. Missing data defaults to fail-closed (flagged and blocked)
6. Enum values sourced from shared family registries

## Truth Surface

- Material classes and taxonomy
- Material forms and physical delivery
- Physical properties with units and test methods
- Compatibility matrices (compatible, incompatible, conditional, untested)
- Weathering behavior under environmental exposure
- Hygrothermal properties at stated conditions
- Material-to-control-layer mappings
- Standards references (citation only)
- Evidence linkages to test reports and TDS

## Kernel Boundaries

Does not own: specification truth, assembly truth, chemistry truth, scope truth, reference intelligence. See `docs/doctrine/truth-boundary.md` for complete boundary definition.

## Version History

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-03-17 | Initial kernel structure — full object model, schemas, contracts |
