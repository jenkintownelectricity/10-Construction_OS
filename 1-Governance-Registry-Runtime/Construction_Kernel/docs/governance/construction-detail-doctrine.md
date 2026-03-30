# Construction Detail Doctrine

## Purpose

Define governed rules for how construction details are selected, represented, parameterized, and controlled within the Construction domain. Detail doctrine prevents uncontrolled detail variant growth and ensures drawing logic originates from domain truth rather than runtime invention.

---

## Detail Principle

Construction details are governed construction logic, not static drawings. Details encode how construction conditions must be built. They are selected by applicability rules, represented as structured logic, parameterized by construction conditions, and emitted as drawing instructions. Details must not be invented by runtime or downstream consumers.

---

## Canonical Detail Logic Rule

A detail family must be represented by one canonical logic definition unless a true logic change is required. Parameter variation alone must not create a new detail definition.

Examples of parameter variation (same canonical logic):
- Different membrane type on the same parapet condition
- Different insulation thickness on the same roof edge
- Different substrate on the same base flashing detail

Examples of true logic change (different canonical logic):
- Mechanically attached vs. adhered membrane termination
- Metal coping vs. membrane cap on parapet
- Through-wall flashing vs. surface-applied flashing

If a construction condition cannot be satisfied by parameterization of a canonical detail, the system must mark the condition unresolved rather than creating an uncontrolled detail variant.

---

## Detail Applicability Rule

Details are selected through governed applicability rules that match construction conditions to canonical detail logic. Applicability rules must reference:
- Assembly type
- Material class (from canonical taxonomy)
- Interface type
- Substrate type
- Relevant dimensional or environmental conditions

Applicability rules select details. They do not generate geometry.

---

## Detail Schema Rule

Details must be represented as structured construction logic with explicit components, relationships, material references, and parameter inputs. Details must not be stored as static drawing files, opaque geometry blobs, or unstructured text descriptions.

---

## Drawing Instruction IR Rule

Drawing instructions must be emitted from detail logic through a governed, engine-agnostic instruction layer. The IR must remain construction-semantic. It must not encode vendor-specific CAD commands, application-specific scripting, or renderer-specific instructions.

---

## Fail-Closed Detail Rule

If no detail applicability rule matches a condition, the condition must be marked unresolved. If detail logic is incomplete or parameters cannot be resolved, the detail must not be emitted. If IR inputs are incomplete, drawing generation must fail closed.

The system must surface deficiencies rather than generating incomplete or incorrect construction details.

---

## Detail Variant Control Rule

The system must not accumulate uncontrolled detail variants. Every detail in the system must trace to a canonical detail logic definition. Detail families must be periodically auditable for variant sprawl. Duplicate logic masquerading as separate details is a governance violation.

---

## Relationship to Other Doctrine

- **Composition Model**: Details reference assembly composition for component context.
- **Interface Model**: Details often apply at interface conditions (terminations, transitions, penetrations).
- **Material Taxonomy**: Details reference canonical material classes for component materials.
- **Scope Model**: Details respect scope boundaries — by-others components are indicated, not detailed.
- **View Intent Model**: View intent determines how details are communicated; detail logic determines what is communicated.
- **Identity System**: Detail definitions carry governed identity for version tracking and continuity.
- **Evidence System**: Detail selections must be traceable to source evidence.

Detail doctrine must not redefine composition, interface, material, scope, view intent, identity, or evidence.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
