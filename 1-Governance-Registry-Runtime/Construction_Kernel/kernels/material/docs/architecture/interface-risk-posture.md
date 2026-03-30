# Interface Risk Posture — Construction Material Kernel

## Interface Risk Philosophy

Material interfaces are the primary failure zones in building envelope systems. This kernel records material behavior at interface zones but does not predict interface failures. Interface risk assessment that combines material data with assembly context belongs to the intelligence layer.

## Material-Side Interface Risks

| Risk Category | Material Kernel Role | Not Owned |
|---|---|---|
| Chemical incompatibility | Records compatibility result and evidence | Explains chemical mechanism (Chemistry Kernel) |
| Differential thermal movement | Records thermal expansion coefficients | Models assembly-level movement (Assembly Kernel) |
| Moisture migration at interfaces | Records permeance and absorption values | Models vapor drive through assemblies (Assembly Kernel) |
| Adhesion loss | Records adhesion test values | Predicts field adhesion loss over time (not modeled) |
| UV degradation at exposed seams | Records UV weathering behavior | Predicts seam failure timing (not modeled) |

## Interface Zone Coverage

This kernel provides material property data relevant to interface zones defined in the shared interface_zones.json registry:

| Interface Zone | Material Data Provided |
|---|---|
| Roof-to-wall transition | Material compatibility, permeance, flexibility |
| Membrane overlap seams | Weld strength, peel adhesion, chemical compatibility |
| Flashing terminations | Adhesion, elongation, thermal cycling resistance |
| Penetration details | Sealant compatibility, substrate adhesion, movement capacity |
| Expansion joints | Elongation, recovery, thermal range, fatigue resistance |

## Risk Data Structure

Material interface risk data is structured as:
- Compatibility records between materials that meet at interface zones
- Weathering behavior records for materials exposed at interface zones
- Property records for interface-relevant characteristics (adhesion, elongation, flexibility)

## Fail-Closed Interface Posture

When interface compatibility data is missing, the kernel does not assume compatibility. Untested material pairs at interface zones are flagged with `compatibility_result: untested`. The intelligence layer surfaces these gaps for resolution. No downstream consumer should treat an untested interface as safe.

## Boundary with Assembly Kernel

This kernel provides material-level interface data. The Assembly Kernel owns interface zone configurations, detail sequences, and system-level interface risk. Material data flows to the Assembly Kernel via structured pointers.
