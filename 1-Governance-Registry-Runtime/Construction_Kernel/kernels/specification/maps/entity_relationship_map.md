# Entity Relationship Map — Construction Specification Kernel

## Core Entity Relationships

### specification_document (1) --contains--> (many) specification_section
A specification document contains one or more specification sections. Each section belongs to one document.

### specification_section (1) --contains--> (many) requirement
A section contains multiple requirements. Each requirement belongs to one section (identified by csi_section).

### specification_section (1) --contains--> (many) prohibition
A section may contain prohibitions defining what is forbidden.

### specification_section (1) --contains--> (many) allowance
A section may contain allowances defining what is permitted.

### specification_section (1) --contains--> (many) submittal_requirement
A section specifies what submittals are required.

### specification_section (1) --contains--> (many) qualification_requirement
A section specifies who must be qualified and how.

### specification_section (1) --contains--> (many) warranty_requirement
A section specifies warranty obligations.

### specification_section (1) --contains--> (many) testing_requirement
A section specifies required tests and acceptance criteria.

### requirement (many) --references--> (1) source_pointer
Every requirement traces to a source document. Multiple requirements may share a source.

### requirement (many) --cites--> (many) reference_standard
Requirements may cite multiple standards. Standards may be cited by multiple requirements.

### requirement (1) --may have--> (many) requirement_condition
A requirement may have conditions (climate, geometry, substrate, exposure, code_trigger) that modify its applicability.

### specification_revision (many) --revises--> (1) specification_document
Revisions modify specification documents. A document may have multiple revisions.

### specification_revision (1) --supersedes--> (1) specification_revision
Each revision may supersede a previous revision, creating a lineage chain.

## Shared Registry Linkages

### specification_section --maps to--> control_layers.json
Sections declare which control layers they serve via `control_layers_served`.

### requirement --maps to--> control_layers.json
Requirements declare which control layers they address via `control_layers`.

### requirement --maps to--> interface_zones.json
Requirements declare which interface zones they address via `interface_zones`.

### requirement --maps to--> shared_enum_registry.json
Requirements use lifecycle_stage, climate_context, and geometry_context from shared enums.

## Cardinality Summary

| Relationship | Cardinality |
|---|---|
| document to section | 1:many |
| section to requirement | 1:many |
| section to prohibition | 1:many |
| section to allowance | 1:many |
| requirement to source_pointer | many:1 |
| requirement to reference_standard | many:many |
| requirement to requirement_condition | 1:many |
| revision to document | many:1 |
| revision to revision (supersedes) | 1:1 |
