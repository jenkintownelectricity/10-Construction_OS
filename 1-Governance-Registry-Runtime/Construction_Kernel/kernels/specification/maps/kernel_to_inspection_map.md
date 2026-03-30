# Kernel-to-Inspection Map — Construction Specification Kernel

## Purpose

This map defines how specification requirements link to inspection steps. Specification requirements with `obligation_level: "shall"` and `evidence_required: true` are the primary drivers of inspection activities.

## Requirement-to-Inspection Linkage

### Field Testing Requirements

Testing requirements with `test_type: field_test` directly generate inspection steps:

| Spec Requirement Type | Inspection Activity |
|---|---|
| Adhesion testing per ASTM D4541 | Pull-off adhesion test at specified frequency |
| Air barrier testing per ASTM E2357 | Air leakage measurement at test locations |
| Water penetration testing per ASTM E1105 | Water spray test at fenestration openings |
| Flood testing of waterproofing | Standing water test at specified duration |

### Installation Verification Requirements

Requirements specifying installation methods generate visual and dimensional inspection steps:

| Spec Requirement | Inspection Step |
|---|---|
| Minimum flashing height at roof-to-wall | Measure flashing extension above roof surface |
| Fastener spacing in field/perimeter/corner zones | Verify fastener spacing per zone diagram |
| Membrane overlap minimum dimensions | Measure seam overlaps |
| Substrate preparation requirements | Verify substrate condition before installation |

### Submittal-Based Inspections

Submittal requirements generate document review inspection steps:

- Product data review against spec requirements
- Shop drawing conformance review
- Certificate and qualification verification
- Warranty document review

## Inspection Frequency

The `frequency` field on testing_requirement records drives inspection frequency. Common patterns:

- "One test per 10,000 square feet" — distributed across roof area
- "Each day of membrane application" — daily verification
- "At each penetration and transition" — location-specific
- "Prior to concealment" — timing-critical

## Inspection Scope

This kernel records what must be inspected (the specification requirement). How inspections are organized, scheduled, and documented is outside kernel scope.
