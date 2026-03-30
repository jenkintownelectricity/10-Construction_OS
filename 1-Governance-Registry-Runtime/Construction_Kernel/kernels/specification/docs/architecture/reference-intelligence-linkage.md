# Reference Intelligence Linkage — Construction Specification Kernel

## Relationship Model

Construction_Reference_Intelligence reads specification truth from this kernel. The relationship is one-directional: the intelligence layer consumes kernel data; the kernel does not consume intelligence output. This prevents circular dependencies and preserves truth boundary integrity.

## Linkage Mechanism

The intelligence layer accesses specification kernel data through `kernel_refs` — structured pointers that identify:

1. The kernel repository (`Construction_Specification_Kernel`)
2. The schema type being referenced (e.g., `requirement`, `specification_section`)
3. The specific record ID (e.g., `REQ-07-5200-001`)
4. The schema version (`v1`)

These pointers are maintained by the intelligence layer, not by this kernel. This kernel publishes structured truth; it does not track who reads it.

## What the Intelligence Layer Reads

The intelligence layer consumes the following from this kernel:

- **Specification requirements** — to identify patterns, gaps, and cross-project trends
- **Ambiguity flags** — to surface specification gaps for human review
- **Interface zone coverage** — to assess whether specs adequately address transitions
- **Standards references** — to correlate spec requirements with governing standards
- **Testing and submittal requirements** — to evaluate specification completeness
- **Warranty requirements** — to assess risk posture and warranty coordination
- **Revision lineage** — to track how specifications evolve across addenda

## What the Intelligence Layer Does NOT Modify

The intelligence layer never writes back to this kernel. It does not:

- Create, modify, or delete specification records
- Resolve ambiguity flags
- Add interpretive notes to kernel records
- Insert computed values into specification data

Intelligence output (risk scores, pattern analyses, recommendations) lives in the intelligence layer's own data structures, linked back to kernel records via `kernel_refs`.

## Shared Artifact Coordination

Both this kernel and the intelligence layer reference the same shared artifacts in `Construction_Reference_Intelligence/shared/`:

- `control_layers.json` — canonical control layer definitions
- `interface_zones.json` — canonical interface zone definitions
- `shared_enum_registry.json` — shared enumeration values
- `shared_standards_registry.json` — standards citation registry
- `shared_taxonomy.json` — shared taxonomy fields

This shared foundation ensures that specification records and intelligence analyses use the same vocabulary and classification system.

## Registration

This kernel is registered in `ValidKernel_Registry` with role `specification-kernel`. The intelligence layer discovers available kernels through this registry.
