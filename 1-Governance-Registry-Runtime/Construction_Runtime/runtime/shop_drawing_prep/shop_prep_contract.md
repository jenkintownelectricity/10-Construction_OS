# Shop Drawing Preparation Contract — Wave 14

## Contract Version
14.7.0

## Purpose
Prepares manifests and package structure for downstream rendering.
No direct rendering occurs in this subsystem. Renderers remain external.
Output is a deterministic manifest only.

## Authority
- Construction_Runtime (derived, runtime-only)
- Renderers (CADless_drawings, holograph_details) remain external consumers

## Inputs
- Resolved detail manifest (from detail_resolver)
- Variant manifest (from detail_variants)
- Installation sequence manifest (from installation_sequence)

## Outputs
- project_shop_drawing_manifest.json
- sheet_index.json
- drawing_package_manifest.json

## Contract Object: ShopDrawingManifest
```json
{
  "manifest_id": "string",
  "project_id": "string",
  "contract_version": "14.7.0",
  "drawing_entries": [
    {
      "sheet_id": "string",
      "sheet_number": "number",
      "canonical_detail_id": "string",
      "title": "string",
      "render_type": "canonical | variant",
      "variant_id": "optional string",
      "parameters": "optional object"
    }
  ],
  "summary": {
    "total_drawings": "number",
    "canonical_count": "number",
    "variant_count": "number"
  }
}
```

## Rules
1. No direct rendering in this wave.
2. Renderers remain external.
3. Output is a deterministic manifest only.
4. All manifest entries must reference resolved canonical detail IDs or derived variant IDs.
5. No unsupported detail may enter package silently.

## Governance
- This subsystem may NOT render drawings.
- This subsystem may NOT modify renderer behavior.
- This subsystem may NOT write to Construction_Kernel.
- All outputs are runtime-derived and recomputable.
