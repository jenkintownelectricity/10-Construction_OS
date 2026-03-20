# Condition Graph Engine Specification — Wave 14

## Registry Entry
- **Subsystem:** condition_graph_engine
- **Owner:** Construction_Runtime
- **Path:** runtime/condition_graph/
- **Contract Version:** 14.1.0
- **Lifecycle:** active

## Purpose
Builds project-specific condition graphs representing the spatial and functional
relationships between construction conditions on a project.

## Output Artifacts
- `project_condition_graph.json`

## Supported Node Types
ROOF_FIELD, PARAPET, EDGE, DRAIN, SCUPPER, CURB, PIPE_PENETRATION, EXPANSION_JOINT

## Supported Edge Types
adjacent_to, drains_to, penetrates, terminates_at, intersects, requires_continuity_with

## Dependencies
- Construction_Kernel (condition types — frozen, read-only)

## Governance
- Runtime-derived, recomputable
- May not write to Construction_Kernel
- Deterministic output required
