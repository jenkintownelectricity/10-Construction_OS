# Workspace Shell — Construction OS

## Architecture

The workspace shell uses **Dockview** (v5) as the panel docking framework. Dockview provides:
- Panel docking, movement, and resize
- Tab-based panel switching
- Serializable layout state
- No page reload required for panel switching

## Shell Components

| Component | File | Purpose |
|-----------|------|---------|
| WorkspaceShell | `src/ui/workspace/WorkspaceShell.tsx` | Main workspace container with Dockview |
| Panel Component Map | (in WorkspaceShell) | Maps panel IDs to React components |
| CompanionSwitcher | (in WorkspaceShell) | Phone-class panel switching bar |
| Status Bar | (in WorkspaceShell) | Workspace identity, mock indicator, device class |

## Panel Registry

Defined in `src/ui/registry/PanelRegistry.ts`. Each panel declares:
- Unique `id` matching a `PanelId` type
- Event subscriptions and emissions
- Truth Echo participation
- Owned state boundaries
- Default size weight

## Default Workspace Preset: HERO_COCKPIT_DEFAULT

### Desktop/Ultrawide Layout
```
┌──────────┬──────────────────┬───────────┐
│          │                  │           │
│ EXPLORER │      WORK        │ REFERENCE │
│          │  (center-of-     │           │
│          │   gravity)       │           │
├──────────┴──────┬───────────┴───────────┤
│                 │                       │
│    SPATIAL      │       SYSTEM          │
│                 │                       │
└─────────────────┴───────────────────────┘
```

### Laptop Layout
```
┌──────────┬──────────────────┬───────────┐
│ EXPLORER │      WORK        │ REFERENCE │
└──────────┴──────────────────┴───────────┘
```

### Tablet Layout
```
┌──────────┬──────────────────┐
│ EXPLORER │      WORK        │
└──────────┴──────────────────┘
```

### Phone Layout
```
┌──────────────────┐
│      WORK        │
│                  │
├──────────────────┤
│ EXP│WRK│REF│SPA│SYS│  ← companion switcher
└──────────────────┘
```

## Panel Capabilities

- **Docking**: Panels can be moved to any position
- **Resizing**: Panels can be resized by dragging borders
- **Stable context**: Active object survives panel movement
- **No page reload**: All panel switching is in-memory
- **Preset system**: Named presets define default layouts per device class
