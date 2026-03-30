# Construction Detail Schema

## Purpose

Represent construction detail logic as structured construction knowledge. Details are canonical construction logic definitions — not static drawings, opaque geometry files, or unstructured text. The detail schema defines how detail logic is structured, parameterized, and connected to the broader domain model.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Composition Model
    → Interface Model
    → Material Taxonomy
    → Detail Applicability Model
    → Detail Schema  ← this document
    → Drawing Instruction IR
    → Construction_Runtime
```

The Detail Schema sits between applicability selection and drawing instruction emission. Applicability selects the detail. The schema defines the detail's construction logic. The Drawing Instruction IR emits drawing instructions from the resolved detail.

---

## Detail Schema Fields

| Field | Description |
|---|---|
| `detail_id` | Governed identifier for the canonical detail logic definition |
| `detail_family` | The family of construction conditions this detail addresses |
| `components` | Ordered list of construction components within the detail |
| `relationships` | Typed relationships between components |
| `material_references` | Canonical material classes referenced by components |
| `parameter_inputs` | Named parameters that vary the detail for specific conditions |
| `preconditions` | Conditions that must be satisfied before this detail is valid |
| `output_intent` | The communication purpose of the detail (references View Intent Model) |

---

## Detail Components

Components within a detail are construction elements with explicit roles:

| Example Component | Role |
|---|---|
| `membrane_extension` | Waterproofing membrane carried up or across a condition |
| `base_flashing` | Flashing material applied at the base of a vertical surface |
| `termination_bar` | Mechanical bar securing membrane or flashing at termination |
| `counterflashing` | Metal flashing covering and protecting the termination |
| `sealant` | Joint sealant at termination or transition points |
| `cant_strip` | Angled transition between horizontal and vertical surfaces |
| `metal_edge` | Sheet metal edge profile at roof perimeter |
| `cleat` | Concealed metal strip securing edge metal or coping |
| `insulation_extension` | Insulation carried into the detail condition |
| `fastener_pattern` | Mechanical attachment at specified spacing |

Components reference canonical material classes from the Material Taxonomy.

---

## Detail Relationships

Relationships between detail components follow the same typed families as the Composition Model:

| Relationship | Description |
|---|---|
| `overlaps` | One component overlaps another for weatherproofing continuity |
| `fastened_to` | One component is mechanically attached to another |
| `covers` | One component covers and protects another |
| `seals` | One component provides sealant closure against another |
| `supports` | One component provides structural backing for another |
| `terminates_at` | A component ends at a defined boundary within the detail |
| `transitions_to` | A component transitions to a different material or condition |

---

## Detail Relationships Example

```
membrane_extension overlaps base_flashing
base_flashing fastened_to substrate
termination_bar fastened_to substrate
termination_bar covers membrane_extension termination
counterflashing covers termination_bar
sealant seals counterflashing at top edge
```

---

## Parameter Inputs

Parameters allow a single canonical detail logic definition to serve multiple construction conditions:

| Example Parameter | Description |
|---|---|
| `membrane_type` | Canonical material class of the membrane |
| `parapet_height` | Height of the parapet condition |
| `substrate` | Canonical material class of the substrate |
| `insulation_thickness` | Thickness of insulation in the assembly |
| `climate_zone` | Environmental exposure classification |
| `edge_condition` | Type of edge (drip, gravel stop, coping) |
| `attachment_method` | Mechanical, adhered, or ballasted |

Parameters bind to applicability rule outputs. Parameter values must be resolvable before detail emission.

---

## Canonical Detail Logic Rule

A detail family must be represented by one canonical logic definition unless a true logic change is required.

- Parameter variation does not create new definitions.
- True logic change (different components, different relationships, different construction sequence) warrants a new definition.
- If a condition cannot be satisfied by parameterization, the condition must be marked unresolved.

---

## Schema Posture

The detail schema references but does not redefine:
- **Composition**: Detail components align with composition component roles
- **Interfaces**: Details apply at interface conditions
- **Materials**: Detail components reference canonical material classes
- **Scope**: Details respect scope boundaries
- **View Intent**: Detail output intent references view intent types

---

## Fail-Closed Rule

A detail must not be emitted if:
- Required components are undefined
- Required relationships are unresolved
- Material references point to undefined material classes
- Parameter inputs cannot be resolved
- Preconditions are not satisfied

The system must surface the deficiency rather than emitting incomplete detail logic.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine: `Construction_Kernel/docs/governance/construction-detail-doctrine.md`
