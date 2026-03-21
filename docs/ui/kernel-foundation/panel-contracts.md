# Panel Contracts — Construction OS

## Panel System Overview

Five live panel systems, each with declared state ownership, event subscriptions, and Truth Echo participation.

## Explorer Panel

| Aspect | Value |
|--------|-------|
| **ID** | `explorer` |
| **Title** | Explorer |
| **Purpose** | Project hierarchy, search, filter, object/document/zone selection |
| **Subscribes To** | `truth-echo.propagated`, `zone.selected`, `validation.updated` |
| **Emits** | `object.selected`, `zone.selected`, `reference.requested` |
| **Truth Echo** | Subscriber |
| **Owned State** | selectedNodeId, expandedNodes, searchQuery, filterState |
| **Adapter Dependencies** | TruthSourceAdapter (project tree, object lookup, search) |

## Work Panel

| Aspect | Value |
|--------|-------|
| **ID** | `work` |
| **Title** | Work |
| **Purpose** | Primary live work surface — detail, drawing, artifact workspace |
| **Subscribes To** | `truth-echo.propagated`, `object.selected`, `validation.updated`, `workspace.mode.changed` |
| **Emits** | `object.selected`, `validation.requested`, `artifact.requested`, `compare.requested` |
| **Truth Echo** | Subscriber |
| **Owned State** | activeTab, draftState, localCommands |
| **Adapter Dependencies** | ValidationAdapter, ArtifactAdapter |
| **Worker** | validation.worker.ts (off-main-thread validation) |

## Reference Panel

| Aspect | Value |
|--------|-------|
| **ID** | `reference` |
| **Title** | Reference |
| **Purpose** | Specs, code, source docs, citations — compare-ready |
| **Subscribes To** | `truth-echo.propagated`, `reference.requested`, `compare.requested` |
| **Emits** | `object.selected`, `compare.requested` |
| **Truth Echo** | Subscriber |
| **Owned State** | activeReferences, compareState, referenceFilter |
| **Adapter Dependencies** | ReferenceSourceAdapter |

## Spatial Panel

| Aspect | Value |
|--------|-------|
| **ID** | `spatial` |
| **Title** | Spatial |
| **Purpose** | Atlas/plan/zone/location shell — selected object spatial context |
| **Subscribes To** | `truth-echo.propagated`, `object.selected`, `zone.selected` |
| **Emits** | `object.selected`, `zone.selected` |
| **Truth Echo** | Subscriber |
| **Owned State** | viewportState, activeZoneId, selectedSpatialObject, layerVisibility |
| **Adapter Dependencies** | SpatialSourceAdapter |

## System Panel

| Aspect | Value |
|--------|-------|
| **ID** | `system` |
| **Title** | System |
| **Purpose** | Validation summary, alerts, mailbox/proposals, tasks, activity log |
| **Subscribes To** | `truth-echo.propagated`, `validation.updated`, `proposal.created`, `task.created`, `truth-echo.failed` |
| **Emits** | `validation.requested`, `task.created`, `proposal.created` |
| **Truth Echo** | Subscriber |
| **Owned State** | activeTab, validationSummary, tasks, proposals, alerts |

## Panel Rules

1. All panels communicate exclusively through the event bus — no direct calls.
2. Each panel declares its subscriptions and emissions in PanelRegistry.
3. Each panel manages its own local state; canonical state comes from adapters.
4. Every panel participates in Truth Echo.
5. Mock data is always labeled.
