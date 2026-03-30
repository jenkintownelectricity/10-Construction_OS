# Kernel-to-Reference-Intelligence Map — Construction Material Kernel

## Purpose
Maps data exchange between this kernel and the Construction_Reference_Intelligence layer.

## Outbound: Material Kernel to Intelligence

| Data Provided | Intelligence Use | Contract |
|---|---|---|
| Material class records | Cross-kernel taxonomy alignment | material_class_contract |
| Material property values | Specification compliance analysis | material_property_contract |
| Compatibility matrices | Assembly risk identification | material_compatibility_contract |
| Weathering behavior data | Climate-correlated risk patterns | weathering_behavior_contract |
| Hygrothermal properties | Moisture management analysis | hygrothermal_property_contract |
| Evidence linkages | Data quality assessment | All contracts |
| Ambiguity flags | Unresolved question surfacing | All contracts |

## Inbound: Intelligence to Material Kernel

| Artifact Received | Kernel Use |
|---|---|
| shared_enum_registry.json | Enum validation for all schema fields |
| shared_taxonomy.json | Material class enum source |
| shared_standards_registry.json | Standards citation identifiers |
| control_layers.json | Control layer ID registry |
| interface_zones.json | Interface zone context |
| division_07_posture.json | Division 07 alignment validation |

## Intelligence Operations Using Material Data

| Operation | Material Data Consumed | Output (Not Stored Here) |
|---|---|---|
| Compatibility gap analysis | Full compatibility matrix | Untested pair priority list |
| Weathering risk correlation | Weathering + climate context | Climate-zone risk scores |
| Property trend analysis | Property values across classes | Outlier detection reports |
| Evidence currency check | Evidence dates | Stale data alerts |
| Cross-kernel validation | Material refs in other kernels | Reference integrity reports |

## Coordination Protocol

1. Intelligence layer reads material data via frozen seam contracts
2. Material kernel consumes shared artifacts by reference, not copy
3. Intelligence-generated insights are not material truth
4. Material data changes are visible to intelligence through version tracking
