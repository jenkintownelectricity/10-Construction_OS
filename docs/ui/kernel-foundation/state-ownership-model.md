# State Ownership Model — Construction OS

## Six State Layers

| Layer | Owner | Description | Example |
|-------|-------|-------------|---------|
| 1. Canonical Source | Adapters | Data from truth source (via Construction_Runtime/Kernel) | Project tree, object definitions |
| 2. Panel-Local Derived | Each Panel | Data derived by panels from canonical + interactions | Expanded tree nodes, active tab |
| 3. Draft UI State | Each Panel | User edits not yet committed upstream | Form inputs, unsaved changes |
| 4. Compare State | activeObjectStore | When comparing two objects | compareObject identity |
| 5. Workspace/Orchestration | activeObjectStore | Layout, mode, device class, pinned companion | workspaceMode, deviceClass |
| 6. Mailbox/Task/Proposal | System Panel | System-level operational state | Tasks, proposals, alerts |

## State Boundaries

### activeObjectStore owns:
- `activeObject: ActiveObjectIdentity | null` (layer 1 identity)
- `basis: SourceBasis`
- `sourcePanel: PanelId | null`
- `compareObject: ActiveObjectIdentity | null` (layer 4)
- `workspaceMode: WorkspaceMode` (layer 5)
- `deviceClass: DeviceClass` (layer 5)
- `pinnedCompanion: PanelId | null` (layer 5)
- `followingPanels: Set<PanelId>` (layer 5)
- `lastEchoTimestamp: number`
- `echoFailure: string | null`

### Each Panel owns (layer 2 + 3):
- Its own selected/expanded state
- Its own tab/view state
- Its own draft state
- Its own filter/search state

### Adapters own (layer 1 content):
- Canonical project data
- Reference content
- Spatial coordinates
- Validation results

### System Panel owns (layer 6):
- Tasks list
- Proposals list
- Alerts list
- Activity log

## Rules

1. Active object identity must remain stable across panel moves and layout changes.
2. Draft state must not be visually confused with canonical or validated state.
3. Compare state must be explicit (visible in panel chrome when active).
4. Missing source basis must fail closed or display "unresolved basis" clearly.
5. Pinned companion state must survive phone/tablet mode switching.
6. Truth Echo must always resolve around one active object identity or fail closed.
