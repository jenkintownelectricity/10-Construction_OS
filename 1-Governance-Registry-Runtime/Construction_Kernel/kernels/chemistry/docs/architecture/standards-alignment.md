# Chemistry Kernel Standards Alignment

## Alignment Posture

This kernel is standards-aware. It references standards by identifier and maps chemistry objects to relevant test methods and classifications. It does not reproduce standards text.

## Referenced Standards Bodies

| Body | Domain | Usage in This Kernel |
|---|---|---|
| ASTM International | Test methods, material classifications | Cure testing, adhesion testing, compatibility testing |
| ISO | International test methods | Adhesion, aging, chemical resistance |
| SCAQMD | VOC regulations | VOC limit references for solvent systems |
| EPA | Environmental regulations | Hazardous material classifications |
| OSHA | Workplace safety | Exposure limits referenced in hazard records |
| UL | Fire testing | Flame spread, smoke development for coatings |

## Key ASTM Standards Referenced

- **ASTM C920** — Elastomeric joint sealants (chemistry families, cure types)
- **ASTM C794** — Adhesion-in-peel of sealants (adhesion rule test method)
- **ASTM C1135** — Sealant compatibility (incompatibility rule evidence)
- **ASTM C719** — Cyclic movement of sealants (cure performance validation)
- **ASTM D412** — Tensile properties of elastomers (Material Kernel, not here)
- **ASTM D2240** — Durometer hardness (Material Kernel, not here)
- **ASTM C836** — Building sealant surface preparation (adhesion context)
- **ASTM D4541** — Pull-off adhesion testing (adhesion rule evidence)
- **ASTM G154** — UV exposure testing (degradation mechanism evidence)
- **ASTM G155** — Xenon arc exposure (degradation mechanism evidence)

## Standards-to-Object Mapping

Standards references appear in:
- `adhesion_rule.test_method_ref` — ASTM test method used to verify adhesion
- `degradation_mechanism.evidence_refs` — Accelerated aging test standards
- `chemical_hazard_record.regulatory_refs` — OSHA, EPA, SCAQMD references
- `solvent_system.regulatory_class` — VOC regulatory classification

## Boundary with Standards

This kernel stores the mapping between chemistry objects and standard identifiers. It does not interpret whether a specific product passes or fails a standard — that is an intelligence-layer determination requiring test data.
