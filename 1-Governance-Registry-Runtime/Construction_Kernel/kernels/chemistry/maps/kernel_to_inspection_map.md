# Kernel-to-Inspection Map

## Purpose

Describes how the Construction Chemistry Kernel supports chemical compatibility checks during inspection workflows.

## Inspection Touchpoints

| Chemistry Entity | Inspection Use |
|---|---|
| Adhesion Rule | Verify that the sealant-substrate pairing has verified or conditional adhesion status before approving joint installation. |
| Incompatibility Rule | Check that no incompatible chemistries are in direct contact at transitions, terminations, or layered assemblies. |
| Cure Mechanism | Confirm that ambient temperature and humidity satisfy cure constraints at time of application. |
| Chemical System | Validate that the installed product matches the specified chemical system (chemistry family, VOC, system type). |
| Degradation Mechanism | Flag active degradation signatures (plasticizer migration, UV damage, oxidation) during condition assessments. |
| Chemical Hazard Record | Ensure required precautions and PPE are documented for hazardous chemistry systems on site. |

## Data Flow

1. Inspection checklist references a chemical system by `system_id`.
2. Adhesion rules for that system and the target substrate are retrieved.
3. Incompatibility rules are cross-checked against adjacent materials.
4. Cure mechanism constraints are compared to recorded ambient conditions.
5. Pass/fail determination is recorded with evidence references.

## Constraints

- Chemistry kernel data is read-only during inspection. Findings do not modify kernel records.
- Inspection results reference kernel record IDs for traceability.
- Conditional adhesion statuses require inspector judgment and documentation.

## Cross-References

- Adhesion rule contract defines validation requirements.
- Incompatibility rule contract governs severity classifications.
- Cure mechanism contract specifies temperature and humidity validation.
