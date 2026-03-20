# Migration Policy — Construction Reference Graph — Wave 17A

## Wave 15 Detail Graph Migration

The Wave 15 detail graph must migrate into or map into the Construction Reference Graph.

### Migration Requirements

1. **All Wave 15 detail nodes preserved or mapped**
   - Every detail node from the Wave 15 detail graph must have a corresponding
     CRG node with `object_type: DETAIL` in the `global_kernel_partition`
   - Detail identity fields (system, class, condition, variant, assembly_family)
     must be preserved in the node metadata

2. **All valid Wave 15 detail relationships preserved as typed graph edges**
   - Wave 15 relationship types map to CRG relation types:
     - `depends_on` → `prerequisite_for` (navigation)
     - `adjacent_to` → `related_to` (navigation)
     - `blocks` → `prerequisite_for` (navigation)
     - `requires_continuity_with` → `related_to` (navigation)
     - `substitutable_with` → `alternative_to` (navigation)
     - `terminates_into` → `related_to` (navigation)
     - `overlaps_with` → `related_to` (navigation)
     - `precedes` → `installed_before` (navigation)
     - `follows` → `installed_after` (navigation)

3. **Legacy detail graph IDs traceable to new graph IDs**
   - The `source_reference` field in each CRG node must contain the original
     Wave 15 `detail_id`
   - The `source_system` field must be set to `Construction_Kernel`

4. **Migration report required**
   - `reference_graph_migration_report.md` must be produced
   - Must list all migrated nodes, mapped edges, and any unmapped items

### Migration Process

1. Load Wave 15 detail graph (from `runtime/detail_graph/`)
2. For each detail node, create a CRG node:
   - `object_type`: `DETAIL`
   - `scope`: `global`
   - `partition`: `global_kernel_partition`
   - `source_system`: `Construction_Kernel`
   - `source_reference`: original `detail_id`
   - `authority_type`: `kernel_canonical`
3. For each detail edge, create a CRG edge with mapped relation type
4. Validate the migrated graph
5. Produce migration report

### Unmappable Items

- Items that cannot be mapped must be documented in the migration report
- External references must be marked `external_unverified`
- No data loss is acceptable — all Wave 15 content must be accounted for

### Verification

VKBUS must verify:
- All Wave 15 nodes exist in CRG
- All Wave 15 edges are mapped to CRG edges
- No Wave 15 data is lost
- Lineage from Wave 15 is traceable in CRG
