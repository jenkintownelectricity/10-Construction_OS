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

## Purification Record

| Field | Value |
|-------|-------|
| **Purification** | Option A — Atlas purified to spatial context layer only |
| **Date** | 2026-03-21 |
| **Drift Corrected** | Prior UI/application implementation (React/Next.js pages, AI control plane, branding system, construction tools) removed |
| **UI Migrated To** | Construction_Application_OS (sole UI surface) |
| **AI Control Plane Migrated To** | Construction_Application_OS |
| **Branding System Migrated To** | Construction_Application_OS |
| **Spatial Context Preserved** | Spatial object graph types, context resolution types, spatial selectors, anchors, navigable objects |

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
> **Atlas Role:** Core spatial construction context layer — NOT a UI surface. NOT an execution layer.
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

## Atlas Defines

- Spatial object types and graph structure (`src/graph/`)
- Context resolution types (`src/context/`)
- Spatial selectors, anchors, and navigable objects (`src/selectors/`)

## Atlas Must NOT Contain

- React components
- UI rendering logic
- Workspace layout systems
- Panel orchestration
- Runtime artifact generation
- Execution pipeline logic
- AI control plane
- Branding or application configuration
- Application settings or persistence

All UI rendering is owned exclusively by Construction_Application_OS.
All artifact generation is owned exclusively by Construction_Runtime.

## Project Structure

```
Construction_Atlas/
├── README.md                           ← This file
├── package.json                        ← Spatial context layer metadata
├── tsconfig.json                       ← TypeScript configuration
├── src/
│   ├── index.ts                        ← Public type exports
│   ├── graph/
│   │   └── spatial-object-graph.ts     ← Spatial object graph types
│   ├── context/
│   │   └── context-resolution.ts       ← Context resolution types
│   └── selectors/
│       └── spatial-selectors.ts        ← Selectors, anchors, navigable objects
├── schemas/                            ← JSON schemas (future)
└── docs/
    └── system/                         ← System documentation
```

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
- **NOT** an application shell

All UI rendering is owned exclusively by Construction_Application_OS.
All execution is owned by Construction_Runtime.
