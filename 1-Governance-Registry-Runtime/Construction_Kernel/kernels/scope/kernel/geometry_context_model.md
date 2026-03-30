# Geometry Context Model

## Purpose

Defines how building geometry affects scope complexity without performing geometric analysis. The Scope Kernel records geometric context as a scope complexity driver.

## Geometry Context Structure

Geometry context on scope records captures:
- **Building height**: Low-rise (1-3 stories), mid-rise (4-12), high-rise (13+)
- **Roof type**: Flat, low-slope, steep-slope, curved, multi-level
- **Facade type**: Simple wall, articulated, curtain wall, mixed
- **Penetration density**: Low, medium, high

## Geometry-Driven Scope Impacts

### Building Height
| Height Class | Scope Impact |
|---|---|
| Low-rise | Standard access, simpler sequencing |
| Mid-rise | Scaffold/lift access, vertical sequencing between floors |
| High-rise | Complex logistics, wind exposure, phased vertical sequencing |

### Roof Geometry
| Roof Type | Scope Impact |
|---|---|
| Flat / low-slope | Standard membrane scope, drainage considerations |
| Multi-level | Additional transitions, flashing scope at level changes |
| Curved | Custom fabrication scope, increased sheet metal complexity |
| Green / plaza | Waterproofing + protection + drainage scope layers |

### Facade Complexity
| Facade Type | Scope Impact |
|---|---|
| Simple wall | Standard air barrier and insulation scope |
| Articulated | Increased flashing and sealant scope at geometry changes |
| Curtain wall | Complex interface scope between glazing and opaque wall |
| Mixed systems | Multiple trade coordination zones |

### Penetration Density
| Density | Scope Impact |
|---|---|
| Low | Standard penetration sealing scope |
| Medium | Increased firestopping and flashing scope |
| High | Significant coordination scope, potential prefabrication |

## Geometry and Interface Zones

Complex geometry creates more interface zones. Each geometric transition (roof level change, wall plane offset, material change) generates at least one interface zone requiring explicit trade assignments.

## Geometry and Inspection Scope

Complex geometry increases inspection scope:
- More transitions require more pre-cover inspections
- Concealed conditions require inspection before closure
- Access constraints may require phased inspection schedules

## Recording Protocol

1. Geometry context is recorded on scope of work records via `geometry_context`.
2. Geometry does not change what is in scope -- it affects the complexity and quantity of scope items.
3. The Scope Kernel does not calculate quantities from geometry. Quantity takeoff is outside the truth domain.
