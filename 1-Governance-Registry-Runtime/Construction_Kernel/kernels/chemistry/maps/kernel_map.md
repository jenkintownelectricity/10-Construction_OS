# Chemistry Kernel Map

## Purpose

Provides an overview of the Construction Chemistry Kernel and its internal entity relationships.

## Kernel Identity

- **Name:** Construction_Chemistry_Kernel
- **Domain:** Construction chemistry — sealants, adhesives, coatings, membranes, and related chemical systems used in Division 07 and adjacent building envelope work.
- **Schema Version:** v1
- **Status:** Active

## Core Entities

| Entity | Schema | Description |
|---|---|---|
| Chemical System | chemical_system.schema.json | A formulated product defined by chemistry family, cure mechanism, and solvent system. |
| Chemistry Entry | chemistry_entry.schema.json | A single chemistry fact: compatibility rule, cure profile, adhesion requirement, or constraint. |
| Polymer Family | polymer_family.schema.json | A polymer classification with characteristic properties and known incompatibilities. |
| Additive | additive.schema.json | A chemical additive with type classification and migration risk flag. |
| Cure Mechanism | cure_mechanism.schema.json | The curing process including temperature, humidity, and time constraints. |
| Solvent System | solvent_system.schema.json | Carrier system classification with VOC, flash point, and regulatory data. |
| Adhesion Rule | adhesion_rule.schema.json | A verified or conditional adhesion relationship between a chemistry and substrate. |
| Incompatibility Rule | incompatibility_rule.schema.json | A known adverse interaction between two chemistries. |
| Degradation Mechanism | degradation_mechanism.schema.json | A deterioration process tied to a chemistry and environmental factors. |
| Chemical Hazard Record | chemical_hazard_record.schema.json | Hazard classification with exposure route, regulatory refs, and precautions. |

## Relationships

- Chemical systems reference cure mechanisms and solvent systems.
- Adhesion rules reference chemical systems and substrates.
- Incompatibility rules reference pairs of chemical systems.
- Degradation mechanisms reference the affected chemistry system.
- Chemical hazard records reference chemistry systems.
- Chemistry entries serve as general-purpose fact records spanning all domains above.

## Design Principles

- All records are static truth. No runtime behavior is embedded.
- All schemas enforce `additionalProperties: false`.
- Cross-references use string IDs, not embedded objects.
- Evidence references trace claims to lab tests, field studies, or manufacturer data.
