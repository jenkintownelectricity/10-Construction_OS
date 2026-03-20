# Shop Drawing Preparation Specification — Wave 14

## Registry Entry
- **Subsystem:** shop_drawing_prep
- **Owner:** Construction_Runtime
- **Path:** runtime/shop_drawing_prep/
- **Contract Version:** 14.7.0
- **Lifecycle:** active

## Purpose
Prepares manifests and package structure for downstream rendering.
No direct rendering occurs. Renderers (CADless_drawings, holograph_details)
remain external consumers.

## Output Artifacts
- `project_shop_drawing_manifest.json`
- `sheet_index.json`
- `drawing_package_manifest.json`

## Dependencies
- Detail Resolver Engine (resolved detail manifest)
- Variant Generator (variant manifest)
- Installation Sequence Engine (sequence manifest)

## Governance
- Runtime-derived, recomputable, deterministic
- No rendering in this subsystem
- Renderers remain external
- No unsupported detail may enter package silently
- May not write to Construction_Kernel
