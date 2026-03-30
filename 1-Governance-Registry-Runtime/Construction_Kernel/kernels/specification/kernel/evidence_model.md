# Evidence Model — Construction Specification Kernel

## Purpose

This model defines how the specification kernel relates to evidence that supports or demonstrates compliance with specification requirements. The kernel records what evidence is required — not the evidence itself.

## Evidence in Specification Context

Specifications require evidence of compliance through several mechanisms:

### Submittal-Based Evidence
Product data sheets, shop drawings, samples, test reports, certificates, and warranty documents submitted by the contractor for architect/engineer review. Governed by `submittal_requirement` records.

### Test-Based Evidence
Field tests, laboratory tests, mock-ups, and preconstruction tests that demonstrate performance compliance. Governed by `testing_requirement` records.

### Qualification-Based Evidence
Documentation of manufacturer experience, installer certifications, testing agency accreditation, and inspector qualifications. Governed by `qualification_requirement` records.

### Warranty-Based Evidence
Executed warranty documents demonstrating that warranty requirements have been fulfilled. Governed by `warranty_requirement` records.

## Evidence Types from Shared Registry

The `shared_enum_registry.json` defines canonical evidence types:

- `field_observation` — site inspection documentation
- `lab_test` — laboratory test results per referenced standards
- `forensic_report` — failure investigation documentation
- `manufacturer_data` — manufacturer product data and technical bulletins
- `literature` — published research and guidance documents
- `expert_judgment` — documented expert analysis
- `sensor_data` — monitoring and measurement data
- `inspection_report` — third-party inspection records
- `commissioning_report` — commissioning test documentation
- `warranty_claim` — warranty claim and resolution records

## Evidence Requirement Recording

When a specification states an evidence requirement, the kernel records:

1. The type of evidence required (via submittal, test, qualification, or warranty record)
2. The specification requirement the evidence supports (via requirement linkage)
3. Timing requirements (when evidence must be provided)
4. Acceptance criteria (what constitutes passing evidence)
5. Review requirements (who reviews and approves the evidence)

## Evidence Ownership

The kernel does not store evidence artifacts. It records the specification's demand for evidence. Actual evidence documents (PDF test reports, submitted product data, inspection photos) are managed outside this kernel. The linkage between evidence artifacts and specification requirements is maintained by the intelligence layer.

## Evidence Gaps

When a specification requires a performance criterion but does not specify how compliance is to be demonstrated, the kernel records the requirement with `evidence_required: true` and `ambiguity_flag: true`, noting that the evidence method is unspecified.
