# TRIAD-01 — UI Foundation Triad

## Metadata
- **Triad ID**: TRIAD-01
- **Version**: 1.0.0
- **Wave**: UI Kernel Foundation
- **Kernels**: KERN-UI-PATTERN, KERN-SCREEN-ORCHESTRATION, KERN-CONTEXT-AND-TRUTH, KERN-INGREDIENT-PLACEMENT-OPTIONALITY

## Purpose

The UI Foundation Triad binds the four UI kernels into a coherent governing framework for the Construction OS cockpit. It defines how the kernels relate, where their boundaries are, and what rules govern their interaction.

## Triad Composition

```
KERN-UI-PATTERN ←→ KERN-SCREEN-ORCHESTRATION
       ↕                      ↕
KERN-CONTEXT-AND-TRUTH ←→ KERN-INGREDIENT-PLACEMENT-OPTIONALITY
```

### KERN-UI-PATTERN
Governs *what it looks like*. Visual quality, composition rules, dashboard drift prevention.

### KERN-SCREEN-ORCHESTRATION
Governs *where things go*. Device adaptation, panel counts, companion behavior.

### KERN-CONTEXT-AND-TRUTH
Governs *what it's about*. Active object identity, Truth Echo, source basis.

### KERN-INGREDIENT-PLACEMENT-OPTIONALITY
Governs *what appears when*. Persistent vs contextual vs system vs optional ingredients.

## Interaction Rules

1. **PATTERN → ORCHESTRATION**: Pattern defines visual quality standards. Orchestration ensures those standards apply at every device class.
2. **ORCHESTRATION → CONTEXT**: Orchestration determines which panels are visible. Context ensures Truth Echo still functions regardless of panel visibility.
3. **CONTEXT → PATTERN**: Context determines source basis and active identity. Pattern governs how that basis is visually communicated.
4. **INGREDIENT → ORCHESTRATION**: Ingredient placement rules interact with device orchestration — what's persistent on desktop may be accessible-via-companion on phone.
5. **INGREDIENT → CONTEXT**: Contextual ingredients depend on active object identity to know when to appear/disappear.
6. **INGREDIENT → PATTERN**: Pattern governs the visual treatment of each ingredient class.

## Governing Principle

No kernel may override another's owned scope. Conflicts are resolved by deferring to the kernel that owns the contested concept.
