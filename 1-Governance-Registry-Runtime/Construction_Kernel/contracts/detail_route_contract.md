# Detail Route Contract

**Authority:** Construction_Kernel
**Wave:** 13A
**Status:** Active

## Purpose

The Detail Route Contract governs the structure, validation, and consumption of the Detail Route Graph — the canonical graph of relationships between Detail DNA families.

## Governed Artifacts

| Artifact | Path | Authority |
|----------|------|-----------|
| Relationship Schema | `schemas/detail_relationship_schema.json` | Construction_Kernel |
| Route Index | `data/detail_route_index.json` | Construction_Kernel |

## Relationship Types

| Type | Directionality | Acyclic Required | Description |
|------|---------------|-----------------|-------------|
| `depends_on` | Directional | **Yes** | Source cannot be installed without target being complete. |
| `adjacent_to` | Bidirectional | No | Details share a physical boundary or are spatially proximate. |
| `blocks` | Directional | **Yes** | Source prevents target from proceeding. |
| `requires_continuity_with` | Bidirectional | No | Both details must maintain unbroken membrane/barrier continuity. |
| `substitutable_with` | Bidirectional | No | Details are alternative approaches to the same condition. |
| `terminates_into` | Directional | No | Source detail ends at or connects into target detail. |
| `overlaps_with` | Bidirectional | No | Details share physical overlap zones (e.g., reinforcement areas). |
| `precedes` | Directional | **Yes** | Source must be installed before target in construction sequence. |
| `follows` | Directional | **Yes** | Source is installed after target in construction sequence. |

## Graph Integrity Rules

### Cycle Protection

The following relationship types MUST form a Directed Acyclic Graph (DAG):
- `depends_on`
- `precedes`
- `blocks`
- `follows`

Cycles in these types are **validation errors** and must be rejected.

The following types MAY form cycles:
- `adjacent_to`
- `substitutable_with`
- `overlaps_with`
- `requires_continuity_with`
- `terminates_into`

### Validation Requirements

1. Every `source_detail_id` and `target_detail_id` MUST reference a valid detail family in `data/detail_dna/`.
2. Self-referencing edges (source == target) are NOT permitted.
3. Duplicate edges (same source, target, and type) are NOT permitted.
4. DAG validation MUST be performed on acyclic relationship types after any route modification.

## Consumption Rules

1. **Construction_Runtime** may read the route index to resolve detail sequencing and dependency chains.
2. **Construction_Runtime** may NOT modify the route index.
3. **Renderers** (CADless_drawings, holograph_details) may query adjacency relationships for layout hints but may NOT use the route graph for classification or resolution decisions.
4. **detail_training_corpus** may read the route index for training pair generation.

## Criticality Levels

| Level | Meaning |
|-------|---------|
| `required` | Relationship must be satisfied for system integrity. Violation is a validation error. |
| `recommended` | Relationship should be satisfied. Violation produces a warning. |
| `informational` | Relationship exists for documentation and training purposes. No enforcement. |

## Freeze Policy

The route contract structure (relationship types and integrity rules) is frozen after Wave 13A.
New routes between detail families may be added (additive changes only).
Existing relationship types may NOT be removed or renamed.
