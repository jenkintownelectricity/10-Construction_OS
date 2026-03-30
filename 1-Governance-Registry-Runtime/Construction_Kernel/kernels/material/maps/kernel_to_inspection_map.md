# Kernel-to-Inspection Map — Construction Material Kernel

## Purpose
Maps how material kernel data supports quality inspection and field verification activities.

## Inspection-Relevant Material Data

| Data Type | Inspection Use | Kernel Source |
|---|---|---|
| Material properties | Verify delivered materials meet property requirements | Material Property records |
| Compatibility matrices | Verify adjacent materials are compatible | Compatibility Records |
| Temperature ranges | Verify application temperature compliance | Material Entry temperature_range |
| Standards references | Identify applicable test methods for field testing | Standards Reference records |
| Weathering behavior | Baseline for in-service condition assessment | Weathering Behavior records |

## Inspection Integration Points

| Inspection Activity | Material Data Required |
|---|---|
| Material submittal review | Material class, properties, standards compliance |
| Pre-installation verification | Application temperature range, substrate compatibility |
| In-progress inspection | Material compatibility at transitions, adhesion requirements |
| Post-installation testing | Property values for comparison against field test results |
| Warranty inspection | Weathering baseline, expected degradation rates |

## Data Flow

Material truth flows from the kernel to inspection processes. Inspection results (field test data, condition assessments) may flow back as new evidence records, entering the kernel as draft records subject to validation.

## Boundary

The kernel provides material reference data for inspection. Inspection procedures, checklists, pass/fail criteria, and inspection scheduling are outside kernel scope. The Specification Kernel owns acceptance criteria; this kernel provides the material property values against which acceptance is evaluated.
