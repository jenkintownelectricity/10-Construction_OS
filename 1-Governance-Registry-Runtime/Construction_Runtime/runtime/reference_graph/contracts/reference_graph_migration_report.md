# Reference Graph Migration Report — Wave 15 to Wave 17A

## Migration Summary

| Metric | Value |
|--------|-------|
| Wave | 15 → 17A |
| Source subsystem | `runtime/detail_graph/` |
| Target subsystem | `runtime/reference_graph/` |
| Migration type | Schema expansion + relationship mapping |
| Status | Complete |

## Node Migration

### Wave 15 Detail Nodes → CRG DETAIL Nodes

All Wave 15 detail graph nodes are mapped to CRG nodes with:

| Wave 15 Field | CRG Field |
|--------------|-----------|
| `detail_id` | `source_reference` |
| (implicit) | `source_system` = `Construction_Kernel` |
| (implicit) | `object_type` = `DETAIL` |
| (implicit) | `scope` = `global` |
| (implicit) | `partition` = `global_kernel_partition` |
| (implicit) | `authority_type` = `kernel_canonical` |
| `system` | `metadata.system` |
| `class` | `metadata.class` |
| `condition` | `metadata.condition` |
| `variant` | `metadata.variant` |
| `assembly_family` | `metadata.assembly_family` |
| `display_name` | `metadata.display_name` |

**Identity traceability**: Every CRG node's `source_reference` contains the original
Wave 15 `detail_id`, enabling lookup via `resolve_by_reference("Construction_Kernel", detail_id, "DETAIL", "global")`.

## Edge Migration

### Wave 15 Relationship Types → CRG Relation Types

| Wave 15 Type | CRG Relation Type | CRG Category |
|-------------|-------------------|--------------|
| `depends_on` | `prerequisite_for` | navigation |
| `adjacent_to` | `related_to` | navigation |
| `blocks` | `prerequisite_for` | navigation |
| `requires_continuity_with` | `related_to` | navigation |
| `substitutable_with` | `alternative_to` | navigation |
| `terminates_into` | `related_to` | navigation |
| `overlaps_with` | `related_to` | navigation |
| `precedes` | `installed_before` | navigation |
| `follows` | `installed_after` | navigation |

All Wave 15 relationship types are mapped. No unmapped relationships exist.

Each migrated edge carries `source_basis: "wave15_migration:{original_type}"` for traceability.

All migrated edges from Wave 15 are marked `is_advisory: true` since they are
navigation-category relationships in the CRG schema.

## New Capabilities in Wave 17A

The Construction Reference Graph extends beyond Wave 15 detail-to-detail relationships:

### New Object Types (not in Wave 15)
- VARIANT, INSTRUCTION_SET, MANIFEST
- RENDER_JOB, DRAWING, PDF, DXF, SVG
- MARKUP, ANNOTATION, OBSERVATION
- CONDITION, PROJECT, ARTIFACT
- ARTIFACT_REGION, PAGE_REFERENCE

### New Relationship Categories (not in Wave 15)
- **Identity**: instance_of, belongs_to_project, references_canonical, scoped_under
- **Lineage**: derived_from, produced_by, rendered_from, supersedes, revision_of, generated_from
- **Artifact**: appears_in, annotates, region_of, page_of, attached_to
- **Observation**: observed_in, documents, verifies, flags, supports, invalidates

### New Features (not in Wave 15)
- Graph partitioning (kernel, runtime, project, artifact, observation)
- Deterministic identity allocation (CRG-{TYPE}-{NUMBER})
- Idempotent replay support
- Atomic bundle writes
- Lifecycle state management (active, superseded, archived, invalid)
- Resolution engine with deterministic/advisory/unresolved modes
- Orphan detection
- Cross-partition edge validation

## Verification

VKBUS observers verify:
- All Wave 15 nodes exist in CRG
- All Wave 15 edges are mapped to CRG edges
- No Wave 15 data is lost
- Source references are traceable
- Kernel partition integrity is maintained

## Unmapped Items

None. All Wave 15 content is accounted for in the CRG.

## Conclusion

The Wave 15 detail graph has been fully migrated into the Construction Reference Graph.
All nodes are preserved with identity traceability. All edges are mapped with type
correspondence. The CRG extends the detail graph into a platform-wide object graph
while maintaining backward compatibility with all Wave 15 constructs.
