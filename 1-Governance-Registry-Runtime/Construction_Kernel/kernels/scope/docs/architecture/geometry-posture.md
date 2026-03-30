# Geometry Posture

## Purpose

Defines how the Scope Kernel accounts for building geometry as a factor that affects scope complexity, trade coordination, and interface density. The kernel does not own geometric models -- it records how geometry influences scope.

## Principle

Geometry is a scope complexity driver. Complex geometry creates more interface zones, more sequencing dependencies, and more inspection points. The Scope Kernel records geometric context without performing geometric analysis.

## Geometry-Affected Scope Elements

### 1. Interface Zone Density
Complex building geometries generate more interface zones:
- Curved roofs increase flashing complexity
- Multi-level roof transitions create additional scope boundaries
- Irregular floor plans increase sealant joint scope
- Cantilevered elements create unique waterproofing conditions

### 2. Trade Coordination Complexity
Geometry affects the number of trades working in proximity:
- High-rise buildings require vertical sequencing across many trades
- Complex facades increase curtain wall / air barrier / insulation coordination
- Roof penetration density affects roofing and MEP trade coordination

### 3. Inspection Access
Geometry affects inspection feasibility:
- Concealed conditions require pre-cover inspection before closure
- High-elevation work requires scaffold or lift access for inspection
- Below-grade work has narrow inspection windows before backfill

### 4. Scope Quantity Drivers
While the Scope Kernel does not estimate quantities, it records geometric factors that affect scope:
- Linear feet of transitions and terminations
- Number of penetrations
- Area classifications (field vs. perimeter vs. corner zones for wind uplift)

## Geometry Context in Scope Records

The `geometry_context` field on scope records captures:
- Building height classification
- Roof geometry type (flat, sloped, curved, multi-level)
- Facade complexity (simple, articulated, curtain wall)
- Penetration density (low, medium, high)

## What the Scope Kernel Does NOT Do

- Does not perform geometric calculations or modeling
- Does not store BIM geometry
- Does not calculate material quantities from geometry
- Does not generate shop drawings or detail drawings

## Division 07 Geometry Sensitivity

| Scope Category | Geometry Sensitivity | Impact |
|---|---|---|
| Membrane roofing | High | Roof shape, slope, penetration count |
| Waterproofing | Medium | Foundation depth, plaza deck geometry |
| Air barriers | High | Facade complexity, opening count |
| Flashing | Very High | Transition count, geometry complexity |
| Sheet metal | High | Custom shapes, complex copings |
| Sealants | Medium | Joint length, joint width variation |
| Fireproofing | Low | Follows structural geometry |
