# Evidence Linkage Model — Construction Specification Kernel

## Purpose

This model defines how evidence (test reports, submittals, inspection records, manufacturer data) links to specification requirements. The kernel records what evidence is required by the specification; the actual evidence artifacts are stored and evaluated elsewhere.

## Linkage Structure

A specification requirement may declare that evidence is required through two mechanisms:

1. **evidence_required field** — boolean flag indicating that compliance evidence must be provided
2. **Testing requirements** — specific test records linked to the requirement via test_method_refs

## Evidence Types

Evidence types are defined in `shared_enum_registry.json` under `evidence_types`:

- `field_observation` — documented observation of installed conditions
- `lab_test` — laboratory test report per referenced ASTM or other standard
- `forensic_report` — investigation report of failure or performance issue
- `manufacturer_data` — manufacturer product data sheet or technical bulletin
- `literature` — published research or industry guidance
- `expert_judgment` — documented expert opinion
- `sensor_data` — monitoring data from installed sensors
- `inspection_report` — third-party inspection documentation
- `commissioning_report` — commissioning test results
- `warranty_claim` — warranty claim documentation

## Specification-Side Evidence Requirements

The kernel records what the specification demands, not the evidence itself:

| Specification Requirement | Evidence Linkage |
|---|---|
| "Installer shall have minimum 5 years experience" | qualification_requirement with evidence_required |
| "Perform adhesion test per ASTM D4541" | testing_requirement with test_method_ref |
| "Submit manufacturer's product data" | submittal_requirement of type product_data |
| "Provide 20-year NDL system warranty" | warranty_requirement with evidence_required |
| "Conduct preconstruction mock-up" | testing_requirement of type mock_up |

## Evidence Chain

The complete evidence chain spans multiple kernels and the intelligence layer:

1. **This kernel** — records that evidence is required and what type
2. **Source documents** — the actual evidence artifacts (test reports, submittals)
3. **Intelligence layer** — evaluates whether evidence satisfies the requirement

This kernel owns only step 1. Steps 2 and 3 are outside the specification truth boundary.

## Missing Evidence Handling

When a specification requires evidence but no evidence type is specified (e.g., "provide proof of qualification"), the kernel records `evidence_required: true` and sets `ambiguity_flag: true` with a note that the evidence type is unspecified.

## Evidence and Revision Lineage

When a specification revision changes evidence requirements (e.g., an addendum adds a new testing requirement), the revision lineage model captures the change. The original requirement record is deprecated and the new record with updated evidence requirements supersedes it.
