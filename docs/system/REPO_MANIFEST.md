# Repo Manifest — Construction_Application_OS

## Repo Name
Construction_Application_OS

## Purpose
Application coordination layer above Construction_Runtime and aligned to Construction_Kernel. Coordinates user-facing construction applications.

## Stack Layer
Layer 7 — Application

## Owns
- Application inventory and specifications
- Application workflows (assembly-to-shop-drawing, spec-to-opportunity)
- App-to-runtime capability mappings
- App-to-kernel domain mappings
- Role model (Project Manager, Estimator, Detailer, System)
- Conceptual UI specifications (app shell, navigation, status surfaces)
- OS-level coordination documentation

## Does Not Own
- Universal truth (Universal_Truth_Kernel)
- Governance doctrine (ValidKernel-Governance)
- Contract shapes (ValidKernel_Specs)
- System topology (ValidKernel_Registry)
- Generic runtime execution (ValidKernel_Runtime)
- Construction truth definitions (Construction_Kernel)
- Runtime execution implementation (Construction_Runtime)
- Runtime pipeline code, validators, geometry engine, writers

## Upstream Dependencies
- Universal_Truth_Kernel (conceptual — truth ultimately grounded in nucleus)
- Construction_Kernel (domain truth definitions consumed by apps)
- Construction_Runtime (runtime capabilities consumed by apps)
- ValidKernel-Governance (governance rules)

## Downstream Dependents
- User-facing construction applications (consumers of this coordination layer)

## Primary Directories
- `os/` — OS-level definitions (v0.1 spec, app inventory, workflow inventory, role model)
- `apps/` — Per-application specs (assembly_parser/, spec_intelligence/)
- `workflows/` — Workflow definitions
- `maps/` — Stack map, app-to-runtime map, app-to-kernel map
- `ui/` — Conceptual UI specs
- `docs/system/` — Hardening surfaces

## Canonical First-Read Files
1. `README.md`
2. `os/CONSTRUCTION_APPLICATION_OS_V0.1.md`
3. `docs/system/REPO_MANIFEST.md`
4. `docs/system/AUTHORITATIVE_PATHS.md`
5. `maps/stack_map.md`

## Frozen Directories / Frozen Surfaces
- `maps/stack_map.md` — Stack layer definitions
- App-to-runtime mapping structure (maps real v0.2 runtime components)
- App-to-kernel mapping structure (maps real kernel domains)
- Two-app inventory (Assembly Parser, Spec Intelligence) — no speculative additions

## Mutable Directories / Mutable Surfaces
- `apps/` — App spec content may evolve
- `workflows/` — Workflow details may evolve
- `ui/` — Conceptual specs may evolve toward implementation
- `os/` — OS definitions may evolve with new versions

## Relationship to Universal_Truth_Kernel
Upstream conceptual dependency (transitive via Construction_Kernel and Construction_Runtime). This layer consumes applied construction truth ultimately grounded in Universal_Truth_Kernel. It does not originate, redefine, or contradict truth at any layer.

## Future Agent Reading Order
1. `Universal_Truth_Kernel` → `nucleus/NUCLEUS_DOCTRINE.md`
2. `ValidKernel_Registry` → topology surfaces
3. This repo → `docs/system/REPO_MANIFEST.md`
4. This repo → `docs/system/AUTHORITATIVE_PATHS.md`
5. This repo → `docs/system/DEPENDENCY_MAP.md`
6. This repo → `docs/system/FROZEN_SEAMS.md`
7. `os/CONSTRUCTION_APPLICATION_OS_V0.1.md`
8. `maps/stack_map.md`
9. Only then targeted app specs or workflow files

## Execution Notes
- No executable code in this repo (v0.1 is documentation/specification only)
- UI specs are conceptual only — no implementation in this pass
- Two first-class applications only; do not add speculative apps
- App-to-runtime mappings must match actual Construction_Runtime v0.2 capability
- App-to-kernel mappings must match actual Construction_Kernel domain boundaries
