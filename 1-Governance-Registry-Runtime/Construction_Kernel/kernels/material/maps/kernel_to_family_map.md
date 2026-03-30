# Kernel-to-Family Map — Construction Material Kernel

## Family Position

| Field | Value |
|---|---|
| Family | construction-kernel |
| Role | material-kernel |
| Kernel ID | KERN-CONST-MATL |
| Registry | ValidKernel_Registry |

## Sibling Relationships

| Sibling Kernel | Relationship | Data Flow |
|---|---|---|
| Construction_Specification_Kernel | Specification reads material properties | Outbound: property values |
| Construction_Assembly_Kernel | Assembly reads material data for layer design | Outbound: properties, compatibility |
| Construction_Chemistry_Kernel | Chemistry reads material class for analysis | Outbound: class, compatibility; Inbound: mechanism refs |
| Construction_Scope_Kernel | Scope reads material references | Outbound: class references |

## Shared Artifact Consumption

| Artifact | Source | Consumed By This Kernel |
|---|---|---|
| shared_enum_registry.json | Intelligence layer | Enum field validation |
| shared_taxonomy.json | Intelligence layer | Material class enum |
| shared_standards_registry.json | Intelligence layer | Standards citation format |
| control_layers.json | Intelligence layer | Control layer mappings |
| interface_zones.json | Intelligence layer | Interface zone context |
| division_07_posture.json | Intelligence layer | Division alignment |

## Family Coordination Rules

1. No sibling kernel duplicates material truth
2. Cross-kernel references use pointer IDs, not embedded data
3. Shared enum changes require family-wide validation
4. This kernel has no inbound dependencies from siblings
5. Intelligence layer orchestrates cross-kernel correlation

## Material Kernel Contributions to Family

- Provides the material property foundation for all sibling kernels
- Defines compatibility constraints that assemblies must respect
- Supplies weathering and hygrothermal data for durability analysis
- Maintains evidence traceability for all material facts
