# Dependency Map

## Purpose

Documents all dependencies between the Chemistry Kernel and external systems, kernels, and data sources.

## Upstream Dependencies (This Kernel Consumes)

| Source | What | How |
|---|---|---|
| Manufacturer SDS | Chemical composition, hazard data, VOC content | Manual entry into chemistry records with SDS reference |
| ASTM Standards | Test method identifiers | Referenced by ID in evidence_refs and test_method_ref fields |
| ISO Standards | International test method identifiers | Referenced by ID in evidence_refs fields |
| Shared Family Artifacts | Control layers, interface zones, division posture | Referenced from Construction_Reference_Intelligence shared/ |

## Downstream Dependencies (Other Systems Consume This Kernel)

| Consumer | What They Consume | Reference Mechanism |
|---|---|---|
| Construction_Material_Kernel | Chemical system IDs for material-chemistry linkage | `chemistry_ref` field (CSYS-xxx) |
| Construction_Assembly_Kernel | Adhesion rules, incompatibility rules, cure mechanisms | Typed ID references |
| Construction_Specification_Kernel | Chemistry family classifications, compatibility data | Chemistry family enum values |
| Construction_Reference_Intelligence | All chemistry truth records | Full record query by typed ID |

## Internal Dependencies

| From | To | Relationship |
|---|---|---|
| Chemical System | Polymer Family | `polymer_base` reference |
| Chemical System | Additive | `additives[]` references |
| Chemical System | Cure Mechanism | `cure_mechanism_ref` |
| Chemical System | Solvent System | `solvent_system_ref` |
| Adhesion Rule | Chemical System | `chemistry_ref` |
| Adhesion Rule | Chemical System | `primer_ref` (optional) |
| Incompatibility Rule | Chemical System | `chemistry_a_ref`, `chemistry_b_ref` |
| Degradation Mechanism | Chemical System | `chemistry_ref` |
| Chemical Hazard Record | Chemical System | `chemistry_ref` |

## No Circular Dependencies

This kernel has no circular dependencies. All reference directions are acyclic. Chemical System is the hub object; all other objects reference it.
