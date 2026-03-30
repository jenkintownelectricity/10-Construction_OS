# Construction Detail Applicability Model

## Purpose

Determine which canonical construction detail logic applies to a given construction condition. The applicability model is the governed selection layer between construction truth (assemblies, interfaces, materials, scope) and detail logic emission.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Composition Model
    → Interface Model
    → Material Taxonomy
    → Scope Boundary Model
    → View Intent Model
    → Detail Applicability Model  ← this document
    → Detail Schema
    → Drawing Instruction IR
    → Construction_Runtime
```

The Detail Applicability Model sits after the domain models and before detail schema. It consumes construction conditions and selects the applicable canonical detail logic.

---

## Applicability Inputs

Detail applicability rules evaluate the following inputs:

| Input | Source | Description |
|---|---|---|
| `assembly_type` | Composition Model | The type of assembly at the condition |
| `material_class` | Material Taxonomy | The canonical material class of relevant components |
| `interface_type` | Interface Model | The type of interface condition (termination, transition, penetration, etc.) |
| `substrate_type` | Material Taxonomy | The canonical material class of the substrate |
| `climate_zone` | Project context | Environmental exposure classification |
| `dimensional_conditions` | Composition / project data | Height, thickness, span, or other measurable parameters |
| `scope_condition` | Scope Boundary Model | Scope classification of the condition |
| `coordination_condition` | Scope Boundary Model | Coordination obligations at the condition |

---

## Applicability Rule Structure

Each applicability rule must specify:

| Field | Description |
|---|---|
| `rule_id` | Governed identifier for the applicability rule |
| `condition_pattern` | The set of input conditions this rule matches |
| `applies_detail` | The canonical detail logic definition selected by this rule |
| `parameter_bindings` | Input values bound to detail parameters |
| `preconditions` | Conditions that must be true for this rule to apply |
| `priority` | Resolution order when multiple rules match |

---

## Applicability Example

```
condition:
  interface_type: roof_to_parapet
  membrane_class: epdm_membrane
  substrate: concrete_deck
  parapet_substrate: cmu
  parapet_height: 24in

applies_detail: EPDM_PARAPET_FLASHING_STANDARD

parameter_bindings:
  membrane_type: epdm_membrane
  parapet_height: 24in
  substrate: cmu
  base_flashing_height: calculated
```

---

## Applicability Posture

Applicability rules select governed canonical detail logic. They do not:
- Generate geometry
- Create new detail definitions
- Infer construction logic
- Override detail parameters without governed basis

Applicability is a selection mechanism, not a creation mechanism.

---

## Multiple Match Rule

When multiple applicability rules match a condition:
1. Rules are evaluated by priority order.
2. If priorities are equal, the condition must be flagged for governed resolution.
3. The system must not silently select between ambiguous matches.

---

## Fail-Closed Rule

If no detail applicability rule matches a condition:
- The condition must be marked unresolved.
- The system must not generate a detail for the condition.
- The system must not fall back to a generic or default detail.
- The deficiency must be surfaced to review workflows.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine: `Construction_Kernel/docs/governance/construction-detail-doctrine.md`
