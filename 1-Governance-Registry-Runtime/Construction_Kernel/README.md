# Construction Kernel

The canonical kernel defining truth boundaries for the construction domain.

## Construction OS Core Architecture (FROZEN)

```
Universal_Truth_Kernel
├── ValidKernel_Geometry_Kernel
├── ValidKernel-Governance
└── Construction_Kernel                 ← YOU ARE HERE
     ├── Construction_Atlas (formerly Construction_Atlas_UI)
     │        ↓
     Construction_Runtime
              ↓
     Construction_Application_OS
```

> **Architecture Status:** FROZEN
> **Root Reference:** Universal_Truth_Kernel (reference-only / no-write in downstream passes)
> **Construction_Atlas** (formerly Construction_Atlas_UI) is a spatial context truth layer that binds geometry and construction meaning. It is NOT a UI surface. It is NOT an execution layer.
> **UI Authority:** Construction_Application_OS is the sole UI surface of Construction OS.

## Construction_Atlas Dependency

Construction_Atlas (formerly Construction_Atlas_UI) depends on Construction_Kernel for construction domain ontology. Atlas resolves spatial construction context — what object exists, where it exists, what surrounds it, and what rules apply — using the construction truth boundaries defined in this kernel combined with spatial primitives from ValidKernel_Geometry_Kernel.

## Supporting Kernels

This kernel organizes construction knowledge into seven supporting kernels:

1. Governance
2. Geometry
3. Chemistry
4. Assembly
5. Reality
6. Deliverable
7. Intelligence

This kernel operates within the truth boundary defined by Universal_Truth_Kernel. Truth doctrine is defined there and referenced here.

## Explicit Dependencies

| Dependency | Relationship |
|------------|-------------|
| **Universal_Truth_Kernel** | Root doctrine — truth boundary definition (REFERENCE-ONLY) |
| **ValidKernel_Geometry_Kernel** | Consumes universal spatial primitives for construction domain objects |

## Downstream Consumers

| Consumer | Relationship |
|----------|-------------|
| **Construction_Atlas** | Consumes construction domain ontology and truth boundaries |
| **Construction_Runtime** | Executes against truth boundaries defined in this kernel |
| **Construction_Reference_Intelligence** | Derives intelligence from construction-domain truths |
