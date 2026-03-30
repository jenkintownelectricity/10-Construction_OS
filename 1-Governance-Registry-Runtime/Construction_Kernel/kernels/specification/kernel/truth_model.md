# Truth Model — Construction Specification Kernel

## What Constitutes Specification Truth

Specification truth is an as-written fact extracted from a project specification document or referenced standard. It is not an interpretation, inference, or recommendation. Every specification truth in this kernel meets all of the following criteria:

1. **Sourced** — traces to an identifiable source document (project manual, addendum, RFI response, bulletin, or standards body publication)
2. **As-written** — recorded using the obligation language and terminology from the source
3. **Classifiable** — maps to a recognized entity type (requirement, prohibition, allowance, submittal, test, warranty, qualification)
4. **Structured** — conforms to a versioned JSON Schema with explicit required fields
5. **Immutable once active** — cannot be modified after commitment; changes create new revision records

## Truth Categories

### Specification Documents
Project manuals and their constituent parts. A specification document is the top-level container. Truth: this document exists, it covers this project, it contains these sections.

### Requirements
Statements of obligation from specification text. Truth: the specification states this requirement with this obligation level (shall/should/may) in this section for this scope of work.

### Prohibitions
Statements of what is forbidden. Truth: the specification explicitly prohibits this material, method, or condition under these circumstances.

### Allowances
Statements of what is permitted. Truth: the specification explicitly allows this alternative or substitution under these conditions.

### Submittal Requirements
Statements of what must be submitted. Truth: the specification requires this type of submittal at this time with this review requirement.

### Testing Requirements
Statements of what must be tested. Truth: the specification requires this test method with these acceptance criteria at this frequency.

### Warranty Requirements
Statements of warranty obligations. Truth: the specification requires this warranty type for this duration under these conditions.

### Qualification Requirements
Statements of who must be qualified. Truth: the specification requires this party to hold these qualifications with this minimum experience.

### Standards References
Citations to external standards. Truth: the specification cites this standard as governing this requirement. The standard's content is not truth held by this kernel.

## Truth Boundaries

Specification truth stops at the boundary of what the specification document states. It does not extend to:

- What the specifier intended but did not write
- What a standard requires beyond what the spec cites
- What industry practice suggests but the spec does not mandate
- What field conditions reveal about specification adequacy

## Truth Admission Protocol

A new specification fact enters the kernel through this protocol:

1. Source document is identified and a source_pointer record is created
2. The specification fact is extracted and mapped to the appropriate entity type
3. The record is populated with all required schema fields
4. Schema validation passes
5. The record is committed with `status: draft`
6. Upon review, status transitions to `status: active` and the record becomes immutable
