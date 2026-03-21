# Change Log and Rationale — UI Kernel Foundation Wave

## Build Boundary Rules

- Only files required for safe insertion, workspace shell, panels, docs, theme, contracts, and supporting tests were touched.
- No existing documentation or specification files were modified.
- No broad refactors performed.

## Files Changed

### Root Config (new)
| File | Rationale |
|------|-----------|
| `package.json` | Added build scripts, dependencies for React/Vite/Dockview/TypeScript |
| `tsconfig.json` | TypeScript configuration with strict mode |
| `vite.config.ts` | Vite build configuration with React plugin and worker support |
| `vitest.config.ts` | Test runner configuration |
| `index.html` | Vite HTML entrypoint |

### Source — Contracts (`src/ui/contracts/`)
| File | Rationale |
|------|-----------|
| `events.ts` | Typed event contracts — all 14 required event types with payloads |
| `adapters.ts` | Typed adapter contracts — 6 adapter interfaces (truth, reference, spatial, validation, artifact, voice) |

### Source — Event Bus (`src/ui/events/`)
| File | Rationale |
|------|-----------|
| `EventBus.ts` | Central event bus — microtask-based, fail-safe, with debug logging |
| `EventBus.test.ts` | Event bus unit tests |

### Source — Stores (`src/ui/stores/`)
| File | Rationale |
|------|-----------|
| `activeObjectStore.ts` | Active object state — canonical identity, fail-closed semantics |
| `useSyncExternalStore.ts` | React hook for store subscription |
| `activeObjectStore.test.ts` | Store unit tests |

### Source — Adapters (`src/ui/adapters/`)
| File | Rationale |
|------|-----------|
| `mockTruthSource.ts` | Mock truth source with realistic construction project data |
| `mockReferenceSource.ts` | Mock reference/spec data |
| `mockSpatialSource.ts` | Mock spatial/plan/zone data |
| `mockValidation.ts` | Mock validation results |
| `mockArtifact.ts` | Mock artifact generation seam |
| `mockVoice.ts` | Mock voice adapter seam |
| `index.ts` | Adapter registry assembly |

### Source — Orchestration (`src/ui/orchestration/`)
| File | Rationale |
|------|-----------|
| `TruthEcho.ts` | Truth Echo orchestrator — governs context synchronization |
| `TruthEcho.test.ts` | Truth Echo unit tests (7 tests including fail-closed) |
| `DeviceOrchestrator.ts` | Device class detection and layout rules for 5 device classes |
| `DeviceOrchestrator.test.ts` | Device orchestrator unit tests |

### Source — Panels (`src/ui/panels/`)
| File | Rationale |
|------|-----------|
| `PanelShell.tsx` | Common panel wrapper with Truth Echo visual feedback |
| `explorer/ExplorerPanel.tsx` | Explorer panel — tree view, search, selection |
| `work/WorkPanel.tsx` | Work panel — detail, validation, drawing, artifact tabs |
| `reference/ReferencePanel.tsx` | Reference panel — specs, citations, compare view |
| `spatial/SpatialPanel.tsx` | Spatial panel — SVG plan view, zone selection |
| `system/SystemPanel.tsx` | System panel — validation, tasks, proposals, activity log |

### Source — Workspace (`src/ui/workspace/`)
| File | Rationale |
|------|-----------|
| `WorkspaceShell.tsx` | Dockview workspace shell with preset system and phone companion |

### Source — Registry (`src/ui/registry/`)
| File | Rationale |
|------|-----------|
| `PanelRegistry.ts` | Panel definitions with state ownership and event subscriptions |

### Source — Workers (`src/ui/workers/`)
| File | Rationale |
|------|-----------|
| `validation.worker.ts` | Web Worker for off-main-thread validation computation |
| `useValidationWorker.ts` | React hook for worker-backed validation |

### Source — Theme (`src/ui/theme/`)
| File | Rationale |
|------|-----------|
| `tokens.ts` | Design token system — colors, typography, spacing, Truth Echo tokens |
| `GlobalStyles.tsx` | Global CSS styles + Dockview overrides + scrollbar + echo animation |

### Source — App (`src/`)
| File | Rationale |
|------|-----------|
| `main.tsx` | React mount point |
| `App.tsx` | Application root |
| `vite-env.d.ts` | Vite type declarations |
| `test/setup.ts` | Test setup (jest-dom matchers) |

### Documentation (`docs/ui/`)
All documentation artifacts listed in this wave.

## Dependencies Added

| Dependency | Version | Why |
|-----------|---------|-----|
| react | ^19.2.4 | UI framework — industry standard, component model |
| react-dom | ^19.2.4 | DOM rendering for React |
| dockview | ^5.1.0 | Panel docking system — per spec requirement |
| dockview-react | ^5.1.0 | React integration for Dockview |
| typescript | ^5.9.3 | Type safety for all contracts and code |
| vite | ^8.0.1 | Fast build tool with worker support |
| @vitejs/plugin-react | ^6.0.1 | React JSX transform for Vite |
| vitest | ^4.1.0 | Test runner compatible with Vite |
| @testing-library/react | ^16.3.2 | React component testing |
| @testing-library/jest-dom | ^6.9.1 | DOM assertion matchers |
| jsdom | ^29.0.1 | DOM emulation for test environment |
| @types/react | ^19.2.14 | React type definitions |
| @types/react-dom | ^19.2.3 | React DOM type definitions |
