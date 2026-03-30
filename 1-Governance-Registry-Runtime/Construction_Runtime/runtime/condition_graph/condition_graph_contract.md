# Condition Graph Contract — Wave 14

## Contract Version
14.1.0

## Purpose
Defines the contract for the Condition Graph Engine, which builds project-specific
condition graphs representing the spatial and functional relationships between
construction conditions on a project.

## Authority
- Construction_Runtime (derived, runtime-only)
- Construction_Kernel provides canonical condition types (read-only)

## Inputs
- Project condition specifications (user/system provided)
- Kernel-supported condition types (frozen, read-only)

## Outputs
- `project_condition_graph.json`

## Contract Object: ConditionGraph
```json
{
  "graph_id": "string",
  "source_refs": ["string"],
  "build_timestamp": "ISO-8601",
  "contract_version": "14.1.0",
  "nodes": [ConditionNode],
  "edges": [ConditionEdge],
  "checksum": "sha256 hex"
}
```

## Supported Node Types
- ROOF_FIELD
- PARAPET
- EDGE
- DRAIN
- SCUPPER
- CURB
- PIPE_PENETRATION
- EXPANSION_JOINT

## Supported Edge Types
- adjacent_to
- drains_to
- penetrates
- terminates_at
- intersects
- requires_continuity_with

## Rules
1. Graph must be acyclic for sequencing-critical edges (drains_to, terminates_at).
2. Non-sequencing adjacency edges may be cyclic only if explicitly allowed by schema.
3. Every node must map to a supported kernel condition type.
4. Every edge must validate against supported node pair rules.
5. Unsupported node/edge types must fail validation.
6. Deterministic ordering required in serialized output.
7. Fail closed on any invalid input.

## Governance
- This subsystem may NOT create new canonical condition types.
- This subsystem may NOT write to Construction_Kernel.
- All outputs are runtime-derived and recomputable.
