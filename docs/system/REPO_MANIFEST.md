# REPO_MANIFEST — Construction_Kernel

## Identity

- **Repo Name:** Construction_Kernel
- **Purpose:** Applied construction-domain kernel downstream of Universal_Truth_Kernel. Defines construction-domain truth boundaries through seven supporting kernels.
- **Stack Layer:** Layer 5 — Domain Kernel
- **Baseline Version:** v0.1
- **Manifest Version:** v0.1

## Ownership

### Owns

- Construction kernel v0.1 architecture
- Seven domain kernels: Governance, Geometry, Chemistry, Assembly, Reality, Deliverable, Intelligence
- Kernel relationship map
- App dependency map
- Construction-domain truth boundaries

### Does Not Own

- Universal truth origination (Universal_Truth_Kernel)
- Generic governance doctrine (ValidKernel-Governance)
- Contract shapes (ValidKernel_Specs)
- System topology (ValidKernel_Registry)
- Generic runtime execution (ValidKernel_Runtime)
- Construction runtime execution (Construction_Runtime)
- Application UX (Construction_Application_OS)

## Stack Position

### Upstream

- **Universal_Truth_Kernel** — Conceptual. Operates within the truth boundary defined by the nucleus.
- **ValidKernel-Governance** — Follows governance rules.
- **ValidKernel_Registry** — Registered in topology.

### Downstream

- **Construction_Runtime** — Executes against kernel-defined truth.
- **Construction_Application_OS** — Apps aligned to kernel domains.

## Directory Structure

| Directory | Contents |
|-----------|----------|
| `kernel/` | Master kernel definition (CONSTRUCTION_KERNEL_V0.1.md) |
| `kernels/` | Seven domain kernels (Governance, Geometry, Chemistry, Assembly, Reality, Deliverable, Intelligence) |
| `maps/` | Kernel relationship map, app dependency map |
| `apps/` | Application specs (spec_intelligence_app, assembly_parser_app) |

## Reading Order

### First-Read

1. `README.md`
2. `kernel/CONSTRUCTION_KERNEL_V0.1.md`
3. `docs/system/REPO_MANIFEST.md`

### Future Agent Reading Order

1. `Universal_Truth_Kernel` → `nucleus/NUCLEUS_DOCTRINE.md`
2. `ValidKernel_Registry` → topology surfaces
3. This repo → `docs/system/REPO_MANIFEST.md`
4. This repo → `docs/system/AUTHORITATIVE_PATHS.md`
5. This repo → `docs/system/DEPENDENCY_MAP.md`
6. This repo → `docs/system/FROZEN_SEAMS.md`
7. `kernel/CONSTRUCTION_KERNEL_V0.1.md`
8. Only then targeted kernel files

## Mutability

### Frozen

- Seven kernel identity/ownership boundaries
- Kernel relationship flow: Governance + Geometry + Chemistry → Assembly, Assembly + Reality → Deliverables, All → Intelligence
- "System is bounded by truth" inheritance from nucleus

### Mutable

- Kernel internal content
- App specs
- Maps

## Relationship to Universal_Truth_Kernel

Direct upstream conceptual dependency. This kernel operates within the truth boundary defined by Universal_Truth_Kernel. Truth doctrine is defined in the nucleus and referenced here. May specialize and apply truth for the construction domain but may not contradict the nucleus.

## Execution Notes

No executable code. Contains construction domain ontology and truth boundary definitions.
