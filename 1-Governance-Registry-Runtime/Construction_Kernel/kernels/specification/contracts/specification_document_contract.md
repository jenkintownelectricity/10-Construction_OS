# Specification Document Contract

## Entity: specification_document

## Consumer Guarantees

Any consumer reading a specification_document record from this kernel can rely on:

1. **Identity** — `document_id` is unique and stable. It never changes after commitment.
2. **Project reference** — `project_ref` identifies the project this document belongs to.
3. **Division** — `csi_division` is always present and identifies the CSI division.
4. **Status** — `status` is one of: active, draft, deprecated. Active documents represent current truth.
5. **Schema compliance** — the record conforms to `specification_document.schema.json` with `additionalProperties: false`.

## Validation Rules

- `schema_version` must be "v1"
- `document_id` must be a non-empty string
- `title` must be a non-empty string
- `status` must be one of the defined enum values
- `revision_history` entries, if present, conform to the nested schema

## Immutability

Once a specification_document reaches `status: active`, its core fields (document_id, title, project_ref, csi_division) are immutable. Status transitions are permitted only from draft to active, or from active to deprecated.

## Relationship Guarantees

- `sections` array, if present, contains valid specification_section IDs
- `revision_history` entries are chronologically ordered

## What This Contract Does NOT Guarantee

- Completeness of section references (sections may be added incrementally)
- Existence of referenced sections (they may be in draft or not yet created)
- Project-level metadata beyond project_ref (project name, location, etc.)
