# Cockpit Readability Fix — Implementation Note

**Document ID:** L0-DOC-CONOS-VKGL04R-UIREAD-001
**Date:** 2026-03-22
**Scope:** Typography, spacing, and layout readability improvements

## Summary

All cockpit panel text has been rescaled from microscopic (11-12px) to readable
(13.6-16.8px) sizes. Row spacing increased. Workspace layout adjusted to prevent
lower panel compression. Density modes added.

## Root Font Scale

```
html { font-size: 16px; }
```

## Typography Token Changes (tokens.ts)

| Token | Old Value | New Value | Purpose |
|-------|-----------|-----------|---------|
| sizeXs | 0.6875rem (11px) | 0.85rem (~13.6px) | Rows, status, meta, badges |
| sizeSm | 0.75rem (12px) | 0.95rem (~15.2px) | Panel body, content, lists |
| sizeBase | 0.8125rem (13px) | 1rem (16px) | Base readable size |
| sizeMd | 0.875rem (14px) | 1.05rem (~16.8px) | Panel titles, headings |
| sizeLg | 1rem (16px) | 1.25rem (20px) | Section headings |
| sizeXl | 1.25rem (20px) | 1.5rem (24px) | Page headings |

New tokens added:
- `font.lineNormal: '1.4'` — line-height for content/lists/diagnostics
- `font.lineTight: '1.25'` — line-height for headings/titles
- `space.rowY: '8px'` — vertical row padding
- `space.rowX: '12px'` — horizontal row padding

## Density Modes

- `body.readable` — font-size: 1.1rem (default on desktop)
- `body.compact` — font-size: 0.95rem (available for dense layouts)

Set in App.tsx on mount:
```typescript
document.body.classList.add('readable');
```

## CSS Custom Properties (GlobalStyles.tsx)

```css
:root {
  --font-xs: 0.85rem;
  --font-sm: 0.95rem;
  --font-md: 1.05rem;
  --font-lg: 1.25rem;
  --line-tight: 1.25;
  --line-normal: 1.4;
  --space-row-y: 8px;
  --space-row-x: 12px;
}
```

## Workspace Layout

- Status bar minHeight increased from 28px to 40px
- Dockview container uses `minHeight: 0` to allow flex shrink
- CSS classes `.workspace-shell`, `.workspace-bottom` added for grid layout fallback
- Lower panels no longer compressed by center work area

## Files Changed

| File | Changes |
|------|---------|
| `src/ui/theme/tokens.ts` | Typography scale, line-height tokens, row spacing tokens |
| `src/ui/theme/GlobalStyles.tsx` | CSS custom properties, density modes, cockpit typography classes, workspace layout rules |
| `src/App.tsx` | Readable density mode on mount |
| `src/ui/panels/PanelShell.tsx` | Increased header minHeight (32→40px), title uses sizeMd, improved line-heights |
| `src/ui/panels/awareness/AwarenessPanel.tsx` | lineHeight added to rows, tab padding increased |
| `src/ui/panels/proposals/ProposalMailbox.tsx` | lineHeight added to cards, tab padding increased |
| `src/ui/panels/diagnostics/RuntimeDiagnosticsPanel.tsx` | lineHeight on pipeline/event rows, tab padding |
| `src/ui/panels/assistant/AssistantConsole.tsx` | lineHeight on response cards |
| `src/ui/panels/system/SystemPanel.tsx` | lineHeight on all tabs, row padding increased |
| `src/ui/panels/explorer/ExplorerPanel.tsx` | Hardcoded 8px/10px → tokens.font.sizeXs |
| `src/ui/panels/work/WorkPanel.tsx` | lineHeight on content rows |
| `src/ui/panels/reference/ReferencePanel.tsx` | lineHeight on reference items |
| `src/ui/panels/spatial/SpatialPanel.tsx` | lineHeight on spatial items |
| `src/ui/decks/DeckPicker.tsx` | Hardcoded 8px/9px/10px → tokens.font.sizeXs |
| `src/ui/workspace/WorkspaceShell.tsx` | Status bar height, minHeight: 0, title font size |

## Remaining Exceptions

None. All cockpit panel font sizes now use tokenized values >= 0.85rem (13.6px).
No hardcoded pixel font sizes below 13px remain in touched cockpit files.

## Guardrail

The minimum cockpit font size is enforced by the token system. All panels
reference `tokens.font.sizeXs` as their smallest size, which is 0.85rem.
The CSS guardrail class `.panel *` is defined but relies on browser support
for `min-font-size` which is limited — the token system is the primary control.
