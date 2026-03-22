# REPO_MANIFEST

## Identity

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Repository         | Construction_OS_Registry                   |
| Owner              | jenkintownelectricity                      |
| Layer              | Infrastructure Layer                       |
| Primary Role       | Topology Authority                         |

## Purpose

Construction OS topology and repository governance authority. This repository is the single authoritative source for the structural map of all Construction OS repositories, their classifications, and the dependency relationships between them.

## Classification

- **Type:** Infrastructure service
- **Authority scope:** Topology authority — not doctrine authority
- **Defers to kernels for truth.** This repository does not originate, store, or adjudicate doctrine. Truth belongs to kernels; the registry reflects structure only.

## What It IS

- Topology authority for Construction OS
- Repository governance authority
- Validator of topology and dependency declarations
- Store of topology maps — the canonical record of what exists, where it sits, and what it depends on

## What It IS NOT

- **NOT a kernel.** It holds no doctrine and makes no truth claims.
- **NOT truth authority for doctrine.** Doctrine originates in and is governed by kernels.
- **NOT a cognitive bus.** It does not route messages, events, or signals between components.
- **NOT an awareness cache.** It does not store or propagate cognitive-layer awareness state.
- **NOT a runtime executor.** It does not run workloads, schedule tasks, or manage process lifecycles.

## Interactions

The registry registers all six other cognitive-layer components:

1. CRI (Cognitive Runtime Interface)
2. VKBUS
3. Cognitive Bus
4. Assistant
5. Workers
6. Awareness Cache

Registration establishes that a component exists within the topology and declares its dependencies. The registry **does not govern the internal behavior** of any registered component. Each component retains full authority over its own internals; the registry is concerned only with structural placement and inter-component relationships.

## Governance

- **Authoritative for topology.** All topology questions — what repos exist, how they are classified, what depends on what — resolve here.
- **Must not drift into doctrine ownership.** The boundary between topology authority and doctrine authority is load-bearing. If this repository begins to originate or adjudicate doctrine, it has exceeded its mandate. Topology authority only; truth belongs to kernels.

## Related Artifacts

This repository also hosts the **Cognitive Layer Boundary Matrix** at:

```
docs/architecture/cognitive-layer-boundary-matrix.md
```

The boundary matrix defines the structural boundaries between cognitive-layer components and is maintained here because boundary definitions are a topology concern.
