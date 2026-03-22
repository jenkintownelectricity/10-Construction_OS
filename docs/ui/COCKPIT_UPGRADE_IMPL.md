# Construction OS — Cockpit Upgrade Implementation Notes

**Document ID**: L0-CMD-CONOS-VKGL04R-COCKPITPLUS-001-IMPL
**Date**: 2026-03-22
**Authority**: Armand Lefebvre

## Touched Files

### New Components

| File | Purpose |
|------|---------|
| `src/ui/components/AuthorityHUD.tsx` | Adaptive Authority HUD — L3/L2/L1 display state |
| `src/ui/components/CommandPalette.tsx` | Semantic Action Bar (CMD+K / CTRL+K) |
| `src/ui/components/ContextualOverlay.tsx` | Division 07 split-view comparison overlay |
| `src/ui/layout/BottomDock.tsx` | Bottom dock consolidation for lower panels |
| `src/ui/devtools/DevToolsPanel.tsx` | Isolated dev/debug controls |

### Modified Files

| File | Changes |
|------|---------|
| `src/ui/workspace/WorkspaceShell.tsx` | Integrated Authority HUD, Bottom Dock, Command Palette, Dev Tools toggle; restructured desktop layout to top 3 panels + bottom dock |
| `src/ui/panels/PanelShell.tsx` | Removed MOCK badges from headers; added badge count support; added context collapse behavior; visual hierarchy refinement |
| `src/ui/panels/work/WorkPanel.tsx` | Added contextual overlay trigger and split-view integration; removed direct mock references from display |
| `src/ui/panels/diagnostics/RuntimeDiagnosticsPanel.tsx` | Added threaded/dependency mode; list/threaded toggle; stage focus on failure click; causal chain view |
| `src/ui/panels/explorer/ExplorerPanel.tsx` | Added subtle tree guide lines for visual hierarchy |
| `src/ui/panels/awareness/AwarenessPanel.tsx` | Added badge count for FAIL_CLOSED log |
| `src/ui/panels/proposals/ProposalMailbox.tsx` | Added badge count for pending proposals |
| `src/ui/panels/reference/ReferencePanel.tsx` | Improved empty state with reference source category explanations |
| `src/ui/theme/tokens.ts` | Added authority level colors (L3/L2/L1) |
| `src/ui/theme/GlobalStyles.tsx` | Added authority CSS vars, context collapse animation, command palette animation |
| `src/ui/stores/activeObjectStore.ts` | Added authorityLevel, overlayActive, devToolsVisible state |

## Panel Behaviors

### Contextual Overlay (Division 07)
- Activated via "Split View Overlay" button in Work panel detail tab
- Also activatable via Command Palette action "Open Contextual Overlay"
- LEFT side: current canonical/derived state from truth source
- RIGHT side: proposed modification from proposal pipeline
- Controls: Approve, Reject, Inspect Basis, Return to Prior Gravity
- Approve/Reject route to Proposal Mailbox (Ring 1 pathway) — NOT executed directly
- Overlay closes cleanly, restoring prior workspace state
- FAIL_CLOSED: If no active object, overlay shows safe empty state

### Authority HUD
- Displays L3 (blue), L2 (purple), L1 (gold) state indicator
- Positioned in top shell header alongside CONSTRUCTION OS title
- Awareness only — does NOT enforce authority logic
- Authority level can be changed via Dev Tools panel (dev mode only)
- Does NOT restyle the full application

### Threaded Diagnostics
- Events view has List / Threaded toggle
- List mode: flat chronological event list (default)
- Threaded mode: events grouped by pipeline stage with causal chain indicators
- Failed stages show "FAILED" badge; subsequent stages show "BLOCKED" with causal arrow
- Clicking a failure focuses the relevant pipeline stage and attempts to select the associated object
- FAIL_CLOSED: Missing causal data shows stage without chain indicator (safe degradation)

### Command Palette
- Triggered by CMD+K / CTRL+K or header button
- Searches across all cockpit domains in parallel:
  - **Objects**: via truth source adapter (project tree, all nodes)
  - **Zones**: via truth source adapter (zone-type nodes)
  - **Conditions**: via awareness adapter (active conditions by signature/type/stage)
  - **Proposals**: via proposal adapter (by ID, type, reasoning summary, source)
  - **Diagnostics**: via runtime diagnostics adapter (by event type, stage, message)
  - **References**: via reference adapter (by title, content, type, source document)
  - **Decks**: via deck store (by deck name, ID)
