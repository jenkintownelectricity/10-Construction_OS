# Detail Render Contract

**Authority:** Construction_Runtime (interface contract only)
**Renderers:** CADless_drawings, holograph_details
**Wave:** 13A
**Status:** Active

## Purpose

This contract defines the interface between resolved Detail DNA families and rendering subsystems. Renderers consume geometry instructions derived from resolved details. Renderers do NOT perform detail classification, material compatibility checks, or condition resolution.

## Authority Boundary

| Responsibility | Owner |
|---------------|-------|
| Detail classification and taxonomy | Construction_Kernel |
| Detail resolution | Construction_Runtime |
| Drawing Instruction IR emission | Construction_Runtime |
| SVG rendering from IR | CADless_drawings |
| 3D mesh rendering from semantic data | holograph_details |
| Material compatibility logic | construction_dna |

## Renderer Purity Rules

Renderers MUST remain pure consumers of geometry instructions. Specifically, renderers:

1. **MAY** consume `DrawingInstructionSet` (IR) for 2D rendering
2. **MAY** consume `SemanticDetail` for 3D rendering
3. **MAY** query detail metadata (display_name, tags) for annotation
4. **MAY NOT** define detail classification logic
5. **MAY NOT** define material compatibility rules
6. **MAY NOT** resolve detail conditions
7. **MAY NOT** select detail variants based on construction logic
8. **MAY NOT** modify kernel data

## Render Input: 2D (CADless_drawings)

The runtime provides a `DrawingInstructionSet` per the existing `drawing_instruction.schema.json`:

```json
{
  "instruction_version": "0.2",
  "entities": [
    { "entity_type": "RECT", "layer": "A-COMP", "..." : "..." },
    { "entity_type": "LINE", "layer": "A-DETAIL", "..." : "..." }
  ],
  "dimensions": [],
  "text_annotations": [],
  "layers": ["A-COMP", "A-DETAIL", "A-DIMS", "A-TEXT"],
  "sheet_metadata": { "width": 24, "height": 18, "unit": "in" },
  "provenance": {
    "source_detail_id": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
    "resolved_by": "Construction_Runtime",
    "wave": "13A"
  }
}
```

## Render Input: 3D (holograph_details)

The runtime provides a `SemanticDetail` per the holograph schema:

```json
{
  "id": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
  "category": "roofing",
  "name": "EPDM Parapet Termination with Counterflashing",
  "parameters": {},
  "viewport": { "width": 600, "height": 400, "depth": 300 },
  "layers": [],
  "connections": [],
  "products": []
}
```

## Detail DNA Metadata Available to Renderers

Renderers may access the following read-only metadata for annotation and display:

| Field | Source | Usage |
|-------|--------|-------|
| `detail_id` | Detail family | Title block, reference bubbles |
| `display_name` | Detail family | Drawing title |
| `tags` | Detail family | Search indexing (not for rendering logic) |
| `assembly_family` | Detail family | Material pattern selection |
| `synonyms` | Detail family | Alternative title display |

## Fail-Closed Rules

1. If the IR contains an unsupported entity type, the renderer MUST fail — not skip silently.
2. If a required layer is missing from the IR, the renderer MUST fail.
3. Renderers MUST NOT infer or generate geometry not present in the IR.
4. All rendering failures MUST be surfaced as classified errors per the runtime error taxonomy.

## Versioning

- This contract version: `13A`
- DrawingInstructionSet version: `0.2`
- SemanticDetail schema: per holograph_details current version
