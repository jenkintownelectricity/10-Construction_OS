# Authoritative Paths — Construction_Application_OS

## Cross-Repo Reading Order

Before reading this repo, read:
1. `Universal_Truth_Kernel` → `nucleus/NUCLEUS_DOCTRINE.md`
2. `ValidKernel_Registry` → topology surfaces

Then read this repo's surfaces:
3. `docs/system/REPO_MANIFEST.md`
4. `docs/system/AUTHORITATIVE_PATHS.md`
5. `docs/system/DEPENDENCY_MAP.md`
6. `docs/system/FROZEN_SEAMS.md`

Then repo-specific authoritative files:
7. `os/CONSTRUCTION_APPLICATION_OS_V0.1.md`
8. `maps/stack_map.md`
9. Only then targeted app specs or workflow files

## Authoritative Files

| File | Authority |
|------|-----------|
| `os/CONSTRUCTION_APPLICATION_OS_V0.1.md` | Defines OS identity, apps, workflows, roles |
| `os/app_inventory.md` | Canonical app list |
| `maps/app_to_runtime_map.md` | App-to-runtime capability mappings |
| `maps/app_to_kernel_map.md` | App-to-kernel domain mappings |
| `maps/stack_map.md` | Stack layer definitions |

## Supporting Files

| File | Role |
|------|------|
| `apps/*/README.md` | Per-app overviews |
| `apps/*/workflow.md` | Per-app workflow details |
| `apps/*/dependencies.md` | Per-app dependency lists |
| `workflows/*.md` | Cross-cutting workflow definitions |
| `os/role_model.md` | Role definitions |
| `os/workflow_inventory.md` | Workflow catalog |

## Paths to Skip Unless Explicitly Needed
- `ui/` — Conceptual only in v0.1; skip unless working on UI design

## Paths Reserved for Audit/Debug/Deep Work
- `apps/*/inputs.md` — Input contract details
- `apps/*/outputs.md` — Output contract details
