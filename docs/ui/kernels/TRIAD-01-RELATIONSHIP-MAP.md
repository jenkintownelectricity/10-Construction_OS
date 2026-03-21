# TRIAD-01 — Relationship Map

## Kernel Relationships

```
┌──────────────────────┐     ┌──────────────────────────┐
│   KERN-UI-PATTERN    │────▶│ KERN-SCREEN-ORCHESTRATION │
│                      │     │                          │
│ Visual composition   │     │ Device adaptation        │
│ Premium presentation │     │ Panel visibility         │
│ Dashboard drift ban  │     │ Companion behavior       │
│ Depth hierarchy      │     │ Workspace presets        │
└──────────┬───────────┘     └────────────┬─────────────┘
           │                              │
           │ basis display                │ panel visibility
           │ echo visuals                 │ affects echo scope
           │                              │
           ▼                              ▼
┌──────────────────────┐     ┌──────────────────────────┐
│ KERN-CONTEXT-AND-    │────▶│ KERN-INGREDIENT-         │
│ TRUTH                │     │ PLACEMENT-OPTIONALITY    │
│                      │     │                          │
│ Active object ID     │     │ Persistent ingredients   │
│ Truth Echo           │     │ Contextual ingredients   │
│ Source basis          │     │ System ingredients       │
│ Fail-closed rules    │     │ Optional ingredients     │
│ Compare state        │     │ Clutter prevention       │
└──────────────────────┘     └──────────────────────────┘
```

## Data Flow

```
User Action (panel interaction)
  → Event Bus (typed event)
    → Truth Echo (KERN-CONTEXT-AND-TRUTH)
      → Active Object Store update
        → Panel re-orientation (KERN-INGREDIENT-PLACEMENT-OPTIONALITY)
          → Visual update (KERN-UI-PATTERN)
            → Layout adaptation (KERN-SCREEN-ORCHESTRATION)
```

## Cross-Kernel Dependencies

| From | To | Dependency |
|------|----|-----------|
| UI-PATTERN | CONTEXT-AND-TRUTH | Source basis for visual indicators |
| UI-PATTERN | INGREDIENT-PLACEMENT | Ingredient class for visual treatment |
| SCREEN-ORCHESTRATION | CONTEXT-AND-TRUTH | Panel visibility affects Truth Echo scope |
| SCREEN-ORCHESTRATION | INGREDIENT-PLACEMENT | Device class affects ingredient visibility |
| CONTEXT-AND-TRUTH | Event Bus | Event delivery for Truth Echo |
| INGREDIENT-PLACEMENT | CONTEXT-AND-TRUTH | Active object determines contextual visibility |
