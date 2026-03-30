# Kernel-to-Reference Intelligence Map — Construction Assembly Kernel

## Purpose

Maps the specific data flows between this kernel and the Construction_Reference_Intelligence layer.

## Data Flow Direction

Assembly Kernel -> Reference Intelligence (read-only)

The intelligence layer reads assembly truth. It does not write to or modify assembly records.

## Objects Consumed by Intelligence Layer

| Kernel Object | Intelligence Use Case |
|---|---|
| assembly_system | Pattern analysis: identify common vs. unusual layer stack configurations |
| assembly_system.climate_context | Climate-correlated assembly performance analysis |
| assembly_system.geometry_context | Geometry-correlated failure pattern identification |
| transition_condition | Interface risk intelligence: failure rates by transition type |
| transition_condition.risk_level | Risk distribution analysis across project portfolio |
| penetration_condition | Seal method effectiveness analysis by penetration type |
| penetration_condition.control_layers_affected | Control-layer vulnerability mapping at penetrations |
| tested_assembly_record | Test coverage gap analysis: which assemblies lack validation |
| tested_assembly_record.result | Compliance trend analysis |
| continuity_requirement | Requirement vs. reality gap detection |
| edge_condition | Edge failure correlation with wind exposure data |
| tie_in_condition | New-to-existing transition success/failure patterns |

## Intelligence Outputs That Reference Assembly Data

The intelligence layer may produce:
- Failure pattern reports referencing specific assembly_system configurations
- Interface risk scores aggregated from transition and penetration conditions
- Test coverage maps identifying untested assembly types
- Climate-assembly correlation reports
- Continuity gap alerts when assemblies violate continuity requirements

These outputs reference assembly records by ID. They do not modify kernel truth.

## Shared Vocabulary

Both this kernel and the intelligence layer use the same shared registries:
- Control layer IDs (11 values)
- Interface zone IDs (10 values)
- Risk levels (4 values)
- Evidence types (10 values)
- Lifecycle stages (8 values)

This shared vocabulary ensures semantic alignment without data duplication.

## Coordination Protocol

1. Intelligence layer queries are read-only against kernel data
2. Intelligence findings that suggest kernel record errors are reported as proposals, not direct edits
3. New shared enum values require coordinated update through the shared registry
