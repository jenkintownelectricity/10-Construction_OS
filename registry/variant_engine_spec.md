# Variant Generator Specification — Wave 14

## Registry Entry
- **Subsystem:** variant_generator
- **Owner:** Construction_Runtime
- **Path:** runtime/detail_variants/
- **Contract Version:** 14.3.0
- **Lifecycle:** active

## Purpose
Generates derived parameterized detail variants from canonical detail families.
Canonical IDs remain unchanged. Variant IDs are derived, not canonical truth.

## Output Artifacts
- `detail_variant_payload.json`
- `variant_manifest.json`

## Supported Parameters
parapet_height, membrane_thickness, pipe_diameter, curb_size,
drain_diameter, reglet_depth, joint_width, overflow_size

## Dependencies
- Construction_Kernel (canonical detail families — frozen, read-only)
- Detail Resolver Engine (resolved detail IDs)

## Governance
- Runtime-derived, recomputable
- May not alter canonical detail IDs
- May not write to Construction_Kernel
