# Construction Application OS

A workstation-grade construction management UI built with React, TypeScript, and Dockview. Construction OS provides a multi-panel cockpit environment where every panel stays synchronized through a centralized Truth Echo orchestration system.

## Stack Position

```
Universal_Truth_Kernel
  ↓
ValidKernel-Governance
  ↓
ValidKernel_Specs
  ↓
ValidKernel_Registry
  ↓
ValidKernel_Runtime
  ↓
Construction_Kernel
  ↓
Construction_Runtime
  ↓
Construction_Application_OS          ← YOU ARE HERE (Layer 7 — Application)
  ↓
Construction Applications
```

## Tech Stack

- **React 19** with TypeScript
- **Vite 8** for dev server and bundling
- **Dockview** for dockable, resizable, rearrangeable panel layout
- **Vitest** with React Testing Library for testing
- **Web Workers** for off-main-thread validation computation

## Features

### Multi-Panel Workspace (Dockview Cockpit)

Five purpose-built live panels arranged in a dockable, resizable workspace shell:

- **Explorer** — Project hierarchy tree with search, expand/collapse, and object/zone/document selection. Drives navigation across the entire cockpit.
- **Work** — Primary work surface with tabbed sub-views: Detail, Drawing, Validation, and Artifacts. Supports worker-backed validation and compare mode.
- **Reference** — Specs, code references, source documents, and citations for the active object. Compare-ready with source basis visibility.
- **Spatial** — Atlas/plan view showing zones and spatially-positioned objects. Click-to-select with zone boundaries and layer support.
- **System** — Validation summary, tasks, proposals, activity log, and system alerts. Real-time event stream monitor.

All panels are registered in a central **Panel Registry** that declares each panel's event subscriptions, emissions, Truth Echo participation, and owned state.

### Truth Echo Orchestration

The signature feature of the architecture. When any panel selects an object, Truth Echo propagates that selection to every other subscribed panel so the entire cockpit reorients around the same object simultaneously.

- Centralized orchestration — no direct panel-to-panel calls
- Fail-closed semantics — ambiguous or missing objects are rejected, not silently swallowed
- Visual feedback — panels flash on echo receipt; source panel shows an active indicator dot
- Echo failure alerts surface in the System panel

### Typed Event Bus

All inter-panel communication flows through a singleton, typed event bus. 14 event types including:

- `object.selected` / `zone.selected` — navigation events
- `reference.requested` / `compare.requested` — cross-panel data requests
- `validation.requested` / `validation.updated` — validation lifecycle
- `artifact.requested` — drawing/report/export generation
- `proposal.created` / `task.created` — workflow events
- `workspace.mode.changed` — mode switching (default, compare, focus, review)
- `truth-echo.propagated` / `truth-echo.failed` — orchestration events
- `panel.follow.changed` / `companion.pinned` — layout events

Events use microtask-based dispatch to prevent synchronous cascade storms. Debug logging and a 200-entry event log are built in.

### Adapter Contract System

Six typed adapter interfaces define the seam between UI and data sources:

| Adapter | Purpose |
|---------|---------|
| **TruthSourceAdapter** | Project tree, object lookup, search |
| **ReferenceSourceAdapter** | Specs, code, citations, document references |
| **SpatialSourceAdapter** | Spatial objects, zones, spatial context |
| **ValidationAdapter** | Structural/domain/geometry/full validation |
| **ArtifactAdapter** | Drawing, report, and export generation |
| **VoiceAdapter** | Voice command recognition (seam ready) |

Every adapter declares `adapterName` and `isMock` so the UI always knows whether it's displaying real or mock data. All data flows through `SourcedData<T>` wrappers that carry source basis (`canonical`, `derived`, `draft`, `compare`, `mock`) and timestamps.

Mock adapters are included for all six interfaces, providing a complete working demo with a realistic project tree (zones, assemblies, elements, specifications, documents).

### Device-Responsive Layout

The Device Orchestrator detects five device classes and adapts the panel layout accordingly:

