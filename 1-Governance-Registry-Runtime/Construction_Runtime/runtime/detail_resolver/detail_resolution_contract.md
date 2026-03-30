# Detail Resolution Contract — Wave 14

## Contract Version
14.2.0

## Purpose
Resolves canonical detail families from a project condition graph and material context.
Returns only canonical detail IDs from Construction_Kernel. Never fabricates IDs.

## Authority
- Construction_Runtime (derived, runtime-only)
- Construction_Kernel provides canonical detail families and route graph (frozen, read-only)

## Inputs
- project_condition_graph.json (from Subsystem 1)
- material_context (assembly family / material class)
- Frozen kernel detail families
- Frozen route graph (detail_route_index.json)

## Outputs
- resolved_detail_manifest.json

## Contract Object: ResolvedDetail
```json
{
  "condition_ref": "string — node_id from condition graph",
  "canonical_detail_id": "string — detail_id from kernel or null",
  "resolution_status": "RESOLVED | UNRESOLVED | UNKNOWN | UNSUPPORTED",
  "resolution_reason": "string — human-readable resolution path",
  "material_context_ref": "string — assembly family used for resolution",
  "route_context_ref": "string — route relationship context if applicable",
  "ambiguity_flags": ["string — list of ambiguity indicators"]
}
```

## Rules
1. Resolver must return canonical detail IDs only.
2. Resolver must validate that selected family exists in kernel.
3. Resolver must emit resolution reason path.
4. Resolver must emit UNKNOWN/UNRESOLVED where confidence or support is insufficient.
5. Resolver must fail closed if no valid match exists.
6. Resolver must not fabricate family IDs.
7. Resolver decisions must be deterministic for identical inputs.

## Governance
- This subsystem may NOT create new detail families.
- This subsystem may NOT write to Construction_Kernel.
- All outputs are runtime-derived and recomputable.
