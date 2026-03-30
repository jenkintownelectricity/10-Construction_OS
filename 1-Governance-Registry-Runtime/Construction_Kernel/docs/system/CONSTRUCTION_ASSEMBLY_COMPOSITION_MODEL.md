# Construction Assembly Composition Model

## Purpose

Define the canonical compositional structure of construction assemblies so the system can represent machine-readable, buildable assembly relationships rather than flat text descriptions.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Identity System
    → Assembly Composition Model  ← this document
    → Assembly Graph
    → Construction Truth Spine
    → Construction_Runtime
```

The Composition Model defines how assemblies are structured internally. The Identity System defines how assemblies persist across revisions. The Truth Spine records events against identified, composed assemblies.

---

## Assembly vs Component

| Concept | Definition |
|---|---|
| Assembly | A governed, identity-bearing construction object representing a buildable configuration. Assemblies are the primary truth-bearing compositional unit. |
| Component | A constituent part within an assembly. Components contribute to physical realization. Components may carry independent identity when they are themselves assemblies. |

An assembly is not merely a collection. It is a governed, typed, bounded composition with explicit relationships between its parts.

---

## Allowed Component Roles

Components within an assembly carry explicit roles:

| Role | Description |
|---|---|
| primary | The principal functional element of the assembly |
| substrate | The surface or structure to which the assembly is applied |
| backing | Material providing support behind the primary element |
| blocking | Solid material providing attachment or load transfer points |
| fastener | Mechanical connection element |
| sealant | Material providing environmental separation |
| insulation | Material providing thermal or acoustic separation |
| finish | Exposed surface material |
| flashing | Material directing water away from vulnerable joints |
| reinforcement | Material providing additional structural capacity |
| accessory | Secondary functional element supporting the primary |
| transition | Material or element bridging between different assembly types |

Component roles are not exhaustive. New roles may be admitted through governed determination. Roles must not be invented ad hoc by runtime consumers.

---

## Allowed Relationship Families

Relationships between components are grouped into families:

| Family | Description |
|---|---|
| contains | Parent assembly contains child component |
| supports | One component structurally supports another |
| attaches_to | One component is mechanically fastened to another |
| covers | One component covers the surface of another |
| seals | One component provides environmental seal against another |
| insulates | One component provides thermal/acoustic separation from another |
| terminates_at | A component or assembly ends at a defined boundary |
| transitions_to | A component bridges to a different material or assembly type |
| interfaces_with | An assembly meets another assembly or building edge |

Every relationship must belong to a recognized family. Untyped or ad-hoc relationships are governance violations.

---

## Layering Semantics

Many construction assemblies are layered build-ups applied to a substrate. Layering rules:

- Layer order must be explicit (numbered or sequenced from substrate outward).
- Each layer corresponds to a component with an assigned role.
- Layer boundaries define where one component ends and the next begins.
- Layer order must not be inferred from document position or drawing arrangement.
- Gaps in layer sequence must be explicitly declared or flagged as incomplete.

---

## Support Semantics

Support relationships define how components bear load or provide backing:

- Support must be explicitly typed (structural, blocking, backing, furring).
- Support direction must be determinable from context (gravity, lateral, attachment).
- Missing support where structurally required must cause the composition to be marked incomplete.

---

## Attachment Semantics

Attachment relationships define mechanical connections:

- Attachment method must be typed (screw, nail, adhesive, clip, weld, embed).
- Attachment target must reference a specific component.
- Attachment through multiple layers must declare the penetration path.

---

## Termination Semantics

Terminations define where assemblies or components end:

- Termination type must be explicit (free edge, return, cap, transition, abutment).
- Terminations at building edges must declare the edge condition.
- Unterminated assemblies must be flagged as incomplete.

---

## Adjacency Hooks

Adjacency hooks declare where an assembly's composition boundary meets external conditions:

- Adjacent assembly (different assembly type meeting at a shared boundary)
- Building edge (roof edge, foundation, opening, penetration)
- System boundary (MEP penetration, structural interface)

Adjacency hooks are declared, not resolved, at the composition level. Resolution occurs through the Interface and Adjacent Systems Model.

---

## Detail Linkage Hooks

Details are governed drawing-level instructions tied to specific composition conditions:

- A detail hook declares that a specific composition condition requires a detail.
- Detail hooks reference composition nodes or edges, not document locations.
- Detail applicability is determined by composition state, not by drawing sheet.

Detail linkage is declared at the composition level. Resolution occurs through the Detail Applicability Model.

---

## Composition Completeness Posture

An assembly's composition may be in one of the following states:

| State | Description |
|---|---|
| complete | All required components, relationships, layers, terminations, and interfaces are declared |
| partial | Some components or relationships are declared but gaps exist |
| stub | Only the assembly identity and type are declared; no internal composition |
| disputed | Conflicting composition evidence exists |

The system must not treat partial, stub, or disputed compositions as complete. Completeness claims require all structural, layering, support, attachment, termination, and interface relationships to be resolved.

---

## Why This Matters

Flat text descriptions of assemblies cannot be reliably parsed, validated, or used for deterministic drawing generation. A governed composition model enables:

- Machine-readable assembly structure
- Deterministic validation of buildability
- Governed detail applicability
- Traceable composition changes through the truth spine
- Fail-closed detection of incomplete or ambiguous assemblies

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine: `Construction_Kernel/docs/governance/construction-assembly-composition-doctrine.md`
