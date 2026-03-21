# Coexistence Strategy — UI Kernel Foundation

## Chosen Strategy

**New governed workspace entrypoint** — because no prior frontend implementation existed.

## Rationale

The Construction_Application_OS repository was documentation-only at v0.1. No frontend code, build system, or runtime dependencies existed. The insertion strategy is therefore a clean additive bootstrap rather than an extension or replacement.

## Touched Routes / Entrypoints

| Path | Action | Purpose |
|------|--------|---------|
| `index.html` | **Created** | Vite HTML entrypoint |
| `src/main.tsx` | **Created** | React mount point |
| `src/App.tsx` | **Created** | Application root — renders WorkspaceShell |

## Touched Shell Boundaries

| Boundary | Status |
|----------|--------|
| Existing `ui/` markdown specs | **Untouched** — preserved as conceptual specs |
| Existing `os/` definitions | **Untouched** |
| Existing `apps/` specs | **Untouched** |
| Existing `maps/` mappings | **Untouched** |
| Existing `workflows/` | **Untouched** |
| Existing `state/` | **Untouched** |
| Existing `docs/system/` | **Untouched** |

## New Boundaries

| Boundary | Scope |
|----------|-------|
| `src/ui/` | All UI implementation code |
| `src/ui/workspace/` | Workspace shell (Dockview integration) |
| `src/ui/panels/` | Five panel system implementations |
| `src/ui/events/` | Central event bus |
| `src/ui/adapters/` | Adapter registry and mock implementations |
| `src/ui/stores/` | State management (active object store) |
| `src/ui/orchestration/` | Truth Echo, device orchestration |
| `src/ui/contracts/` | Typed event and adapter contracts |
| `src/ui/registry/` | Panel registry |
| `src/ui/workers/` | Web Worker implementations |
| `src/ui/theme/` | Design tokens and global styles |
| `docs/ui/` | All documentation artifacts for this wave |

## Coexistence Guarantees

1. No existing files in `os/`, `apps/`, `workflows/`, `maps/`, `state/`, `ui/`, or `docs/system/` were modified
2. `README.md` was not modified
3. `package.json` was modified only to add build tooling (was auto-generated with `npm init`)
4. All new code lives under `src/` — a new directory
5. All new docs live under `docs/ui/` — a new subdirectory
6. The `ui/` directory (existing conceptual specs) is not conflated with `src/ui/` (new implementation)
