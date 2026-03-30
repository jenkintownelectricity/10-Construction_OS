# Reference Intelligence Linkage — Construction Assembly Kernel

## Relationship

The Construction_Reference_Intelligence layer reads assembly truth from this kernel. It does not write to or modify assembly records. The intelligence layer observes, annotates, and reasons across kernel truth surfaces — but assembly truth remains authoritative here.

## Direction of Data Flow

```
Construction_Assembly_Kernel (assembly truth)
        |
        | reads via pointer references
        v
Construction_Reference_Intelligence (cross-domain intelligence)
```

The intelligence layer may:
- Read assembly system configurations to identify failure-prone patterns
- Read transition and penetration conditions to assess interface risk
- Read tested assembly records to identify coverage gaps
- Read continuity requirements to flag inconsistencies across assemblies
- Correlate assembly data with material, chemistry, and specification truth from sibling kernels

The intelligence layer may NOT:
- Modify assembly records
- Override assembly truth with intelligence-derived conclusions
- Insert records into this kernel
- Redefine enums, control layers, or interface zones consumed by this kernel

## What the Intelligence Layer Consumes

| Assembly Object | Intelligence Use |
|---|---|
| assembly_system | Pattern analysis: common vs. unusual configurations, failure-correlated layer stacks |
| transition_condition | Interface risk intelligence: which transitions fail most, under what conditions |
| penetration_condition | Penetration failure patterns: seal method effectiveness by penetration type |
| tested_assembly_record | Test coverage analysis: which assemblies lack test validation |
| continuity_requirement | Continuity gap detection: requirements vs. actual assembly configurations |
| edge_condition | Edge failure intelligence: wind uplift correlations, edge detail effectiveness |

## Shared Artifacts

Both this kernel and the intelligence layer consume shared artifacts from `Construction_Reference_Intelligence/shared/`:

- `control_layers.json` — 11 control-layer definitions
- `interface_zones.json` — 10 interface zone definitions
- `shared_enum_registry.json` — shared enum values
- `shared_standards_registry.json` — standards reference registry
- `shared_evidence_registry.json` — evidence type classifications
- `shared_risk_registry.json` — risk category definitions

This kernel references these by pointer (see `shared/SHARED_ARTIFACTS_POINTER.md`). It never duplicates them.

## Cross-Kernel Correlation Points

The intelligence layer correlates assembly truth with sibling kernels:

| Sibling Kernel | Correlation Point |
|---|---|
| Material Kernel | `material_ref` in assembly layers resolves to material properties |
| Chemistry Kernel | Material compatibility questions at layer interfaces |
| Specification Kernel | `spec_ref` in components resolves to specification requirements |
| Scope Kernel | Assembly scope boundaries map to scope-of-work delineations |
