# Event Contracts — Construction OS

## Event Bus Architecture

Central event bus with typed contracts. All panel-to-panel communication flows through the bus. Direct panel calls are forbidden.

## Event Catalog

| Event | Payload Type | Description |
|-------|-------------|-------------|
| `object.selected` | `ObjectSelectedPayload` | An object was selected in any panel |
| `zone.selected` | `ZoneSelectedPayload` | A zone was selected (typically from Explorer or Spatial) |
| `reference.requested` | `ReferenceRequestedPayload` | A panel requests reference data for an object |
| `compare.requested` | `CompareRequestedPayload` | A panel requests a comparison between two objects |
| `artifact.requested` | `ArtifactRequestedPayload` | A panel requests artifact generation |
| `validation.requested` | `ValidationRequestedPayload` | A panel requests validation of an object |
| `validation.updated` | `ValidationUpdatedPayload` | Validation results have been updated |
| `proposal.created` | `ProposalCreatedPayload` | A new proposal was created |
| `task.created` | `TaskCreatedPayload` | A new task was created |
| `workspace.mode.changed` | `WorkspaceModeChangedPayload` | Workspace mode changed (default/compare/focus/review) |
| `panel.follow.changed` | `PanelFollowChangedPayload` | A panel changed its Truth Echo follow status |
| `companion.pinned` | `CompanionPinnedPayload` | A companion panel was pinned (phone-class) |
| `truth-echo.propagated` | `TruthEchoPropagatedPayload` | Truth Echo successfully propagated |
| `truth-echo.failed` | `TruthEchoFailedPayload` | Truth Echo failed (ambiguous/missing object) |

## Event Rules

1. Events use lightweight payloads — prefer IDs + typed metadata over full objects.
2. Ambiguous or missing targets fail closed.
3. Events are delivered via microtask to prevent synchronous cascade storms.
4. Handler errors are caught and logged — they do not break the bus.
5. Events are logged for debugging (max 200 entries).

## Code Location

Machine-readable typed contracts: `src/ui/contracts/events.ts`
