# Interface Risk Map — Construction Material Kernel

## Purpose
Maps material-side interface risks at common Division 07 building envelope transition zones.

## High-Risk Material Interfaces

| Interface Zone | Material A | Material B | Risk | Kernel Data |
|---|---|---|---|---|
| PVC on polystyrene | PVC membrane | EPS/XPS insulation | Plasticizer migration destroys foam | Compatibility: incompatible |
| Bitumen on polystyrene | Modified bitumen | EPS/XPS insulation | Solvent attack on foam | Compatibility: incompatible |
| EPDM-to-TPO transition | EPDM membrane | TPO membrane | Cannot heat-weld dissimilar polymers | Compatibility: conditional |
| Silicone on bitumen | Silicone sealant | Bituminous surface | Adhesion failure | Compatibility: incompatible |
| Metal flashing on dissimilar metal | Copper flashing | Aluminum coping | Galvanic corrosion | Compatibility: incompatible |

## Moderate-Risk Material Interfaces

| Interface Zone | Material A | Material B | Risk | Kernel Data |
|---|---|---|---|---|
| TPO on polyiso | TPO membrane | Polyiso insulation | Generally compatible; verify adhesive | Compatibility: compatible |
| Urethane sealant on concrete | Urethane sealant | Concrete substrate | Compatible with primer | Compatibility: conditional |
| EPDM adhesive on cover board | EPDM bonding adhesive | Gypsum cover board | Requires proper primer | Compatibility: conditional |

## Data Gap Risks (Untested Interfaces)

| Interface Zone | Material A | Material B | Risk Level | Action |
|---|---|---|---|---|
| New formulation contact | Reformulated TPO | Legacy adhesive | Unknown | Flag for testing |
| Cross-manufacturer contact | Brand A TPO | Brand B flashing | Unknown | Flag for compatibility data |

## Risk Mitigation Data

For each incompatible or conditional interface, the kernel provides:
- Compatibility result with evidence references
- Conditions for conditional compatibility (separation sheets, primers)
- Chemistry kernel pointer for mechanism explanation
- Weathering data for exposed interface materials

## Interface Risk Posture

All untested material interfaces default to `untested` status. The intelligence layer prioritizes untested pairs at common interface zones for testing. No system should assume compatibility at an interface without an active compatibility record.
