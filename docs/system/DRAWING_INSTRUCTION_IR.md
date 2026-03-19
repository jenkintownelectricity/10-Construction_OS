# Drawing Instruction IR

## Purpose

Provide an engine-agnostic, construction-semantic instruction layer for generating construction drawings. The Drawing Instruction IR represents drawing logic rather than geometry files. It bridges resolved detail logic and rendering engines without encoding vendor-specific commands.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Composition Model
    → Interface Model
    → Material Taxonomy
    → View Intent Model
    → Detail Applicability Model
    → Detail Schema
    → Drawing Instruction IR  ← this document
    → Construction_Runtime (renderer)
```

The Drawing Instruction IR is the final domain-governed layer before rendering. It consumes resolved detail logic, view intent, and material references, and emits structured instructions that any compliant renderer can interpret.

---

## IR Instruction Posture

IR instructions reference canonical component types, detail components, relationships, and representation intent rather than raw geometry primitives. The IR is construction-semantic: it describes what must be drawn in construction terms, not how pixels or vectors are emitted.

---

## IR Instruction Types

| Instruction Type | Description |
|---|---|
| `draw_component` | Emit a construction component with type, material, and position context |
| `draw_profile` | Emit a shaped profile (metal edge, counterflashing, coping) with type reference |
| `draw_relationship` | Emit the visual representation of a relationship between components |
| `place_symbol` | Place a construction symbol (fastener, anchor, weld) with spacing and type |
| `place_annotation` | Place a text annotation with content and reference target |
| `place_dimension` | Place a dimension with type, value, and reference points |
| `place_material_tag` | Place a material identification tag referencing canonical material class |
| `define_view_boundary` | Define the extent and clipping of the drawing view |
| `set_representation_depth` | Set the level of detail for subsequent instructions |

---

## IR Instruction Fields

Each IR instruction carries:

| Field | Description |
|---|---|
| `instruction_type` | One of the defined IR instruction types |
| `target_reference` | The canonical component, relationship, or condition being represented |
| `material_reference` | Canonical material class (where applicable) |
| `position_context` | Relative position within the detail or view (not absolute coordinates) |
| `parameters` | Type-specific parameters (spacing, text, dimension value, profile type) |
| `representation_intent` | How this element should be communicated (from View Intent Model) |

---

## IR Example

```
define_view_boundary
  type: detail_view
  target: EPDM_PARAPET_FLASHING_STANDARD
  depth: component_level

draw_component
  type: membrane_extension
  material: epdm_membrane
  context: from_roof_surface to parapet_face

draw_component
  type: base_flashing
  material: epdm_membrane
  context: parapet_face full_height

draw_component
  type: termination_bar
  material: galvanized_steel
  context: top_of_base_flashing

place_symbol
  type: fastener
  material: stainless_fastener
  spacing: 12in
  context: termination_bar_to_substrate

draw_profile
  type: metal_counterflashing
  material: galvanized_steel
  context: covers termination_bar

place_annotation
  text: "EPDM base flashing"
  target: base_flashing

place_dimension
  type: overlap
  value: 4in
  reference: membrane_extension to base_flashing

place_material_tag
  material: epdm_membrane
  target: base_flashing
```

---

## IR Boundary Rule

The IR must not encode:
- Vendor-specific CAD commands (AutoCAD LISP, Revit API calls)
- Application-specific scripting (Python geometry library calls)
- Renderer-specific low-level instructions (DXF entity codes, SVG path commands)
- Absolute coordinate geometry (x,y,z positions)
- File format structures (layer definitions, block references)

The IR defines what must be drawn. The renderer defines how it is geometrically emitted.

---

## Renderer Separation Rule

The IR is renderer-agnostic. It may be rendered to:
- DXF
- SVG
- PDF
- CAD-native geometry
- 3D model formats

Each renderer translates IR instructions into format-specific output. The IR itself must remain independent of any specific output format.

---

## IR Completeness Rule

A complete IR emission requires:
- All referenced components resolved in the detail schema
- All material references resolved against the canonical taxonomy
- All relationships represented
- All required annotations declared
- All required dimensions declared
- View boundary and representation depth defined

---

## Fail-Closed Rule

If required component references, relationship references, or output intent are incomplete, IR emission must fail closed. The system must not emit partial drawing instructions or silently omit unresolved elements.

IR instructions must be interpretable without reference to a specific CAD application or file format. If an instruction cannot be interpreted without vendor-specific knowledge, it is a governance violation.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Detail Schema: `Construction_Kernel/docs/system/CONSTRUCTION_DETAIL_SCHEMA.md`
- Governance doctrine: `Construction_Kernel/docs/governance/construction-detail-doctrine.md`
