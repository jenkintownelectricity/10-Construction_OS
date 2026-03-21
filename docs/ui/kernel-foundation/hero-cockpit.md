# Hero Cockpit — HERO_COCKPIT_DEFAULT

## Purpose

The first-frame sought-after workspace composition. When the cockpit loads, it must immediately feel powerful, structured, and operational.

## Preset Name

`HERO_COCKPIT_DEFAULT`

## Composition

### Work (center-of-gravity)
- Largest panel allocation
- Center position in all layouts
- Tabs: Detail, Drawing, Validation, Artifacts
- Worker-backed validation button
- Compare mode support

### Explorer (persistent)
- Left position
- Project tree with zone/object hierarchy
- Search bar
- Expandable nodes
- Selection emits Truth Echo

### Reference (visible)
- Right position on desktop+
- Specs, citations, documents for active object
- Filter bar (All/Specs/Code/Citations/Docs)
- Compare view support

### Spatial (visible or one action away)
- Bottom-left on desktop/ultrawide
- SVG plan view with zones and objects
- Layer controls (structural, envelope, MEP)
- Zone and object selection emits Truth Echo
- Hidden on laptop/tablet/phone but accessible via Dockview tab or companion switcher

### System (visible or pinned)
- Bottom-right on desktop/ultrawide
- Validation, Tasks, Proposals, Activity tabs
- Alert display for Truth Echo failures
- Task creation from active object
- Hidden on laptop/tablet/phone but accessible

## Truth Echo in Hero Cockpit

When a user selects an object in Explorer:
1. Explorer emits `object.selected`
2. Truth Echo sets active object in store
3. Work panel reorients to show object detail
4. Reference panel loads references for the object
5. System panel highlights validation status
6. All panels show the same active object identity bar

When a user selects a zone in Spatial:
1. Spatial emits `zone.selected`
2. Truth Echo sets active object to the zone
3. Explorer highlights the zone in the tree
4. Work panel reorients to zone detail
5. Reference panel loads zone references
6. System panel reflects zone validation state

## Device Adaptation

| Device | Visible Panels | Hidden (accessible) |
|--------|---------------|-------------------|
| UltraWide | Explorer, Work, Reference, Spatial, System | — |
| Desktop | Explorer, Work, Reference, System | Spatial |
| Laptop | Explorer, Work, Reference | Spatial, System |
| Tablet | Explorer, Work | Reference, Spatial, System |
| Phone | Work | All via CompanionSwitcher |
