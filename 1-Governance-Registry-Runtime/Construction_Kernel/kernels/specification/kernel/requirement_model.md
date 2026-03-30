# Requirement Model — Construction Specification Kernel

## Purpose

Requirements are the most granular truth unit in the specification kernel. Each requirement captures a single obligation statement from a specification document with its obligation level, scope, and context.

## Requirement Structure

Every requirement record contains:

### Required Fields
- `requirement_id` — unique identifier (pattern: REQ-{section}-{seq})
- `title` — concise description of the requirement
- `obligation_level` — shall (mandatory), should (recommended), or may (permissive)
- `status` — draft, active, or deprecated

### Optional Context Fields
- `csi_section` — CSI section where the requirement originates
- `control_layers` — control layers this requirement serves
- `interface_zones` — interface zones this requirement addresses
- `performance_criteria` — measurable performance thresholds
- `test_method_refs` — ASTM, AAMA, or other test method citations
- `standards_refs` — governing standards citations
- `source_ref` — pointer to the source document
- `climate_context` — climate zone or exposure flag applicability
- `geometry_context` — geometric condition applicability
- `lifecycle_stage` — primary lifecycle stage
- `evidence_required` — whether compliance evidence must be provided
- `ambiguity_flag` — whether the requirement contains ambiguous language
- `notes` — supplementary context

## Obligation Levels

### Shall (Mandatory)
The requirement is a binding obligation. Non-compliance is a specification violation. Examples:
- "Membrane shall be installed in accordance with manufacturer's written instructions"
- "Insulation shall have minimum R-30 thermal resistance"

### Should (Recommended)
The requirement is a recommended practice. Deviation requires justification but is not a violation. Examples:
- "Installer should attend manufacturer's training program"
- "Seams should be tested within 24 hours of welding"

### May (Permissive)
The requirement permits an action or alternative. It establishes what is allowed, not what is required. Examples:
- "Contractor may submit alternative fastener pattern with engineering justification"
- "Membrane color may be selected by architect from manufacturer's standard range"

## Performance Criteria

Requirements with measurable thresholds record them in `performance_criteria` as key-value pairs. Examples:
- `{"min_adhesion_psi": 200}` — minimum adhesion pull-off value
- `{"max_air_leakage_cfm_per_sf": 0.04}` — maximum air leakage rate
- `{"min_r_value": 30}` — minimum thermal resistance

## Requirement Relationships

- A requirement belongs to one specification section
- A requirement may reference multiple standards and test methods
- A requirement may serve multiple control layers
- A requirement may address multiple interface zones
- A requirement is superseded via revision lineage when specifications change

## Compound Requirements

When a specification clause contains multiple obligations, each obligation is recorded as a separate requirement. A clause stating "Membrane shall be mechanically attached in the field and fully adhered at the perimeter" produces two requirements: one for field attachment, one for perimeter attachment.
