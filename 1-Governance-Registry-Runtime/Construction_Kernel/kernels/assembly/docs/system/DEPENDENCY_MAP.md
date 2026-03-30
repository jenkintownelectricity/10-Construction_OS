# Dependency Map — Construction Assembly Kernel

## Purpose

Documents all external dependencies consumed by this kernel and all downstream systems that consume this kernel's truth.

## Upstream Dependencies (This Kernel Consumes)

### Construction_Reference_Intelligence — Shared Artifacts

| Artifact | Path | Usage |
|---|---|---|
| Control Layer Registry | `shared/control_layers.json` | All `control_layer_id` fields reference these 11 IDs |
| Interface Zone Registry | `shared/interface_zones.json` | All `interface_zone` fields reference these 10 IDs |
| Shared Enum Registry | `shared/shared_enum_registry.json` | Lifecycle stages, climate flags, geometry contexts, risk levels, confidence levels |
| Shared Standards Registry | `shared/shared_standards_registry.json` | Standards reference IDs (IBC, NFPA_285, ASHRAE_90_1, etc.) |
| Shared Evidence Registry | `shared/shared_evidence_registry.json` | Evidence type classifications |
| Shared Risk Registry | `shared/shared_risk_registry.json` | Risk categories and severity levels |
| Shared Taxonomy | `shared/shared_taxonomy.json` | Taxonomy field definitions and allowed values |
| Division 07 Posture | `shared/division_07_posture.json` | CSI Division 07 subsection definitions |

### Construction_Material_Kernel — Material References

- `material_ref` fields in `assembly_layer` and `assembly_component` schemas resolve to material entries in the Material Kernel.
- This kernel does not store material properties. It references material identity only.

### Construction_Specification_Kernel — Specification References

- `spec_ref` fields in `assembly_component` schemas resolve to specification entries in the Specification Kernel.
- This kernel does not store specification requirements. It references specification identity only.

## Downstream Consumers (Consume This Kernel's Truth)

### Construction_Reference_Intelligence

- Reads assembly systems, transitions, penetrations, tested assembly records, and continuity requirements.
- Uses assembly truth for cross-domain intelligence, pattern analysis, and failure correlation.

### Construction_Scope_Kernel

- References assembly system IDs when delineating scope boundaries.
- Assembly transitions may define scope handoff points between trades.

## No Runtime Dependencies

This kernel has no runtime dependencies. It is a static truth store. All references are resolved by identifier lookup, not by API call or network request.

## Dependency Health Checks

| Dependency | Validation Method |
|---|---|
| Shared enum values | Schema validation ensures enum fields match shared registry values |
| Control layer IDs | Schema enum constraints or validation against shared registry |
| Interface zone IDs | Schema enum constraints or validation against shared registry |
| Material references | Deferred: validated when cross-kernel queries are executed |
| Specification references | Deferred: validated when cross-kernel queries are executed |
