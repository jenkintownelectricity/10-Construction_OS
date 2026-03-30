# Standards Alignment — Construction Assembly Kernel

## Posture

The Assembly Kernel is standards-aware but does not reproduce standards text. It references standards by citation and tracks assembly compliance as structured metadata. Standards interpretation remains with qualified professionals.

## Primary Standards Governing Assembly Compliance

### IBC — International Building Code

The IBC establishes mandatory requirements for building enclosure assemblies:

- **Chapter 14 — Exterior Walls**: Wall assembly requirements including weather resistance, fire resistance, and structural adequacy.
- **Chapter 15 — Roof Assemblies and Rooftop Structures**: Roof assembly requirements for weather protection, fire classification, and wind resistance.
- **Chapter 26 — All-Glass Buildings and Enclosures**: Glazed assembly provisions.
- **Section 1402.2 — Weather Protection**: Requires exterior walls to provide weather protection for the building.
- **Section 1503 — Weather Protection**: Requires roof coverings to be securely fastened, providing weather protection.
- **Table 601 / Table 602**: Fire-resistance-rated construction requirements affecting assembly composition.

Assembly records reference IBC sections through `standards_refs` fields. Compliance status is recorded on tested assembly records.

### NFPA 285 — Fire Propagation of Exterior Wall Assemblies

NFPA 285 governs fire propagation testing for exterior non-load-bearing wall assemblies containing combustible components:

- Applies when combustible materials (foam insulation, WRBs, etc.) are used in wall assemblies above 40 feet.
- Tested assembly records capture the specific configuration tested: substrate, insulation type and thickness, air/water barrier, cladding.
- Substitution of any component invalidates the tested configuration. The kernel records exactly what was tested.
- Assembly records link to NFPA 285 test reports through `evidence_refs`.

### ASHRAE 90.1 — Energy Standard

ASHRAE 90.1 drives assembly configuration through thermal performance requirements:

- **Section 5 — Building Envelope**: Prescriptive insulation requirements by climate zone and assembly type.
- **Table 5.5-1 through 5.5-8**: Minimum R-values and maximum U-factors for opaque assemblies.
- Continuous insulation requirements affect layer position and control-layer assignments.
- Assembly records track climate zone applicability and thermal control layer configuration.

## Secondary Standards Referenced

| Standard | Assembly Relevance |
|---|---|
| FM 4450 / FM 4470 | Wind uplift classification for roof assemblies |
| UL 580 / UL 790 | Roof wind uplift and fire classification |
| ASTM E2357 | Air leakage of building enclosure assemblies |
| ASTM E331 | Water penetration of exterior wall assemblies |
| ASTM E119 | Fire endurance of building construction |
| ASTM C1549 / C518 | Thermal performance measurement |
| AAMA 501 / 503 | Wall assembly water and structural testing |
| SPRI ES-1 | Edge securement for low-slope roof systems |

## Linkage to Assembly Objects

- `assembly_system` — `standards_refs[]` lists applicable standards by reference ID.
- `tested_assembly_record` — `test_standard_ref` identifies the specific test method. `result` captures the outcome.
- `continuity_requirement` — May reference code sections driving the continuity obligation.
- `transition_condition` — Standards may govern specific transition details (e.g., NFPA 285 at floor lines).

## Non-Reproduction Commitment

This kernel cites standards by reference ID, section number, and table number only. It does not embed, paraphrase, or reproduce copyrighted standards text. Users must consult the referenced standard directly for requirements.
