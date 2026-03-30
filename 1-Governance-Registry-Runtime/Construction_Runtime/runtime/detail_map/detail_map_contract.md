# Detail Map Contract — Wave 14

## Contract Version
14.4.0

## Purpose
Navigates the frozen detail relationship graph to compute paths,
expose adjacency/continuity/dependency context, and provide route
summaries for UI and resolver support.

## Authority
- Construction_Runtime (derived, runtime-only)
- Construction_Kernel provides the frozen route graph (read-only)

## Inputs
- Frozen detail_route_index.json from Construction_Kernel
- Detail IDs for path queries

## Outputs
- detail_paths.json
- detail_navigation_summary.json

## Contract Object: DetailPath
```json
{
  "source_detail_id": "string",
  "target_detail_id": "string",
  "path": [
    {"detail_id": "string", "relationship": "string", "criticality": "string"}
  ],
  "path_length": "number"
}
```

## Rules
1. May read frozen route graph only.
2. May not alter canonical detail route graph.
3. Cache must be derivable and safe to delete.
4. Route answers must preserve relationship type semantics.

## Governance
- This subsystem may NOT modify the route graph.
- This subsystem may NOT write to Construction_Kernel.
- All outputs are runtime-derived and recomputable.
