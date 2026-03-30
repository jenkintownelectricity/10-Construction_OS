# Dependency Map — Construction Material Kernel

## Purpose

This document maps all dependencies for the Construction Material Kernel — what it depends on and what depends on it.

## Inbound Dependencies (This Kernel Depends On)

| Source | Artifact | Dependency Type |
|---|---|---|
| Construction_Reference_Intelligence | shared/shared_enum_registry.json | Enum vocabulary source |
| Construction_Reference_Intelligence | shared/shared_taxonomy.json | Material class taxonomy |
| Construction_Reference_Intelligence | shared/shared_standards_registry.json | Standards citation format |
| Construction_Reference_Intelligence | shared/control_layers.json | Control layer registry |
| Construction_Reference_Intelligence | shared/interface_zones.json | Interface zone registry |
| Construction_Reference_Intelligence | shared/division_07_posture.json | Division 07 domain alignment |

## Outbound Dependencies (Other Systems Depend On This Kernel)

| Consumer | Data Consumed | Contract |
|---|---|---|
| Construction_Specification_Kernel | Material property values for spec requirements | material_property_contract |
| Construction_Assembly_Kernel | Material properties, compatibility for assembly design | material_compatibility_contract |
| Construction_Chemistry_Kernel | Material class and compatibility data for chemistry analysis | material_class_contract |
| Construction_Scope_Kernel | Material references for scope boundaries | material_class_contract |
| Construction_Reference_Intelligence | All material truth for cross-kernel correlation | All contracts |

## Dependency Rules

1. This kernel never depends on sibling kernels (Specification, Assembly, Chemistry, Scope)
2. This kernel depends only on shared family artifacts from the intelligence layer
3. Sibling kernels read from this kernel via frozen seam contracts
4. The intelligence layer has read access to all material records
5. No circular dependencies are permitted

## Dependency Health Check

| Check | Expected State |
|---|---|
| Shared enum registry accessible | Required for schema validation |
| Shared taxonomy accessible | Required for material class enum |
| Standards registry accessible | Required for test method references |
| No sibling kernel imports | Verified — zero inbound from siblings |
| No circular references | Verified — unidirectional flow |
