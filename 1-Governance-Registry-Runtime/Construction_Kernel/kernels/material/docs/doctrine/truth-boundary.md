# Truth Boundary — Construction Material Kernel

## Owned Truth Surface

This kernel owns material-domain truth and nothing else. Material truth includes:

- **Material classes** — thermoplastic, thermoset, elastomer, bituminous, cementitious, metallic, mineral fiber, cellular plastic, composite, fluid applied, sheet applied, spray applied
- **Material forms** — sheet, liquid, foam, rigid board, batt, loose fill, paste, tape, coating, membrane, panel
- **Physical properties** — tensile strength, elongation, permeance, R-value, flame spread, smoke developed, tear resistance, puncture resistance, dimensional stability
- **Performance characteristics** — tested values under standard conditions with test method references
- **Compatibility relationships** — material-to-material compatibility as compatible, incompatible, conditional, or untested
- **Weathering behavior** — UV resistance, thermal cycling response, moisture exposure effects, freeze-thaw resistance, biological resistance
- **Hygrothermal properties** — vapor permeance, moisture absorption, capillary coefficient, sorption isotherm, wet thermal conductivity
- **Material-to-control-layer mappings** — which control layers a material class can serve
- **Standards references** — ASTM test methods that define material properties (by citation only)
- **Evidence pointers** — traceable references to lab tests, manufacturer TDS, field data

## Not Owned — Specification Truth

Specification requirements, obligation levels, submittal requirements, warranty terms, and qualification criteria are owned by the Construction Specification Kernel. A specification may require "tensile strength not less than 200 psi" — that requirement is specification truth. The actual tensile strength value of a specific material class is material truth stored here.

## Not Owned — Assembly Truth

Assembly configurations, layer sequences, attachment methods, and system compositions are owned by the Construction Assembly Kernel. This kernel knows that a TPO membrane has certain physical properties. How that membrane is configured within a roofing assembly (substrate, insulation layers, attachment, coverboard) is assembly truth.

## Not Owned — Chemistry Truth

Chemical reaction behavior, adhesion mechanisms, cure kinetics, solvent compatibility, and molecular interaction models are owned by the Construction Chemistry Kernel. This kernel records that two materials are incompatible. The chemistry kernel explains the chemical mechanism of that incompatibility (e.g., plasticizer migration, solvent attack).

## Not Owned — Scope Truth

Project scope boundaries, trade responsibilities, division of work, and exclusion clauses are owned by the Construction Scope Kernel. Material selection may be influenced by scope constraints, but scope truth is not duplicated here.

## Not Owned — Reference Intelligence

Pattern analysis, cross-kernel correlation, risk scoring, and design guidance generation are performed by Construction_Reference_Intelligence. This kernel provides structured material truth that the intelligence layer reads. It does not perform intelligence operations.

## Boundary Enforcement

Any record that crosses a truth boundary is rejected at schema validation. Fields belonging to other kernels are not present in material schemas. Cross-kernel relationships use pointer references only. When a material fact implies truth that belongs to another kernel, only the material-side fact is recorded here with a reference pointer.
