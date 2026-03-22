# Construction OS — Gravity Glass Workspace Implementation Notes

**Document ID**: L0-CMD-CONOS-VKGL04R-GRAVITYGLASS-002-IMPL
**Date**: 2026-03-22
**Authority**: Armand Lefebvre

## Touched Files

### New Files

| File | Purpose |
|------|---------|
| `src/ui/gravity/ProximityConstants.ts` | Configurable proximity field parameters, edge types, state interfaces |
| `src/ui/gravity/ProximityField.ts` | Deterministic proximity field engine with trigger/ramp/safe-zone logic |
| `src/ui/gravity/WorkspaceBias.tsx` | Workspace bias controls (+/- expand/shrink, ←/→ visual/doc bias) |
| `src/ui/gravity/GlassMorph.ts` | Glass morph CSS style objects for secondary panels |
| `src/ui/gravity/EdgePanel.tsx` | Reactive edge panel component with proximity-driven width transitions |
| `src/ui/gravity/GravityDeckFan.tsx` | Left contextual deck fan-out with card stack navigation |
| `src/ui/gravity/HoverPeek.tsx` | Hover peek preview with temporary/locked states |

### Modified Files

| File | Changes |
|------|---------|
| `src/ui/workspace/WorkspaceShell.tsx` | Full gravity workspace layout: proximity field integration, edge panels, deck fan-out, bias controls in header, proximity-reactive bottom dock |
| `src/ui/layout/BottomDock.tsx` | Thinner idle state (28px), proximity expansion, glass morph styling, auto-collapse behavior |
| `src/ui/panels/work/WorkPanel.tsx` | Added Spatial tab to workspace mode buttons |
| `src/ui/stores/activeObjectStore.ts` | Added workspaceBias, tileCount, peekTarget, peekLocked state |
| `src/ui/theme/GlobalStyles.tsx` | Added motion doctrine CSS, glass morph utility classes, edge strip transitions |

## Proximity Field Constants

All constants stored in `src/ui/gravity/ProximityConstants.ts`:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `triggerBand` | 80px | Distance from edge where sensing begins |
| `rampBand` | 40px | Distance where expansion ramps to full |
| `centerSafeZone` | 200px | Center region where no edge reaction occurs |
| `intentDelay` | 180ms | Hover time before expansion begins |
| `expandDuration` | 180ms | Animation duration for expansion |
| `collapseDuration` | 200ms | Animation duration for collapse |
| `edgeIdleWidth` | 4px | Idle strip width for edge panels |
| `edgePreviewWidth` | 320px | Preview width for expanded edge panels |
| `edgeLockedWidth` | 380px | Width for locked edge panels |
| `dockIdleHeight` | 28px | Idle height for bottom dock |
| `dockPreviewHeight` | 260px | Expanded height for bottom dock |
| `dockExpandedHeight` | 380px | Full expanded height for dock |
| `biasStep` | 8% | Workspace share change per bias click |
| `workspaceMinShare` | 40% | Minimum workspace share |
| `workspaceMaxShare` | 90% | Maximum workspace share |
| `workspaceDefaultShare` | 65% | Default workspace share |
| `peekDelay` | 200ms | Delay before hover peek shows |
| `fanIdleWidth` | 6px | Idle width for deck fan strip |
| `fanExpandedWidth` | 280px | Expanded width for deck fan |
| `easing` | `cubic-bezier(0.16, 1, 0.3, 1)` | Motion easing function |

## Edge Behavior

### Left Edge — Documents / References
- Idle: 4px transparent strip with subtle proximity indicator
- Sensing: Strip brightens with cursor proximity
- Expanding: Panel width ramps from 4px toward 320px
- Preview: Full 320px reference panel with glass morph styling
- Locked: 380px, ignores proximity collapse, unlock button visible
- Content: ReferencePanel component

### Right Edge — Drawings / Spatial / Visual
- Same state progression as left edge
- Content: SpatialPanel component
- Visual preview of spatial context and zone navigation

### Top Edge — Quick-Switch Workspace Bar
- Proximity tracked but currently served by existing status bar
- Status bar remains fixed at top with Authority HUD + bias controls

### Bottom Edge — System Dock
- Idle: 28px thin tab strip
- Proximity causes gentle height increase (up to +16px)
- Active state: Full dock expansion (260px preview, 380px expanded)
- Pinned state: Dock stays open regardless of cursor position
- Auto-collapses on cursor exit unless pinned or user-opened

## Proximity Field Model

### State Machine (per edge)
```
idle → sensing → expanding → preview → locked
                 ↑                        ↓
                 └── (unlock) ────────────┘
```

### Arbitration
- Only one edge may dominate at a time
- Strongest proximity value wins
- Locked edges persist regardless of proximity
- Center safe zone (200px from all edges) prevents any edge reaction

### FAIL_CLOSED Behavior
- Invalid mouse coordinates: no update, idle state persists
- Invalid viewport dimensions: no update
- Engine stopped: all edges return to idle
- Missing proximity snapshot: idle defaults used

## Workspace Tile Logic

| Tiles | Layout |
|-------|--------|
| 1 | Full workspace |
| 2 | 50/50 split |
| 3-4 | Grid layout |
| 5+ | Compressed grid |

Bias shifts compress or collapse tiles based on available space.

## Glass Morph Styling

Applied to secondary panels only (edge panels, dock):
- `background: rgba(22,26,34,0.65)`
- `backdrop-filter: blur(12px)`
- `border: 1px solid rgba(255,255,255,0.06)`

Workspace controls remain crisp, not glassy.

## Motion Doctrine

| Allowed | Forbidden |
|---------|-----------|
| slide | spin |
| fan-out | bounce |
| scale | decorative motion |
| rise | jitter |

Timing: 150-220ms with `cubic-bezier(0.16, 1, 0.3, 1)` easing.

## Gravity Deck Fan-Out

- Thin idle strip on left edge (6px)
- Mouse proximity fans cards outward from left
- Vertical scroll through card stack
- Cards show: type icon, object name, type label
- Click card → sets gravity object in workspace via Truth Echo
- Glass morph card styling

## Scope Verification

- [x] Only `Construction_Application_OS` repository modified
- [x] No kernel, atlas, runtime, bus, cache, or assistant modifications
- [x] No authority escalation
- [x] No proposal auto-approval
- [x] No direct execution through hover, dock, or proximity behavior
- [x] Invalid/missing proximity state fails closed to idle layout
- [x] No forbidden animations (spin, bounce, decorative)
- [x] Motion timing limited to 150-220ms range
- [x] Workspace always remains primary panel
