# Variant Generation Contract — Wave 14

## Contract Version
14.3.0

## Purpose
Generates derived parameterized detail variants from canonical detail families.
Canonical detail IDs remain unchanged. Variants produce derived payloads only.
Variant IDs are derived, not canonical truth.

## Authority
- Construction_Runtime (derived, runtime-only)
- Construction_Kernel provides canonical detail families (frozen, read-only)

## Inputs
- Canonical detail ID (from resolved_detail_manifest)
- Parameter specifications (geometry hints, field measurements)

## Outputs
- detail_variant_payload.json (per variant)
- variant_manifest.json (collection)

## Contract Object: DetailVariant
```json
{
  "variant_id": "derived ID: [canonical_detail_id]-V[NNN]",
  "canonical_detail_id": "frozen kernel ID",
  "parameters": {"param_name": "value"},
  "provenance": {
    "canonical_detail_id": "string",
    "generation_source": "variant_generator",
    "contract_version": "14.3.0"
  }
}
```

## Supported Parameters
- parapet_height (4–96 inches)
- membrane_thickness (0.030–0.120 inches)
- pipe_diameter (0.5–24 inches)
- curb_size (6–72 inches)
- drain_diameter (2–12 inches)
- reglet_depth (0.25–2.0 inches)
- joint_width (0.5–6 inches)
- overflow_size (2–12 inches)

## Rules
1. Canonical detail IDs remain unchanged.
2. Variants produce derived payloads only.
3. Parameters must validate against schema and allowed ranges.
4. Prohibited combinations from prior waves must be rejected.
5. Every variant must preserve provenance back to canonical detail ID.
6. Deterministic ordering and deterministic variant IDs required.

## Governance
- This subsystem may NOT alter canonical detail IDs.
- This subsystem may NOT write to Construction_Kernel.
- All outputs are runtime-derived and recomputable.
