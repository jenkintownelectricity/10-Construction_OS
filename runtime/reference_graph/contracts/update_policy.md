# Update Policy — Construction Reference Graph — Wave 17A

## Write Modes

### full_rebuild
- Rebuilds graph state from authoritative source set
- Clears all existing nodes and edges
- Re-registers everything from the provided bundle
- Used for complete graph reconstruction from upstream truth

### incremental_append
- Adds new valid nodes and edges without mutating existing authoritative history
- Existing nodes and edges remain unchanged
- New registrations must pass all validation checks
- Default mode for normal operations

### idempotent_replay
- Repeated identical write requests must not duplicate nodes or edges
- If the same source_system + source_reference + object_type + scope is submitted
  with identical authoritative payload, returns the existing node
- If submitted with different payload, fails closed

## Atomic Bundle Writes

- All write operations are bundled at the operation level
- If any required node or edge in a bundle fails validation, the whole bundle fails closed
- No partial commits are allowed for multi-object registration bundles

## Validation Checks on Update

The update_engine enforces:
1. Transaction bundle validation (all specs structurally valid)
2. Node uniqueness checks (source fingerprint collision detection)
3. Edge uniqueness checks (relation + from + to fingerprint)
4. Lineage completeness checks (where lineage is required)
5. Partition compliance checks (object types in correct partitions)

## Status Transitions

Allowed transitions:
- `active` → `superseded` (replaced by newer version)
- `active` → `archived` (permanently frozen)
- `active` → `invalid` (isolated from resolution)
- `superseded` → `archived`
- `invalid` → `archived`
- `archived` → (no transitions allowed — immutable)

## Prohibited Operations

- Hard deletion of authoritative lineage nodes
- Modification of archived nodes
- Advisory edges overwriting deterministic edges
- Partial commits within a bundle
- Kernel mutation from runtime

## Post-Update Validation

After every update, the system runs:
- Node integrity validation
- Edge integrity validation
- Partition compliance validation
- Relationship rule validation
- Orphan edge detection
- Kernel immutability check
