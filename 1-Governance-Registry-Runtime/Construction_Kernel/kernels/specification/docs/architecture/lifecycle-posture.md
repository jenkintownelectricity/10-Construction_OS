# Lifecycle Posture — Construction Specification Kernel

## Lifecycle Applicability

Specification requirements apply primarily at specific lifecycle stages. The shared `shared_enum_registry.json` defines eight canonical lifecycle stages: design, procurement, installation, commissioning, operation, maintenance, failure, replacement. Specification truth is most dense at the first three stages.

## Stage-Specific Specification Relevance

### Design Stage

Specification sections are authored during design. Requirements, prohibitions, and allowances are established. Standards references are selected. Performance criteria are set. This kernel records the specification facts produced at this stage.

- Relevant objects: specification_document, specification_section, requirement, prohibition, allowance, reference_standard
- Primary activity: specification authoring and coordination

### Procurement Stage

Submittal requirements and qualification requirements are exercised during procurement. Manufacturers and installers demonstrate compliance with spec requirements through submittals.

- Relevant objects: submittal_requirement, qualification_requirement, source_pointer (submittals as sources)
- Primary activity: submittal review, qualification verification

### Installation Stage

Testing requirements, warranty requirements, and field verification occur during installation. Specification requirements governing means and methods are executed.

- Relevant objects: testing_requirement, warranty_requirement, requirement (installation-specific)
- Primary activity: field testing, mock-ups, warranty issuance

### Commissioning Stage

Commissioning verifies that installed systems meet specification performance criteria. Testing requirements with `test_type: field_test` are exercised.

- Relevant objects: testing_requirement, requirement (performance verification)
- Primary activity: system performance validation

### Operation and Maintenance Stages

Specification requirements for maintenance obligations and warranty conditions remain applicable. Warranty durations and conditions defined in specs govern ongoing obligations.

- Relevant objects: warranty_requirement (ongoing), requirement (maintenance-related)
- Primary activity: warranty enforcement, maintenance per spec

### Failure and Replacement Stages

When failures occur, specification records provide the baseline against which actual performance is measured. Replacement work may trigger re-specification.

- Relevant objects: specification_revision (re-specification), requirement (original baseline)
- Primary activity: forensic comparison, re-specification

## Lifecycle Context in Records

The `lifecycle_stage` field on requirement records indicates the primary lifecycle stage where the requirement applies. This enables consumers to filter requirements by stage relevance. Requirements without a lifecycle_stage are assumed to apply broadly.

## Lifecycle and Revision Lineage

Specification revisions (addenda, RFI responses, bulletins) may occur at any lifecycle stage but are most common during design and procurement. The revision lineage model tracks these changes regardless of when they occur.
