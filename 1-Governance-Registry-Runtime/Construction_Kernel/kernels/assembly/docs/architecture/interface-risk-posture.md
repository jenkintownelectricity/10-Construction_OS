# Interface Risk Posture — Construction Assembly Kernel

## Core Position

Transitions and penetrations are the highest-risk zones in any building enclosure. Field failure data consistently shows that the majority of enclosure failures occur not in the field of an assembly but at its boundaries, penetrations, and terminations. The kernel treats interface conditions as first-class objects with dedicated schemas, risk tracking, and evidence requirements.

## Risk Hierarchy

### Critical Risk Zones

1. **Penetrations** — Every penetration through the enclosure interrupts multiple control layers simultaneously. Pipes, conduits, structural members, and equipment anchors each require specific seal methods to restore control-layer continuity. Penetration density in the field of a roof or wall multiplies risk.

2. **Roof-to-Wall Transitions** — The junction where horizontal roof assembly meets vertical wall assembly is the most failure-prone transition in commercial construction. Water control, air control, thermal control, and vapor control must all transition between fundamentally different assembly configurations.

3. **Parapet Transitions** — Parapets impose a three-sided exposure condition: interior, exterior, and top. The membrane must transition from horizontal to vertical to horizontal (coping). Each change in direction creates a stress point.

### High Risk Zones

4. **Below-Grade Transitions** — The grade line transition subjects the assembly to hydrostatic pressure, backfill loads, and moisture from both directions. Waterproofing must transition to weather barrier with no gap in water control.

5. **Expansion Joints** — Designed movement joints must accommodate differential movement while maintaining water, air, and fire control. The assembly must move without tearing, debonding, or opening gaps.

6. **Curb Transitions** — Equipment curbs, skylights, and hatches interrupt the roof membrane. The membrane must transition vertically up the curb, turn over the top, and maintain water and air control at a three-dimensional intersection.

### Moderate Risk Zones

7. **Fenestration Edges** — Window and door perimeters require careful integration of the air barrier, water-resistive barrier, and flashing with the fenestration frame. Sequencing errors are common.

8. **Drain Transitions** — Roof drains and scuppers require the membrane to transition into drain hardware. Clamping ring assemblies and sealant joints must maintain water control at a low point where water concentrates.

9. **Roof Edges** — Perimeter edge conditions subject assemblies to the highest wind uplift pressures (corner and perimeter zones per FM/SPRI). Edge metal and membrane termination must resist these loads.

10. **Deck-to-Wall Transitions** — Plaza and balcony decks transitioning to vertical walls require waterproofing continuity under traffic loads and at a change in plane.

## Risk Tracking in Kernel Objects

- `transition_condition.risk_level` — Enum: critical, high, medium, low
- `penetration_condition.risk_level` — Enum: critical, high, medium, low
- `edge_condition` — Risk is implicit in edge type and assembly exposure
- All interface objects support `evidence_refs` to link risk assessment to supporting data

## Mitigation Posture

The kernel records interface conditions and their risk levels. It does not prescribe remediation. Mitigation strategies, best practices, and failure pattern intelligence belong to the Reference Intelligence layer. The kernel provides the structural truth that the intelligence layer reasons about.

## Evidence Requirements at Interfaces

Interface conditions at critical and high risk levels should include evidence references:
- Mock-up test results for transitions
- Field inspection reports for penetration seal verification
- Wind uplift test data for edge conditions
- Air leakage test results for air barrier continuity at transitions
