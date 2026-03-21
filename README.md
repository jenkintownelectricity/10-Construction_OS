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
> **Atlas Role:** Core spatial construction context layer — NOT a UI surface.
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

All UI rendering is owned exclusively by Construction_Application_OS.

## Dependencies

| Dependency | Relationship |
|------------|-------------|
| **Construction_Kernel** | Consumes construction domain ontology and truth boundaries |
| **ValidKernel_Geometry_Kernel** | Consumes universal spatial primitives (points, surfaces, boundaries, transforms, adjacency, containment) |

## Downstream Consumers

| Consumer | Relationship |
|----------|-------------|
| **Construction_Runtime** | Consumes spatial context for deterministic artifact generation |
| **Construction_Application_OS** | Consumes spatial selectors, anchors, and navigable objects for UI rendering |
