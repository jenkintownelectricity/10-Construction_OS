# Detail DNA Runtime Interface Contract

**Authority:** Construction_Runtime (interface contract only)
**Source of Truth:** Construction_Kernel (Detail DNA schemas and data)
**Wave:** 13A
**Status:** Active

## Purpose

This contract defines how Construction_Runtime consumes Detail DNA families from Construction_Kernel. The runtime executes detail resolution and parameterization but does NOT define detail classification, taxonomy, or compatibility rules.

## Authority Boundary

| Responsibility | Owner |
|---------------|-------|
| Detail family definitions | Construction_Kernel |
| Detail DNA schema | Construction_Kernel |
| Detail taxonomy (system, class, condition, variant, assembly_family) | Construction_Kernel |
| Material compatibility rules | construction_dna |
| Detail family resolution at runtime | Construction_Runtime |
| Detail parameterization | Construction_Runtime |
| Detail instance creation | Construction_Runtime |

## Input Contract

The runtime receives detail resolution requests containing:

```json
{
  "system": "LOW_SLOPE",
  "class": "TERMINATION",
  "condition": "PARAPET",
  "assembly_family": "EPDM",
  "parameters": {
    "membrane_type": "EPDM_060",
    "parapet_height": 36,
    "substrate": "CMU"
  }
}
```

### Required Fields
- `system` — Must match a valid system enum from `detail_dna_schema.json`
- `class` — Must match a valid class enum
- `condition` — Must match a valid condition enum
- `assembly_family` — Must match a valid assembly_family enum

### Optional Fields
- `variant` — If omitted, runtime selects the default variant for the condition
- `parameters` — Detail-specific parameters for instance generation

## Output Contract

The runtime returns a resolved detail family reference:

```json
{
  "resolved_detail_id": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
  "resolution_status": "resolved",
  "detail_family": { },
  "parameter_bindings": { },
  "compatible_material_classes": ["EPDM"],
  "risk_tags": ["UV_EXPOSURE", "WIND_UPLIFT"],
  "related_details": [
    {
      "detail_id": "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01",
      "relationship": "adjacent_to"
    }
  ]
}
```

### Resolution Status Values
- `resolved` — Exactly one detail family matched
- `ambiguous` — Multiple families matched; disambiguation required
- `not_found` — No matching family exists in kernel
- `incompatible` — Family exists but material compatibility check failed

## Fail-Closed Rules

1. If no matching detail family exists, return `not_found`. Do NOT synthesize a detail.
2. If multiple families match without disambiguation, return `ambiguous`. Do NOT select arbitrarily.
3. If material compatibility fails, return `incompatible`. Do NOT override compatibility rules.
4. All resolution decisions MUST be logged in the audit trail.

## Data Source Paths

| Data | Path | Format |
|------|------|--------|
| Detail families | `Construction_Kernel/data/detail_dna/*.json` | JSON per family |
| Detail DNA schema | `Construction_Kernel/schemas/detail_dna_schema.json` | JSON Schema |
| Tag taxonomy | `Construction_Kernel/data/detail_tags.json` | JSON |
| Tag index | `Construction_Kernel/data/detail_tag_index.json` | JSON |
| Route graph | `Construction_Kernel/data/detail_route_index.json` | JSON |
| Material chemistry | `construction_dna` packages | TypeScript |

## Versioning

- This interface contract version: `13A`
- Construction_Kernel schema version: `13A`
- Changes to this interface MUST be coordinated with Construction_Kernel schema changes
