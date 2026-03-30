# Climate Context Model

## Purpose

Defines how climate conditions affect scope execution without owning climate data. The Scope Kernel records climate-driven constraints as scope modifiers.

## Climate Context Structure

Climate context on scope records captures:
- **Climate zone**: IECC climate zone reference (zones 1 through 8)
- **Seasonal restrictions**: Work operations that are constrained by season
- **Temperature constraints**: Minimum and maximum application temperatures
- **Weather event constraints**: Wind, rain, snow conditions that halt work

## Climate-Driven Scope Constraints

### Temperature-Sensitive Operations
| Operation Type | Typical Temperature Constraint |
|---|---|
| Fluid-applied air barrier | Minimum 40 degrees F, rising |
| Self-adhered membrane | Minimum 40 degrees F substrate |
| TPO heat welding | Adjust parameters below 40 degrees F |
| Sealant application | Per manufacturer, typically 40-100 degrees F |
| Spray polyurethane foam | Minimum 40 degrees F, maximum 120 degrees F |
| Concrete waterproofing | Minimum 40 degrees F for cure |

### Wind-Sensitive Operations
| Operation Type | Typical Wind Constraint |
|---|---|
| Loose-laid membrane | Maximum 20 mph sustained |
| Spray-applied coatings | Maximum 15 mph to avoid overspray |
| Sheet metal hoisting | Maximum 25 mph sustained |
| Crane operations | Per crane chart, typically 20-30 mph |

### Moisture-Sensitive Operations
| Operation Type | Moisture Constraint |
|---|---|
| Below-grade waterproofing | Substrate moisture below threshold |
| Roofing insulation | No wet materials installed |
| Air barrier application | Dry substrate required |
| Adhesive-set roofing | No rain during open time |

## Seasonal Work Windows

In northern climates (IECC zones 5-8), some building envelope operations have limited seasonal windows:
- Roofing: Typically April through November
- Waterproofing: Frost-free conditions required
- Exterior sealants: Temperature-dependent window

The Scope Kernel records these constraints but does not generate schedules.

## Recording Protocol

1. Climate constraints are recorded on work operations via `weather_constraints`.
2. Sequence steps may carry `weather_constraints` for phase-level restrictions.
3. The `climate_context` field on scope of work records captures project-level climate data.
4. Climate constraints do not override scope -- they constrain when scope can be executed.
