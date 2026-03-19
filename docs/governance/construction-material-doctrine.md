# Construction Material Doctrine

## Purpose

Define governed rules for how construction materials are classified, referenced, and validated within the Construction domain. Material doctrine prevents the system from becoming a manufacturer catalog and ensures material references remain canonical, bounded, and physics-grounded.

---

## Material Principle

Construction OS models canonical materials rather than manufacturer products. Materials are classified by physical behavior and construction role, not by brand, product line, or trade name. Manufacturer products map to canonical material classes; they do not define them.

---

## Material Hierarchy

The canonical material hierarchy is:

1. **Material physics** — fundamental physical behavior (polymer, metal, mineral, organic, composite)
2. **Canonical material class** — construction-recognized material category (e.g., TPO membrane, EPDM rubber, galvanized steel, extruded aluminum, portland cement concrete)
3. **Construction material role** — function within an assembly (e.g., waterproofing membrane, structural substrate, thermal insulation, vapor retarder)
4. **Assembly component** — positioned material within a composition graph
5. **Manufacturer product mapping** — specific product mapped to canonical class (external reference, not canonical truth)

Products map upward to canonical material classes. Canonical material classes are defined by physical behavior and construction convention, not by products.

---

## Canonical Material Class Rule

Canonical material classes are the governed vocabulary for material references within Construction OS. All material references in assemblies, compositions, compatibility rules, and truth events must use canonical material classes.

- Canonical material classes are defined in the Construction Material Taxonomy.
- New material classes may only be admitted through governed determination.
- Runtime, VKBUS, and downstream consumers must not invent material classes.

---

## Manufacturer Product Boundary Rule

Manufacturer products are external references, not canonical truth objects. The system may record that a specific product maps to a canonical material class, but:

- Product names must not appear in composition graphs as material identifiers.
- Product specifications must not replace canonical material class properties.
- Product catalogs must not be embedded in kernel architecture.
- Product-level detail belongs in evidence surfaces, not in canonical truth.

---

## Material Compatibility Rule

Compatibility between materials must be expressed in terms of canonical material classes, not products. Compatibility rules reference material physics and known construction interactions. Compatibility determinations must be traceable to source evidence (standards, test data, manufacturer technical guidance as evidence).

---

## Fail-Closed Material Rule

Assemblies referencing undefined material classes must fail closed on:
- Composition completeness claims
- Buildability claims
- Compatibility validation
- Drawing generation

The system must not silently substitute, infer, or default material classes.

---

## Relationship to Other Doctrine

- **Composition Model**: Materials are assigned to components within composition graphs. Material doctrine governs what materials may be referenced.
- **Identity System**: Materials do not carry independent identity in the same sense as assemblies. Material identity is the canonical class itself.
- **Evidence System**: Material selections must be traceable to source evidence.
- **Interface Model**: Interface conditions may reference material compatibility at boundaries.
- **Scope Model**: Material procurement responsibility follows scope classification.

Material doctrine must not redefine composition, identity, evidence, interface, or scope.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
