# Construction View Intent Model

## Purpose

Define the canonical model for view intent within the Construction domain. View intent is the governed bridge between domain truth (assemblies, compositions, interfaces, materials, scope) and drawing generation. It determines what must be shown, at what depth, and through which representation type.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Identity System
    → Assembly Composition Model
    → Material Taxonomy
    → Interface Model
    → Scope Boundary Model
    → View Intent Model  ← this document
    → Detail Applicability Model
    → Drawing Instruction IR
    → Construction_Runtime
```

View intent sits between domain models and drawing generation. It consumes composition, material, interface, and scope information and produces governed communication requirements that drive drawing instruction generation.

---

## View Intent Structure

Every view intent must include the following fields:

| Field | Description |
|---|---|
| `view_intent_type` | The type of view being communicated (from governed vocabulary) |
| `target_condition` | The construction condition this view is intended to communicate |
| `focus_objects` | The specific assemblies, components, or interfaces that are the primary subject |
| `representation_depth` | The level of detail required for this communication |
| `required_annotations` | Annotations that must appear for communication completeness |
| `required_dimensions` | Dimensions that must appear for fabrication or installation clarity |

---

## View Types

| View Type | Description |
|---|---|
| `plan_view` | Horizontal cut or top-down representation of construction conditions |
| `section_view` | Vertical cut through assembly showing internal composition and layering |
| `elevation_view` | Vertical projection showing exterior face or profile |
| `detail_view` | Enlarged representation of a specific condition requiring close communication |
| `axon_view` | Three-dimensional axonometric representation showing spatial relationships |

View types are the governed vocabulary. Runtime and downstream consumers must not invent view types outside this vocabulary. New view types require governed admission.

---

## Representation Depth

| Depth | Description |
|---|---|
| `system_level` | Shows major assembly boundaries and system relationships; no internal layering |
| `assembly_level` | Shows assembly composition including primary layers and components |
| `component_level` | Shows individual components, their roles, and relationships |
| `fastening_level` | Shows mechanical connections, attachment methods, and penetration details |

Representation depth governs the level of detail in the view. Depth is declared by intent, not inferred from scale. A detail view at `component_level` shows different information than the same condition at `fastening_level`.

---

## View Intent Inputs

View intent consumes the following as governed inputs:

| Input | Source |
|---|---|
| Assembly composition | Composition Model / Assembly Graph |
| Material classes | Material Taxonomy |
| Interface conditions | Interface and Adjacent Systems Model |
| Scope classifications | Scope Boundary Model |
| Identity context | Assembly Identity System |

All inputs must be resolved before view intent can produce complete communication requirements. Missing inputs cause the view to fail closed.

---

## View Scope Constraint

Views must respect scope boundaries:
- `in_scope` conditions are fully represented.
- `by_others` conditions are indicated but not detailed — shown as context, not as owned work.
- `out_of_scope` conditions are not represented unless required as spatial context.
- `coordination_required` conditions are flagged for review.

View intent must not represent by-others work as in-scope work.

---

## Annotation Requirements

Views must declare required annotations. Annotation types include:

| Annotation Type | Description |
|---|---|
| `material_callout` | Identifies the canonical material class of a component |
| `dimension` | Provides measurement for fabrication or installation |
| `note` | Provides installation instruction or clarification |
| `reference` | Points to a detail, specification section, or standard |
| `scope_indicator` | Marks scope boundaries (in-scope vs. by-others) |
| `status_marker` | Indicates truth state (proposed, approved, built, observed) |

---

## Fail-Closed View Rule

A view must not be generated if:
- View intent type is undeclared
- Target condition is unresolved
- Focus objects have unresolved identity
- Required materials reference undefined material classes
- Required interfaces are undeclared
- Required scope classifications are unresolved
- Representation depth is undeclared

The system must surface the deficiency rather than generating an incomplete view.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine: `Construction_Kernel/docs/governance/construction-view-intent-doctrine.md`
