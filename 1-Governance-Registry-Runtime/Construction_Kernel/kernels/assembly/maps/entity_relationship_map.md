# Entity Relationship Map — Construction Assembly Kernel

## Purpose

Documents the relationships between the 10 core kernel objects.

## Relationship Diagram

```
assembly_system (1)
    |
    |-- contains --> assembly_layer (N)
    |                    |
    |                    |-- references --> material_ref (Material Kernel)
    |                    |-- classified by --> control_layer_id
    |
    |-- has --> control_layer_assignment (N)
    |               |-- references --> control_layer_id
    |
    |-- encounters --> transition_condition (N)
    |                      |-- from_assembly_ref --> assembly_system
    |                      |-- to_assembly_ref --> assembly_system
    |                      |-- at --> interface_zone
    |
    |-- has --> penetration_condition (N)
    |               |-- assembly_ref --> assembly_system
    |               |-- affects --> control_layer_id[]
    |
    |-- has --> edge_condition (N)
    |               |-- assembly_ref --> assembly_system
    |               |-- terminates --> control_layer_id[]
    |
    |-- validated by --> tested_assembly_record (N)
    |                        |-- assembly_ref --> assembly_system
    |                        |-- tested per --> test_standard_ref
    |
    |-- subject to --> continuity_requirement (N)
                           |-- governs --> control_layer_id
                           |-- scope defines applicability

tie_in_condition
    |-- connects --> assembly_system[] (2+)
    |-- maintains --> control_layer_id[]

assembly_component
    |-- participates in --> assembly_layer (via material_ref)
    |-- references --> material_ref (Material Kernel)
    |-- references --> spec_ref (Specification Kernel)
```

## Cardinality Summary

| Relationship | Cardinality |
|---|---|
| assembly_system : assembly_layer | 1 : N |
| assembly_system : control_layer_assignment | 1 : N |
| assembly_system : transition_condition | N : N (assembly appears as from or to) |
| assembly_system : penetration_condition | 1 : N |
| assembly_system : edge_condition | 1 : N |
| assembly_system : tested_assembly_record | 1 : N |
| control_layer_id : continuity_requirement | 1 : N |
| tie_in_condition : assembly_system | N : N |

## Cross-Kernel References

| Reference Field | Source Object | Target Kernel |
|---|---|---|
| material_ref | assembly_layer, assembly_component | Construction_Material_Kernel |
| spec_ref | assembly_component | Construction_Specification_Kernel |
| test_standard_ref | tested_assembly_record | Shared Standards Registry |
| control_layer_id | multiple objects | Shared Control Layer Registry |
| interface_zone | transition_condition | Shared Interface Zone Registry |

## Key Constraints

1. An assembly_layer exists only within an assembly_system
2. A transition_condition connects exactly two assembly_systems
3. A penetration_condition references exactly one assembly_system
4. A tested_assembly_record validates exactly one assembly_system configuration
5. A continuity_requirement governs exactly one control_layer_id
