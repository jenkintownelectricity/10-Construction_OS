# Device Orchestration — Construction OS

## Device Classes

| Class | Breakpoint | Max Panels | Layout Mode | Primary | Companion |
|-------|-----------|------------|-------------|---------|-----------|
| UltraWide | ≥2560px | 6 | full-cockpit | work | — |
| Desktop | ≥1440px | 4 | full-cockpit | work | — |
| Laptop | ≥1024px | 3 | split | work | — |
| Tablet | ≥768px | 2 | compact | work | explorer |
| Phone | <768px | 1 | single-companion | work | explorer |

## Behavior Per Device Class

### UltraWide (≥2560px)
- 4–6 visible live systems possible
- Full cockpit layout: Explorer | Work | Reference + Spatial | System
- Must feel like a coherent cockpit, not panel chaos
- All five systems visible simultaneously

### Desktop (≥1440px)
- 3–4 visible live systems
- Explorer | Work | Reference visible, System visible
- Spatial accessible one action away

### Laptop (≥1024px)
- 2–3 visible live systems
- Explorer | Work | Reference visible
- Spatial and System accessible via tab/switch

### Tablet (≥768px)
- 2 visible live systems
- Work + Explorer visible
- Others accessible via panel switching

### Phone (<768px)
- 1 primary live system (Work)
- 1 pinned companion (Explorer)
- Quick switching between all 5 systems via CompanionSwitcher
- Active context preserved across switches
- No dead-end navigation

## Rules

1. **Capability equivalence**: All five systems are accessible at every device class.
2. **Context persistence**: Active object survives device class transitions.
3. **Phone companion**: Always has a defined companion panel for quick access.
4. **Ultrawide composition**: More panels means better composition, not more clutter.
5. **Truth Echo across devices**: Functions at every device class.
6. **Work as primary**: Always the primary panel — center-of-gravity.

## Code Location

Implementation: `src/ui/orchestration/DeviceOrchestrator.ts`
Tests: `src/ui/orchestration/DeviceOrchestrator.test.ts`
