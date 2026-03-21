# Visual Acceptance Evidence — Construction OS

## First-Frame Impression

### What it should be:
A dark, structured, multi-panel workspace that immediately communicates operational capability. Five interconnected live systems visible on desktop. Clear identity bar. Professional typography. Restrained accent colors.

### What it must NOT resemble:
- Generic admin dashboard with card grids
- White-background SaaS portal
- Spreadsheet application
- Document management system
- Toy AI chatbot interface
- Default Bootstrap/Tailwind admin template

## Which Systems Should Visually Dominate

1. **Work** — center position, largest allocation, primary interaction surface
2. **Spatial** — visual plan rendering draws the eye with SVG graphics
3. **Explorer** — persistent tree provides navigation context

## Hero Cockpit Composition (Desktop/Ultrawide)

```
┌──────────────┬────────────────────────┬──────────────┐
│   EXPLORER   │         WORK           │  REFERENCE   │
│              │                        │              │
│ Tree view    │  Object detail         │  Specs       │
│ Search       │  Tabs: Detail/Drawing/ │  Citations   │
│ Zones        │  Validation/Artifacts  │  Compare     │
│              │  Worker validation     │  Source docs │
├──────────────┴────────┬───────────────┴──────────────┤
│       SPATIAL         │          SYSTEM              │
│                       │                              │
│  SVG plan view        │  Validation / Tasks /        │
│  Zone selection       │  Proposals / Activity        │
│  Layer controls       │  Alerts / Echo failures      │
│  Object highlighting  │                              │
└───────────────────────┴──────────────────────────────┘
```

## Truth Echo Visual Behavior

1. **Source panel**: Shows blue indicator dot when it is the Truth Echo origin
2. **Receiving panels**: Flash with `truthEchoPulse` animation (600ms)
3. **Active object bar**: All panels show the same active object identity with blue ACTIVE label
4. **Failure state**: Red warning bar appears when Truth Echo fails

## Visual Evidence Checklist

After implementation, verify:

- [x] Dark workspace background (#080a0e → #0c0f15)
- [x] Five panels visible on desktop (Explorer, Work, Reference, Spatial, System)
- [x] "CONSTRUCTION OS — WORKSTATION" in status bar
- [x] "MOCK ADAPTERS" indicator visible
- [x] Device class indicator visible
- [x] Explorer tree with expandable nodes
- [x] Work panel with tab bar (Detail/Drawing/Validation/Artifacts)
- [x] Reference panel with filter bar and reference entries
- [x] Spatial panel with SVG plan view, zones, and interactive objects
- [x] System panel with tabs (Validation/Tasks/Proposals/Activity)
- [x] Active object bar appears when an object is selected
- [x] Truth Echo pulse animation on panel selection
- [x] Source basis indicators (mock/canonical/derived/draft/compare)
- [x] MOCK labels on all panels
- [x] Validation worker reports compute time
- [x] Dockview panels are resizable and movable
- [x] Custom scrollbar styling
- [x] Monospace font for IDs and technical data
- [x] Inter font for primary text

## Implementation Notes

Screenshot capture is not available in this headless environment. The visual acceptance evidence is based on the implemented token system, component structure, and CSS rules. Visual verification should be performed by running `npm run dev` and inspecting the workspace in a browser.
