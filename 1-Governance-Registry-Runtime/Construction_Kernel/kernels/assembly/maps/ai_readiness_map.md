# AI Readiness Map — Construction Assembly Kernel

## Purpose

Maps the kernel's structural features to AI consumption capabilities.

## Readiness Assessment by Object Type

| Object Type | Schema Defined | Enums Constrained | Refs Typed | AI Query Ready |
|---|---|---|---|---|
| assembly_system | Yes | assembly_type, status | material_ref, spec_ref | Yes |
| assembly_layer | Yes | control_layer_id, attachment_method, status | material_ref | Yes |
| assembly_component | Yes | component_type, status | material_ref, spec_ref | Yes |
| control_layer_assignment | Yes | control_layer_id, continuity_status | assembly_ref | Yes |
| transition_condition | Yes | interface_zone, status, risk_level | from/to assembly_ref | Yes |
| penetration_condition | Yes | penetration_type, status, risk_level | assembly_ref | Yes |
| edge_condition | Yes | edge_type, status | assembly_ref | Yes |
| tie_in_condition | Yes | tie_in_type, status | assemblies[] | Yes |
| tested_assembly_record | Yes | test_type, status | assembly_ref, test_standard_ref | Yes |
| continuity_requirement | Yes | control_layer_id, continuity_type | (scope is free text) | Partial |

## AI-Friendly Features

### Enumerated Vocabularies

- 6 assembly types
- 11 control layer IDs
- 10 interface zone IDs
- 14 component types
- 6 penetration types
- 6 edge types
- 3 tie-in types
- 6 test types
- 4 continuity types
- 4 risk levels
- 3 status values
- 12 attachment methods

Total: ~80 enumerated values providing a finite, well-defined vocabulary.

### Graph Traversal Paths

AI systems can traverse from any object to related objects:
- assembly_system -> layers -> material_ref -> Material Kernel
- assembly_system -> transition_conditions -> connected assemblies
- assembly_system -> penetration_conditions -> control layers affected
- assembly_system -> tested_assembly_records -> test results
- control_layer_id -> continuity_requirements -> scope

### Structured Queries Supported

1. "Find all roof assemblies with continuous air control" — filter by assembly_type + control_layer_continuity
2. "List critical-risk transitions" — filter transition_condition by risk_level
3. "Which assemblies lack NFPA 285 test records?" — join assembly_system with tested_assembly_record
4. "Show penetrations affecting bulk_water_control" — filter penetration_condition by control_layers_affected

## Gaps for AI Readiness

| Gap | Impact | Mitigation Path |
|---|---|---|
| scope field on continuity_requirement is free text | Cannot be programmatically evaluated | Future: structured scope object |
| seal_method on penetration_condition is free text | Cannot be enumerated | Future: seal method enum |
| notes fields are free text | Unstructured information | AI can extract from notes using NLP |
| Cross-kernel reference resolution | material_ref, spec_ref require sibling kernel | Future: resolution service |