- Supports keyboard navigation (arrows, enter, escape)
- Empty query shows suggested starting points (Jump to AHU-01, Open CW-1, etc.)
- No-results state suggests valid query patterns with examples
- Built-in actions: Run Validation, Compare Mode, Focus Mode, Review Mode, Default Mode, Open Overlay
- Footer shows "Ring 3 — Navigate / Focus / Filter only" — cannot bypass authority boundaries
- FAIL_CLOSED: Each domain search fails independently; unavailable domains are silently skipped

### Bottom Dock
- Consolidates 6 lower panels: Awareness | Diagnostics | Proposals | Spatial | Assistant | System
- One panel visible at a time (tab-based)
- Panel state preserved when switching tabs (all panels stay mounted)
- Controls: Pin (keep dock open), Expand (increase height), Collapse (minimize to tab bar)
- Desktop/Laptop: Bottom dock appears below dockview area
- Tablet/Phone: Bottom dock hidden (panels accessible via companion switcher)

### Dev Control Isolation
- MOCK badges removed from all panel headers
- MOCK ADAPTERS badge removed from workspace status bar
- All dev controls consolidated into DevToolsPanel component
- Dev Tools toggle button in workspace status bar (labeled "DEV")
- Dev Tools panel shows: mock adapter status, authority level switcher, workspace mode selector, event log, active object info
- Visible only when devToolsVisible is true in store

### Visual Hierarchy
- Work panel is visually dominant (largest dockview allocation in top row)
- Panel title (sizeMd, semibold, uppercase) clearly distinct from sublabel (sizeXs, muted)
- Explorer tree guides: subtle vertical and horizontal connector lines between depth levels
- FAIL_CLOSED alert: dark card background with red left accent bar instead of full red block fill
- Badge dots on panel headers for: validation issues, pending proposals, FAIL_CLOSED entries, diagnostic failures

### Context Collapse
- Activated when workspaceMode is 'focus'
- Irrelevant panels dim to 40% opacity with "collapsed" sublabel
- Relevant panels auto-focus based on active object type:
  - element/assembly: explorer, work, reference, spatial, diagnostics, awareness
  - zone: explorer, spatial, work, awareness
  - document/specification: explorer, work, reference
  - project: explorer, work, system, awareness
- Work and System panels are always relevant (never collapsed)
- Collapsed panels show summary text: "Panel dimmed — not relevant to {type}: {name}"
- All collapsed views remain recoverable — switching back to default mode restores full visibility
- No destructive hiding: panel state is fully preserved underneath

### Reference Panel Empty State
- When no object is selected: Shows "REFERENCE SOURCES" card explaining 4 source categories:
  - Specs: Industry standards, code references, project specifications (AISC, ACI, ASTM)
  - Code: Design code sections, compliance requirements, regulatory references
  - Docs: Project drawings, assembly drawings, shop drawing references, reports
  - Citations: Calculation reports, verification notes, provenance documentation
- When object selected but no references: Explains that references are populated by source adapters
- Each source category has an icon and color consistent with the filter bar

### Dock Panel Empty States
- Each dock panel retains its own existing empty states from its panel implementation
- Awareness: "No awareness snapshot available" with explanation
- Diagnostics: "No runtime events received"
- Proposals: "No proposals match the current filter"
- Assistant: "No assistant responses yet"
- System: "No validation events yet" / "No tasks yet" / etc.
- All empty states remain useful and explain what content will appear

## FAIL_CLOSED Exceptions

| Component | Scenario | Behavior |
|-----------|----------|----------|
| ContextualOverlay | No active object | Overlay not rendered; button disabled |
| CommandPalette | Search domain failure | Domain silently skipped; results from other domains shown |
| CommandPalette | All domains fail | Helpful empty state with query suggestions |
| BottomDock | Panel render error | Individual panel shows its own FAIL_CLOSED state |
| AuthorityHUD | Invalid authority level | Falls back to L3 (Read-Only) |
| ContextCollapse | Unknown object type | Panel NOT collapsed (safe default) |
| ThreadedDiagnostics | No causal chain data | Stage shown without blocked indicator |

## Scope Verification

- [x] Only `Construction_Application_OS` repository modified
- [x] No kernel, atlas, runtime, bus, cache, or assistant modifications
- [x] No assistant execution authority added
- [x] No proposal auto-approval
- [x] No hidden execution through command palette
- [x] All advanced UI behavior fails closed to visible safe states