| Device Class | Viewport | Layout | Visible Panels |
|-------------|----------|--------|----------------|
| **Ultrawide** | 2560px+ | Full cockpit | All 5 panels |
| **Desktop** | 1440px+ | Full cockpit | Explorer, Work, Reference, System |
| **Laptop** | 1024px+ | Split | Explorer, Work, Reference |
| **Tablet** | 768px+ | Compact | Work + Explorer companion |
| **Phone** | < 768px | Single + switcher | One panel at a time with bottom nav |

Layout re-applies automatically on window resize. Phone mode includes a bottom companion switcher bar for quick panel access.

### Active Object Store

A singleton external store (compatible with `useSyncExternalStore`) that holds the canonical active object identity. Manages six state layers:

1. Canonical source adapter state
2. Panel-local derived state
3. Draft UI state
4. Compare state
5. Workspace/orchestration state (mode, device class, pinned companion)
6. Mailbox/task/proposal state

### Worker-Backed Validation

Validation computation runs off the main thread via a Web Worker. The worker interface accepts object IDs and validation types, performs computation, and returns typed results with compute-time metrics. The `useValidationWorker` hook provides a clean React interface with loading state.

### Design Token System

A comprehensive token system powers a dark, structured, workstation-grade aesthetic:

- Depth-layered background hierarchy (deep → base → surface → elevated → hover → active)
- Truth Echo visual language (active indicators, propagation traces, pulse highlights)
- Source basis color coding (canonical = green, derived = grey, draft = yellow, compare = purple, mock = orange)
- Semantic colors for validation states (success, warning, error, info)
- Inter + JetBrains Mono typography

### Panel Shell Chrome

Every panel gets consistent chrome via `PanelShell`:

- Panel title with Truth Echo source indicator
- Mock/real data badge and source basis indicator
- Active object bar showing what the panel is oriented around
- Echo failure warning banner
- Echo flash animation on truth propagation

## Quick Start

```bash
npm install
npm run dev        # Start dev server
npm run build      # Production build
npm run test       # Run tests
npm run test:watch # Watch mode
```

## Project Structure

```
src/
├── App.tsx                          # Application root
├── main.tsx                         # Entry point
└── ui/
    ├── contracts/
    │   ├── events.ts                # Typed event contracts (14 event types)
    │   └── adapters.ts              # Typed adapter interfaces (6 adapters)
    ├── events/
    │   └── EventBus.ts              # Singleton typed event bus
    ├── orchestration/
    │   ├── TruthEcho.ts             # Truth Echo orchestrator
    │   └── DeviceOrchestrator.ts    # Device class detection & layout
    ├── stores/
    │   ├── activeObjectStore.ts     # Canonical active object state
    │   └── useSyncExternalStore.ts  # React store hook
    ├── adapters/
    │   ├── index.ts                 # Adapter registry
    │   ├── mockTruthSource.ts       # Mock project tree
    │   ├── mockReferenceSource.ts   # Mock references
    │   ├── mockSpatialSource.ts     # Mock spatial data
    │   ├── mockValidation.ts        # Mock validation
    │   ├── mockArtifact.ts          # Mock artifacts
    │   └── mockVoice.ts             # Mock voice commands
    ├── panels/
    │   ├── PanelShell.tsx           # Common panel chrome
    │   ├── explorer/                # Explorer panel
    │   ├── work/                    # Work panel
    │   ├── reference/               # Reference panel
    │   ├── spatial/                 # Spatial panel
    │   └── system/                  # System panel
    ├── registry/
    │   └── PanelRegistry.ts         # Panel definitions & metadata
    ├── theme/
    │   ├── tokens.ts                # Design tokens
    │   └── GlobalStyles.tsx         # Global CSS reset
    ├── workers/
    │   ├── validation.worker.ts     # Web Worker for validation
    │   └── useValidationWorker.ts   # React hook for worker
    └── workspace/
        └── WorkspaceShell.tsx       # Dockview workspace root
```

## Architecture Principles

- **No direct panel-to-panel calls** — all communication flows through the event bus
- **Fail closed** — ambiguous or missing state is rejected, never silently consumed
- **Source basis visibility** — every piece of data is labeled canonical, derived, draft, compare, or mock
- **Adapter seams** — UI never invents source truth; all data flows through typed adapters
- **Panels are live systems, not pages** — no page-based routing; the workspace is the operating surface
