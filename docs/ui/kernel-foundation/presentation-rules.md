# Presentation Rules — Construction OS

## Visual Identity

Construction OS must feel: **powerful, sought-after, serious, structured, premium, calm but technically potent.**

It must NOT feel like: generic admin SaaS, spreadsheet portal, dead dashboard, cluttered document manager, toy AI app.

## Depth Hierarchy

Three visual depth layers govern the cockpit:

1. **Work Surface** (foreground) — highest visual weight. Work and Spatial panels dominate.
2. **Context Surface** (mid-ground) — Explorer and Reference panels support the work surface.
3. **Intelligence Surface** (background) — System panel provides awareness without competing for attention.

## Design Token System

Located: `src/ui/theme/tokens.ts`

### Color Palette
- **Background**: Dark blue-gray progression (`#080a0e` → `#252d42`)
- **Foreground**: Cool gray text hierarchy (`#e0e4ec` → `#555d73`)
- **Accent**: Restrained blue (`#3b82f6`) — used sparingly for active states
- **Semantic**: Green (success), Yellow (warning), Red (error), Orange (mock)
- **State**: Green (canonical), Gray (derived), Yellow (draft), Purple (compare), Orange (mock)

### Typography
- **Primary**: Inter — clean, professional, high readability
- **Monospace**: JetBrains Mono — for IDs, code, technical data
- **Sizes**: 11px–20px range, no oversized headlines

### Truth Echo Visual Language
- **echoActive**: Blue indicator dot on source panel
- **echoPulse**: 600ms animation on receiving panels
- **echoTrace**: Subtle blue background on active object bar
- **echo shadow**: Blue glow ring on panels during propagation

## Forbidden Patterns

1. Card grids as primary layout
2. Metric tiles / KPI widgets
3. Fake AI sparkle effects
4. Decorative motion without value
5. Rounded-everything soft UI
6. White/light backgrounds
7. Generic admin template aesthetics
8. Oversized hero sections
9. Empty state illustrations

## First-Frame Impression Standard

When the workspace loads, the user must immediately see:
1. Dark, structured, premium workspace
2. Five interconnected live systems (on desktop+)
3. "CONSTRUCTION OS — WORKSTATION" identity
4. Mock adapter indicator (honest about current state)
5. Panel hierarchy with Work as center-of-gravity
6. Clickable, interactive tree in Explorer
7. SVG plan rendering in Spatial

The first frame must communicate: "This is a serious operating environment, not a prototype."
