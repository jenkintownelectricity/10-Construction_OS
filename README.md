# Construction Atlas

**(formerly Construction_Atlas_UI)**

Canonical spatial construction context layer binding geometry and construction meaning.

## Rename Lineage

| Field | Value |
|-------|-------|
| **Previous Name** | Construction_Atlas_UI |
| **Current Name** | Construction_Atlas |
| **Version** | V2 |
| **Reason** | Separation of spatial context truth layer and UI surface |
| **Status** | Permanent rename — lineage annotation required in all architecture and registry documentation |

## Construction OS Core Architecture (FROZEN)

```
Universal_Truth_Kernel
├── ValidKernel_Geometry_Kernel
├── ValidKernel-Governance
└── Construction_Kernel
     ├── Construction_Atlas             ← YOU ARE HERE (Spatial Context Layer)
     │        ↓
     Construction_Runtime
              ↓
     Construction_Application_OS
```

> **Architecture Status:** FROZEN
> **Atlas Role:** Core spatial construction context layer — NOT a UI surface. NOT an execution layer. UI-aware but UI-independent.
> **UI Authority:** Construction_Application_OS is the sole UI surface of Construction OS.

## Purpose

Construction_Atlas is a **truth/context layer** that resolves spatial construction conditions:

- **What object exists** — spatial construction object graph
- **Where it exists** — zones and placements
- **What surrounds it** — adjacency relationships
- **What rules apply** — interface context

## Responsibilities

- Spatial construction object graph
- Zones and placements
- Adjacency relationships
- Interface context
- Spatial anchors and selectors

## Atlas May Define

- Spatial selectors
- Anchors
- Navigable spatial objects
- Context resolution

## Atlas Must NOT Contain

- React components
- UI rendering logic
- Workspace layout systems
- Panel orchestration
- Runtime artifact generation
- Execution pipeline logic

All UI rendering is owned exclusively by Construction_Application_OS.
All artifact generation is owned exclusively by Construction_Runtime.

## Dependencies

| Dependency | Relationship |
|------------|-------------|
| **Construction_Kernel** | Consumes construction domain ontology and truth boundaries |
| **ValidKernel_Geometry_Kernel** | Consumes universal spatial primitives (points, surfaces, boundaries, transforms, adjacency, containment) |

## Downstream Consumers

| Consumer | Relationship |
|----------|-------------|
| **Construction_Runtime** | Consumes spatial context for deterministic artifact generation |
| **Construction_Application_OS** | Consumes navigation context — spatial selectors, anchors, and navigable objects for UI rendering |
| **Construction_Reference_Intelligence** | Observes architecture context for intelligence derivation and guidance relay |

## Boundary Statement

Construction_Atlas is the **spatial context layer**. It is:
- **NOT** a UI surface
- **NOT** an execution layer

All UI rendering is owned exclusively by Construction_Application_OS.
All execution is owned by Construction_Runtime.
