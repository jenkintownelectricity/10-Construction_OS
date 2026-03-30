# Kernel Map — Construction Assembly Kernel

## Purpose

Top-level map of this kernel's structure, truth surfaces, and relationships.

## Kernel Identity

| Field | Value |
|---|---|
| Kernel ID | KERN-CONST-ASSY |
| Family | construction-kernel |
| Role | Assembly truth kernel |
| Domain | CSI Division 07 — Building Envelope Systems |

## Truth Surfaces

| Surface | Schema | Contract |
|---|---|---|
| Assembly Systems | assembly_system.schema.json | assembly_system_contract.md |
| Assembly Layers | assembly_layer.schema.json | (covered by assembly system) |
| Assembly Components | assembly_component.schema.json | (covered by assembly system) |
| Control Layer Assignments | control_layer_assignment.schema.json | (covered by continuity) |
| Transition Conditions | transition_condition.schema.json | transition_condition_contract.md |
| Penetration Conditions | penetration_condition.schema.json | penetration_condition_contract.md |
| Edge Conditions | edge_condition.schema.json | (covered by assembly system) |
| Tie-In Conditions | tie_in_condition.schema.json | (covered by assembly system) |
| Tested Assembly Records | tested_assembly_record.schema.json | tested_assembly_contract.md |
| Continuity Requirements | continuity_requirement.schema.json | continuity_requirement_contract.md |

## Kernel Models

| Model | Path | Purpose |
|---|---|---|
| Truth Model | kernel/truth_model.md | What constitutes assembly truth |
| Assembly Model | kernel/assembly_model.md | Layer stack structure |
| Control Layer Model | kernel/control_layer_model.md | 11 control layers and continuity |
| Transition Model | kernel/transition_model.md | Assembly-to-assembly connections |
| Penetration Model | kernel/penetration_model.md | Elements through assemblies |
| Tested Assembly Model | kernel/tested_assembly_model.md | Test-validated configurations |
| Continuity Model | kernel/continuity_model.md | Continuity rules |
| Taxonomy | kernel/taxonomy.md | Assembly and component types |
| Interface Model | kernel/interface_model.md | 10 interface zones |
| Standards Reference Model | kernel/standards_reference_model.md | Standards linkage |
| Evidence Linkage Model | kernel/evidence_linkage_model.md | Evidence tracing |
| Revision Lineage Model | kernel/revision_lineage_model.md | Version history |
| Lifecycle Context Model | kernel/lifecycle_context_model.md | Lifecycle metadata |
| Climate Context Model | kernel/climate_context_model.md | Climate metadata |
| Geometry Context Model | kernel/geometry_context_model.md | Geometry metadata |

## External Dependencies

| Source | Artifacts Consumed |
|---|---|
| Construction_Reference_Intelligence/shared/ | Control layers, interface zones, enums, standards, evidence, risk, taxonomy |
| Construction_Material_Kernel | Material entries (via material_ref) |
| Construction_Specification_Kernel | Specification entries (via spec_ref) |
