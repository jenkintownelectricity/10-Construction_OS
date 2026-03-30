# Construction Assembly Identity System

## Purpose

Define the architectural system for governing construction object identity within the Construction domain. This system determines how objects are identified, how identity persists across revisions, and how identity operations are structured.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Identity System
    → Construction Truth Spine
    → Construction_Runtime
```

The Assembly Identity System sits within Construction_Kernel alongside the Construction Truth Spine. The Truth Spine records events against identities governed by this system. Construction_Runtime consumes identity rules but does not define them.

---

## Identity-Bearing Object Types

The following object types carry governed identity within the Construction domain:

| Object Type | Description |
|---|---|
| assembly | A proposed or real construction configuration |
| detail | A specific construction detail within or across assemblies |
| material application | A specific application of material to a location or assembly |
| condition | An observed physical state of a building component |
| approval | A formal acceptance or rejection decision |
| observation set | A collection of related field observations |
| deliverable | A document, drawing, or package produced for a purpose |
| deviation | A departure from approved design or specification |
| project location | A governed spatial reference within the project |

---

## Identity vs Representation

The following are representation artifacts and are not identity:

| Artifact | Rule |
|---|---|
| title | title ≠ identity |
| label | label ≠ identity |
| drawing callout | drawing callout ≠ identity |
| sheet position | sheet position ≠ identity |
| document path | document path ≠ identity |

Representation artifacts may change without affecting identity. They may remain stable while identity changes. No representation artifact substitutes for governed identity.

---

## Identity Basis

Identity determination draws on the following:

- **Object class** — the type of construction object
- **Project context** — the project within which the object exists
- **Location context** — the spatial position or zone within the project
- **Relational context** — relationships to other identified objects
- **Revision continuity evidence** — traceable evidence supporting continuity across revisions
- **Governed identity decision** — an explicit determination by a governed process

No single basis element is sufficient alone. Identity requires governed evaluation of available evidence.

---

## Identity States

| State | Description |
|---|---|
| unknown | No identity determination has been attempted |
| provisional | An identity has been assigned but not yet confirmed through governed evaluation |
| established | Identity has been confirmed through governed evaluation with supporting evidence |
| disputed | Identity continuity is challenged by conflicting evidence or competing claims |
| superseded | Identity has been replaced by a successor through a governed operation |

---

## Identity Operations

| Operation | Description |
|---|---|
| create | A new identity is established for a previously unidentified object |
| continue | An existing identity is confirmed to persist across a revision or event |
| split | One identity divides into two or more successor identities |
| merge | Two or more identities combine into a single successor identity |
| replace | One identity is explicitly replaced by a new identity |
| supersede | An identity is retired in favor of a successor with an explicit relationship |
| retire | An identity is permanently closed with no successor |

All identity operations must be explicit and recorded. Implicit identity changes are governance violations.

---

## Assembly Continuity Rule

Assemblies across revisions may only be treated as the same object when continuity is supported by governed identity evidence. Positional, naming, or structural similarity alone does not establish continuity. Continuity requires governed evaluation and explicit determination.

---

## Failure Rule

If identity continuity is unresolved, the system must fail closed on sameness claims. Unresolved identity must not be silently treated as established. The system must not infer continuity where governed evidence is absent.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine for identity rules: `Construction_Kernel/docs/governance/construction-assembly-identity-doctrine.md`
