# Object Model Overview — Construction Specification Kernel

## Core Objects

The specification kernel is built around twelve core object types. Each has a corresponding JSON Schema in `schemas/` with `additionalProperties: false` and explicit required fields.

### specification_document

The top-level container representing a project specification document. Contains metadata (project reference, CSI division, status) and references to its constituent sections. Tracks revision history at the document level.

### specification_section

A CSI-formatted section within a specification document (e.g., 07 52 00 — Modified Bituminous Membrane Roofing). Sections are the primary organizational unit and contain references to requirements, prohibitions, allowances, submittals, qualifications, warranties, and testing requirements. Each section maps to one or more control layers from the shared registry.

### requirement

A specification statement with an obligation level. Requirements are the most granular truth unit in the kernel. Each requirement has:
- `obligation_level` — shall (mandatory), should (recommended), or may (permissive)
- Optional performance criteria, test method references, standards references
- Optional climate context, geometry context, and lifecycle stage applicability
- `ambiguity_flag` — set when the requirement contains ambiguous language

### prohibition

An explicit statement forbidding a material, method, condition, or configuration. Prohibitions carry conditions (when applicable) and source references.

### allowance

An explicit statement permitting an alternative or substitution. Allowances may be conditional and carry source references.

### source_pointer

A traceable reference to the originating document that establishes a specification fact. Source types include project manuals, addenda, RFIs, bulletins, and standards body publications.

### reference_standard

A citation to a governing standard or code (IBC, ASTM, AAMA, NFPA, ASHRAE). Contains the standard identifier, title, issuing body, and relevance description. Never contains the standard's text.

### submittal_requirement

A required submittal for review. Types: product_data, shop_drawing, sample, test_report, certificate, warranty, mix_design. Includes timing and review requirements.

### qualification_requirement

A required qualification for a party involved in the work. Types: manufacturer, installer, testing_agency, inspector. Specifies minimum experience and required certifications.

### warranty_requirement

A warranty obligation. Types: manufacturer_standard, manufacturer_extended, system_warranty, nol (no-dollar-limit), workmanship. Specifies duration in years and conditions.

### testing_requirement

A required test. Types: field_test, lab_test, mock_up, preconstruction. References test methods, acceptance criteria, timing, and frequency.

### specification_revision

A revision record creating lineage between specification versions. Tracks revision number, effective date, changes summary, and supersession relationships.

## Relationships

- A `specification_document` contains one or more `specification_section` records
- A `specification_section` references multiple `requirement`, `prohibition`, `allowance`, `submittal_requirement`, `qualification_requirement`, `warranty_requirement`, and `testing_requirement` records
- Every truth-bearing object references at least one `source_pointer`
- `requirement` records may reference `reference_standard` records
- `specification_revision` records link superseded and superseding records
- Control layer and interface zone linkages use IDs from the shared registries
