# Family Dependency Posture — Construction Assembly Kernel

## Purpose

Assesses this kernel's dependency health within the construction-kernel family.

## Dependency Classification

### Hard Dependencies (Required for Schema Validation)

| Dependency | Source | Impact if Missing |
|---|---|---|
| Control layer IDs | shared/control_layers.json | Cannot validate control_layer_id fields |
| Interface zone IDs | shared/interface_zones.json | Cannot validate interface_zone fields |
| Status enum | Internal schema | Cannot validate record status |
| Assembly type enum | Internal schema | Cannot validate assembly classification |

### Soft Dependencies (Required for Full Resolution)

| Dependency | Source | Impact if Missing |
|---|---|---|
| Material entries | Construction_Material_Kernel | material_ref cannot be resolved; assembly records remain valid but incomplete |
| Specification entries | Construction_Specification_Kernel | spec_ref cannot be resolved |
| Standards registry | shared/shared_standards_registry.json | test_standard_ref cannot be validated against registry |

### Advisory Dependencies (Enrich but Not Required)

| Dependency | Source | Impact if Missing |
|---|---|---|
| Evidence registry | shared/shared_evidence_registry.json | Evidence type classification unavailable |
| Risk registry | shared/shared_risk_registry.json | Risk category definitions unavailable |
| Taxonomy | shared/shared_taxonomy.json | Shared field definitions unavailable |

## Dependency Health Assessment

| Dependency | Status | Risk |
|---|---|---|
| Shared control layers | Available | Low — stable, frozen |
| Shared interface zones | Available | Low — stable, frozen |
| Shared enum registry | Available | Low — stable |
| Shared standards registry | Available | Low — append-only |
| Material Kernel | Not yet populated | Medium — material_ref resolution deferred |
| Specification Kernel | Not yet populated | Medium — spec_ref resolution deferred |
| Chemistry Kernel | No direct dependency | None |
| Scope Kernel | No direct dependency | None |

## Mitigation Posture

- Hard dependencies are frozen seams with change protocols documented in `docs/system/FROZEN_SEAMS.md`
- Soft dependencies use deferred validation: references are syntactically valid but resolution is deferred until sibling kernels are populated
- Advisory dependencies are informational; their absence does not affect kernel operation
