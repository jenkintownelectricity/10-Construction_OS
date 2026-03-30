# Object Model Overview — Construction Assembly Kernel

## Core Objects

The kernel defines 10 core object types. Each has a dedicated JSON Schema and represents a distinct truth surface within the assembly domain.

### 1. assembly_system

The primary object. Represents a complete assembly as an ordered layer stack with control-layer continuity tracking. Typed by function: roof, wall, below-grade, plaza, vegetated, or hybrid.

- Schema: `schemas/assembly_system.schema.json`
- Key fields: `system_id`, `assembly_type`, `layers[]`, `control_layer_continuity`, `interface_zones`

### 2. assembly_layer

A single layer within an assembly system. Defined by position (exterior to interior), control-layer assignment, material reference, and attachment method.

- Schema: `schemas/assembly_layer.schema.json`
- Key fields: `layer_id`, `position`, `control_layer_id`, `material_ref`, `attachment_method`

### 3. assembly_component

A discrete component that participates in one or more assemblies. Typed by function: membrane, insulation, substrate, fastener, sealant, flashing, edge metal, drain, curb, etc.

- Schema: `schemas/assembly_component.schema.json`
- Key fields: `component_id`, `component_type`, `material_ref`, `spec_ref`

### 4. control_layer_assignment

Maps an assembly's layer to a control-layer function. Tracks continuity status: continuous, interrupted, terminated, or transitioned.

- Schema: `schemas/control_layer_assignment.schema.json`
- Key fields: `assignment_id`, `assembly_ref`, `control_layer_id`, `continuity_status`

### 5. transition_condition

Records how two assemblies connect at an interface zone. Tracks which control layers are maintained across the transition and the associated risk level.

- Schema: `schemas/transition_condition.schema.json`
- Key fields: `transition_id`, `interface_zone`, `from_assembly_ref`, `to_assembly_ref`, `risk_level`

### 6. penetration_condition

Records how a penetrating element passes through an assembly. Tracks affected control layers and seal method.

- Schema: `schemas/penetration_condition.schema.json`
- Key fields: `penetration_id`, `penetration_type`, `assembly_ref`, `control_layers_affected`

### 7. edge_condition

Records how an assembly terminates at its perimeter. Typed by edge treatment: fascia, drip edge, gravel stop, coping, parapet cap, termination bar.

- Schema: `schemas/edge_condition.schema.json`
- Key fields: `edge_id`, `edge_type`, `assembly_ref`, `control_layers_terminated`

### 8. tie_in_condition

Records how assemblies connect at construction boundaries: new-to-existing, phased construction, or repair.

- Schema: `schemas/tie_in_condition.schema.json`
- Key fields: `tie_in_id`, `tie_in_type`, `assemblies`, `control_layers_maintained`

### 9. tested_assembly_record

Records a test-validated assembly configuration with test type, standard, result, and evidence reference.

- Schema: `schemas/tested_assembly_record.schema.json`
- Key fields: `record_id`, `test_type`, `test_standard_ref`, `result`, `assembly_ref`

### 10. continuity_requirement

Defines a rule for control-layer continuity: must be continuous, may be interrupted, must terminate, or must transition.

- Schema: `schemas/continuity_requirement.schema.json`
- Key fields: `requirement_id`, `control_layer_id`, `continuity_type`, `scope`

## Relationships

- `assembly_system` contains `assembly_layer[]`
- `assembly_layer` references `assembly_component` via material/component refs
- `control_layer_assignment` links `assembly_system` to control-layer IDs
- `transition_condition` references two `assembly_system` objects and an interface zone
- `penetration_condition` references one `assembly_system`
- `edge_condition` references one `assembly_system`
- `tested_assembly_record` references one `assembly_system`
- `continuity_requirement` references a control-layer ID and defines scope
