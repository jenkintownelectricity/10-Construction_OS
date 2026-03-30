# Interface Risk Posture — Construction Specification Kernel

## Core Principle

Specification gaps at interface zones create construction risk. When a specification section addresses the field of a system but does not explicitly address transitions at interface zones, the gap itself is a specification fact that must be recorded and flagged.

## Interface Zones and Specification Risk

The shared `interface_zones.json` registry defines ten canonical interface zones. Each zone represents a transition where control layer continuity is most likely to be compromised. Specification sections that serve control layers at these zones must include explicit requirements, or the gap must be flagged.

### Risk Categories at Interface Zones

| Interface Zone | Primary Risk | Specification Gap Consequence |
|---|---|---|
| roof_to_wall | Water intrusion, air leakage | Membrane termination height, flashing laps unspecified |
| parapet_transition | Water intrusion, thermal bridging | Coping attachment, membrane wrap-up details missing |
| penetration | Water intrusion, air leakage, fire breach | Flashing collar type, sealant compatibility unspecified |
| fenestration_edge | Water intrusion, air leakage | Membrane-to-frame integration, sequencing gaps |
| below_grade_transition | Water intrusion, hydrostatic pressure | Transition from waterproofing to above-grade WRB unspecified |
| expansion_joint | Water intrusion, movement failure | Joint cover type, movement range unspecified |
| deck_to_wall | Water intrusion, drainage failure | Flashing height, drainage path unspecified |
| roof_edge | Wind uplift, water intrusion | Edge securement, drip detail missing |
| curb_transition | Water intrusion | Curb height, membrane wrap-up unspecified |
| drain_transition | Water intrusion, drainage failure | Drain flashing integration, clamping ring detail missing |

## Ambiguity Flag Requirement

When a specification section addresses a control layer but does not include explicit requirements for an interface zone where that control layer transitions, the kernel records:

1. The specification section and its `control_layers_served`
2. The interface zone that lacks explicit coverage
3. `ambiguity_flag: true` on affected requirements
4. A note identifying the interface gap

This is a fail-closed posture: absence of specification language at an interface zone is treated as a gap requiring resolution, not as implied compliance.

## Cross-Section Interface Coordination

Many interface zones span multiple specification sections. The roof-to-wall transition involves both roofing (07 5x 00) and air barrier (07 27 00) sections. When one section addresses the interface and the other does not, the gap is flagged in the section that omits it.

## Intelligence Layer Consumption

The intelligence layer (Construction_Reference_Intelligence) reads interface risk flags from this kernel to identify patterns of specification gaps across projects. The kernel provides the structured facts; the intelligence layer performs the analysis.
