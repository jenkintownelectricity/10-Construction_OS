# Construction Reference Graph Contract — Wave 17A

## Purpose

The Construction Reference Graph provides canonical identity, lineage, typed linkage,
and reference resolution for all governed Construction OS objects.

## Authority

- **Truth source**: Construction_Kernel (frozen, read-only)
- **Execution layer**: Construction_Runtime
- **Catalog layer**: Construction_OS_Registry
- **Verification layer**: ValidKernelOS_VKBUS

## Contract Surface

### Identity Allocation
- `IdentityAllocator.allocate(source_system, source_reference, object_type, scope)` → `CRG-{TYPE}-{NUMBER}`
- IDs are stable, deterministic, and do not depend on UI state
- Collisions fail closed
- Idempotent replay returns existing node for identical payloads

### Node Registration
- `NodeRegistry.register(object_type, scope, partition, source_system, source_reference, authority_type)`
- Validates partition compliance, authority type, and uniqueness
- Duplicate registration fails closed unless exact replay

### Edge Registration
- `EdgeRegistry.register(relation_type, from_id, to_id)`
- Validates relation type against from/to type rules
- Advisory edges cannot overwrite deterministic edges
- Duplicate insertion fails closed unless exact replay

### Graph Building
- `ReferenceGraphBuilder.register_bundle(nodes, edges, mode)` — atomic bundle registration
- Modes: `full_rebuild`, `incremental_append`, `idempotent_replay`
- If any node or edge fails, the whole bundle fails closed

### Resolution
- `ResolutionEngine.resolve_object(graph_id)` — single object resolution
- `ResolutionEngine.resolve_upstream(graph_id)` — upstream ancestors
- `ResolutionEngine.resolve_downstream(graph_id)` — downstream descendants
- `ResolutionEngine.trace_lineage(graph_id)` — full lineage with validation
- `ResolutionEngine.find_related(graph_id)` — all related nodes
- Resolution prefers exact scoped authoritative matches over global advisory matches
- Ambiguity fails closed or returns unresolved

### Query
- `QueryEngine.bfs(start_id)` — breadth-first traversal
- `QueryEngine.dfs(start_id)` — depth-first traversal
- `QueryEngine.shortest_path(source_id, target_id)` — shortest path
- `QueryEngine.find_nodes_by_type(object_type)` — type-filtered search
- `QueryEngine.get_connected_components()` — component analysis

### Validation
- `GraphValidator.validate_reference_graph()` — comprehensive validation
- Checks: node integrity, edge integrity, partition compliance, relationship rules, orphans, kernel immutability

### Orphan Detection
- `OrphanDetector.detect_orphans()` — nodes with no edges
- `OrphanDetector.detect_disconnected_components()` — disconnected subgraphs

## Failure Cases

- Invalid object type → fail closed
- Identity collision with different payload → fail closed
- Duplicate node/edge → fail closed (unless idempotent replay)
- Invalid relation type → fail closed
- Invalid from/to type pair for relation → fail closed
- Broken lineage (where required) → fail validation
- Advisory overwriting deterministic → fail closed
- Partition violation → fail closed
- Bundle with any invalid item → whole bundle fails closed

## Lifecycle States

- `active` — normal state, included in resolution
- `superseded` — replaced by newer version, queryable for lineage
- `archived` — immutable, no status changes allowed
- `invalid` — excluded from deterministic resolution

## Governance Rules

- Kernel is read-only — runtime consumes but never modifies kernel truth
- Runtime does not redefine kernel semantics
- Advisory results never override deterministic truth
- Hard deletion of authoritative lineage nodes is prohibited
- Graph pruning must never break lineage chains

## Contract Version

`17A.1.0`
