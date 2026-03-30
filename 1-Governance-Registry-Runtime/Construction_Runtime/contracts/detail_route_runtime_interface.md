# Detail Route Runtime Interface Contract

**Authority:** Construction_Runtime (interface contract only)
**Source of Truth:** Construction_Kernel (Detail Route Graph)
**Wave:** 13A
**Status:** Active

## Purpose

This contract defines how Construction_Runtime consumes the Detail Route Graph from Construction_Kernel for dependency resolution, sequencing, and related detail discovery at execution time.

## Authority Boundary

| Responsibility | Owner |
|---------------|-------|
| Route graph structure and data | Construction_Kernel |
| Relationship type definitions | Construction_Kernel |
| Cycle protection rules | Construction_Kernel |
| Route traversal at runtime | Construction_Runtime |
| Dependency chain resolution | Construction_Runtime |
| Sequencing logic | Construction_Runtime |
| Related detail discovery | Construction_Runtime |

## Input Contract

The runtime reads the route graph from:

```
Construction_Kernel/data/detail_route_index.json
```

Each route entry conforms to `Construction_Kernel/schemas/detail_relationship_schema.json`.

## Runtime Operations

### 1. Dependency Resolution

Given a detail family ID, the runtime resolves all `depends_on` relationships transitively to determine prerequisite details.

```
Input:  detail_id
Output: ordered list of prerequisite detail_ids (topological sort)
Error:  ROUTE_CYCLE_DETECTED if cycle found in depends_on edges
```

### 2. Construction Sequencing

Given a set of detail family IDs, the runtime resolves `precedes` and `follows` relationships to determine installation order.

```
Input:  set of detail_ids
Output: ordered sequence of detail_ids
Error:  ROUTE_CYCLE_DETECTED if cycle found in precedes/follows edges
```

### 3. Related Detail Discovery

Given a detail family ID, the runtime discovers related details via all relationship types.

```
Input:  detail_id, optional filter by relationship_type
Output: list of { detail_id, relationship_type, criticality }
```

### 4. Continuity Validation

Given a set of detail family IDs for a project scope, the runtime validates that all `requires_continuity_with` relationships are satisfied.

```
Input:  set of detail_ids in project scope
Output: { valid: boolean, missing_continuity: [{ source, target }] }
```

### 5. Substitution Discovery

Given a detail family ID, the runtime discovers alternative details via `substitutable_with` relationships.

```
Input:  detail_id
Output: list of substitutable detail_ids
```

## Fail-Closed Rules

1. If the route graph contains a cycle in `depends_on`, `precedes`, or `blocks` edges, the runtime MUST reject the graph and surface `ROUTE_CYCLE_DETECTED`.
2. If a referenced detail_id does not exist in `data/detail_dna/`, the runtime MUST surface `ROUTE_INVALID_REFERENCE`.
3. The runtime MUST NOT create, modify, or delete route entries. All modifications go through Construction_Kernel.
4. If continuity validation fails, the runtime MUST surface warnings — it MUST NOT auto-resolve by inserting detail families.

## Error Codes

| Code | Description |
|------|-------------|
| `ROUTE_CYCLE_DETECTED` | Circular dependency found in acyclic relationship type |
| `ROUTE_INVALID_REFERENCE` | Detail ID in route does not exist in kernel |
| `ROUTE_MISSING_CONTINUITY` | Required continuity relationship not satisfied in project scope |
| `ROUTE_AMBIGUOUS_SEQUENCE` | Multiple valid orderings exist; disambiguation required |

## Graph Traversal Constraints

1. Maximum traversal depth: 12 (consistent with existing graph_reference_contract)
2. Traversal MUST be deterministic — same input produces same output
3. All traversal decisions MUST be logged in the audit trail

## Data Source Paths

| Data | Path | Format |
|------|------|--------|
| Route index | `Construction_Kernel/data/detail_route_index.json` | JSON |
| Relationship schema | `Construction_Kernel/schemas/detail_relationship_schema.json` | JSON Schema |
| Route contract | `Construction_Kernel/contracts/detail_route_contract.md` | Markdown |

## Versioning

- This interface contract version: `13A`
- Route graph schema version: `13A`
- Maximum traversal depth aligned with graph_reference_contract: 12
