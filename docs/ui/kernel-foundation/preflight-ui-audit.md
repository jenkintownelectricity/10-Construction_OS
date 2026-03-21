# Pre-Flight UI Audit — Construction_Application_OS

## Detected Stack

| Aspect | Detection |
|--------|-----------|
| Frontend Framework | **None (v0.1 was documentation-only)** — React 19 + TypeScript bootstrapped in this wave |
| Routing Model | **None** — single workspace surface mounted at root |
| Package Manager | npm (v10.9.4) |
| Styling System | **None pre-existing** — CSS-in-JS (inline styles + design tokens) introduced |
| TypeScript Status | **New** — TypeScript 5.9 introduced with strict mode |
| Build Tool | **Vite 8** — introduced in this wave |
| App Entrypoints | `index.html` → `src/main.tsx` → `src/App.tsx` → `WorkspaceShell` |
| Node.js Version | 22.22.0 |

## Detected Entrypoints

- **Previous**: No code entrypoints. Documentation repo only.
- **New**: `index.html` (Vite entrypoint) → `src/main.tsx` → `src/App.tsx`

## Detected Styling Approach

- **Previous**: None
- **New**: Design token system (`src/ui/theme/tokens.ts`) with CSS custom properties, inline styles for panels, Dockview CSS overrides for workspace chrome

## Detected Routing Approach

- **Previous**: None (no frontend existed)
- **New**: No router. Single full-viewport workspace surface. Panels are live systems, not routes.

## Existing Shell / Dashboard / Workspace

- **None detected.** The `ui/` directory contained only conceptual markdown specs (`app_shell_spec.md`, `navigation_spec.md`, `status_surface_spec.md`). No implementation.

## Existing Design Token System

- **None detected.** Introduced fresh in `src/ui/theme/tokens.ts`.

## Existing State Management

- **None detected.** Introduced fresh with a minimal external-store pattern (`activeObjectStore`).

## Monorepo Boundaries

- **Not a monorepo.** Single repository with flat structure.

## Insertion Strategy

Since no prior frontend existed, insertion is clean:
1. Added `package.json` scripts, dependencies, and dev dependencies
2. Created `src/` directory for all UI code
3. Created `index.html` at root for Vite
4. Added `tsconfig.json`, `vite.config.ts`, `vitest.config.ts`
5. Existing documentation directories (`os/`, `apps/`, `workflows/`, `maps/`, `docs/`, `ui/`, `state/`) remain untouched

## Coexistence Strategy

No coexistence conflict exists — this repo had no prior runnable code. All existing markdown documentation, specs, and system files are preserved as-is.

## Dependency Impact

| Dependency | Purpose | Type |
|-----------|---------|------|
| react 19 | UI framework | Runtime |
| react-dom 19 | DOM rendering | Runtime |
| dockview 5 | Panel docking system | Runtime |
| dockview-react 5 | React bindings for Dockview | Runtime |
| typescript 5.9 | Type safety | Dev |
| vite 8 | Build tool | Dev |
| @vitejs/plugin-react | React support for Vite | Dev |
| vitest 4 | Test runner | Dev |
| @testing-library/react | React testing utilities | Dev |
| @testing-library/jest-dom | DOM assertion matchers | Dev |
| jsdom | DOM emulation for tests | Dev |

## Risk Notes

1. **No production data integration** — all adapters are mocks
2. **Dockview is the only significant runtime dependency** — if incompatible with future requirements, it can be replaced via the workspace shell boundary
3. **No routing library** — if multi-surface navigation is needed later, a router can be added without restructuring the workspace
4. **Worker support** depends on browser compatibility (all modern browsers support ES module workers)

## Exact Scope Boundary for This Wave

### In Scope
- Workspace shell (Dockview-based)
- Five live panel systems (Explorer, Work, Reference, Spatial, System)
- Central typed event bus
- Typed adapter contracts with mock implementations
- Active object store with Truth Echo core
- Device orchestration scaffold (5 device classes)
- Worker-backed validation seam
- Design token system and premium visual treatment
- HERO_COCKPIT_DEFAULT preset
- Kernel and triad documentation
- All required documentation artifacts

### Out of Scope
- Real data integration with Construction_Runtime
- Production truth source adapters
- Real validation engine
- Real spatial/atlas rendering
- Voice system implementation
- Artifact generation engine
- User authentication / role enforcement
- Routing between multiple surfaces
