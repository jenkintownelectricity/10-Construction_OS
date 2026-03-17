# Dependency Map — Construction_Application_OS

## Stack Position
Layer 7 — Application

## Upstream Dependencies

| Dependency | Layer | Relationship |
|-----------|-------|-------------|
| Universal_Truth_Kernel | 0 — Nucleus | Conceptual (transitive) — truth ultimately grounded here |
| ValidKernel-Governance | 1 — Control Plane | Governance rules apply to this layer |
| Construction_Kernel | 5 — Domain Kernel | Defines domain truth consumed by apps |
| Construction_Runtime | 6 — Domain Runtime | Provides execution capabilities consumed by apps |

## Downstream Dependents

| Dependent | Relationship |
|-----------|-------------|
| User-facing construction applications | Consume app coordination and workflow definitions |

## Internal Dependency Zones

| Zone | Contents | Dependencies |
|------|----------|-------------|
| `os/` | OS-level definitions | None (self-contained) |
| `apps/` | Per-app specifications | Depends on runtime/kernel for mapping accuracy |
| `workflows/` | Workflow definitions | Depends on runtime pipeline stages |
| `maps/` | Stack, runtime, kernel maps | Depends on actual repo state for accuracy |
| `ui/` | Conceptual UI specs | Depends on role model and app inventory |
| `docs/system/` | Hardening surfaces | Depends on all zones for completeness |

## Relationship to Universal_Truth_Kernel
Transitive upstream conceptual dependency. This layer consumes applied construction truth from Construction_Kernel, executed through Construction_Runtime, ultimately grounded in Universal_Truth_Kernel. This layer does not access nucleus truth directly.
