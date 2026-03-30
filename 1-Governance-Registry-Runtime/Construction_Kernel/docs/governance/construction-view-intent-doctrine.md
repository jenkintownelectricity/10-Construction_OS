# Construction View Intent Doctrine

## Purpose

Define governed rules for how construction conditions are translated into view intent — the governed bridge between domain truth and drawing generation. View intent defines what must be communicated, at what depth, and through which representation type.

---

## View Intent Principle

View intent governs the communication purpose of a drawing view. Every drawing view must have an explicit, typed intent that defines what construction condition is being communicated, to whom, and at what level of detail. Views without governed intent must not be generated.

---

## View Intent Independence Rule

View intent defines communication requirements. View intent does not define:
- Materials (governed by Material Taxonomy)
- Composition (governed by Composition Model)
- Interfaces (governed by Interface Model)
- Scope (governed by Scope Boundary Model)
- Identity (governed by Identity System)

View intent may reference all of these as inputs but must not redefine or expand them.

---

## View Type Rule

Every view must carry an explicit view type from the governed vocabulary. View types define the geometric posture of the representation. Runtime and downstream consumers must not invent view types.

---

## Representation Depth Rule

Every view must declare its representation depth — the level of detail required for the communication purpose. Representation depth is governed, not inferred from drawing scale or sheet size.

---

## Annotation and Dimension Rule

Views must declare required annotations and dimensions. Annotations and dimensions are communication obligations, not decorative additions. Missing required annotations cause the view to fail closed on communication completeness.

---

## View Intent Reference Rule

View intent may reference canonical material classes defined by the Material Taxonomy. View intent must not define or expand the material taxonomy. If a view references an undefined material class, the view must fail closed.

---

## Fail-Closed View Rule

If view inputs are incomplete, reference undefined materials, or lack required intent declarations, the drawing view must not be generated. The system must surface the deficiency rather than generating an incomplete or misleading view.

---

## Relationship to Other Doctrine

- **Composition Model**: View intent selects which composition elements to represent.
- **Material Taxonomy**: View intent references materials for annotation and representation purposes.
- **Interface Model**: View intent may focus on interface conditions for detail communication.
- **Scope Model**: View intent respects scope boundaries — views must not represent by-others work as in-scope.
- **Truth Spine**: View intent is a derived communication act, not a truth event itself.

View intent must not redefine composition, material, interface, scope, or identity doctrine.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
