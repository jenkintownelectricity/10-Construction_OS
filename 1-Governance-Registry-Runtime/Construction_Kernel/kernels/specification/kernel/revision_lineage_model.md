# Revision Lineage Model — Construction Specification Kernel

## Purpose

This model defines how specification revisions create lineage chains that track the evolution of specification content over time. Every change to an active specification record produces a new record linked to the original through revision lineage.

## Revision Sources

Specification revisions originate from:

- **Addenda** — formal modifications issued during bidding or pre-construction
- **Bulletins** — supplementary instructions or clarifications
- **RFI responses** — responses to requests for information that modify spec intent
- **Change orders** — contract modifications affecting specification requirements
- **Re-specifications** — complete replacement of a specification section

## Lineage Chain Structure

Each revision record contains:

- `revision_id` — unique identifier for the revision
- `document_ref` — reference to the specification document being revised
- `revision_number` — sequential revision number (1, 2, 3...)
- `effective_date` — date the revision takes effect
- `changes_summary` — description of what changed
- `supersedes` — ID of the record being superseded
- `status` — draft, active, or deprecated

## Supersession Rules

1. When a new revision supersedes an existing record, the original record's status transitions to `deprecated`
2. The new record's `supersedes` field points to the deprecated record's ID
3. Deprecated records are never deleted — they remain in the kernel as historical truth
4. Multiple records may be superseded by a single revision (e.g., an addendum that modifies several requirements)
5. A revision chain can be traversed forward and backward through `supersedes` pointers

## Lineage Integrity

- Every active record either has no `supersedes` pointer (it is the original) or points to a deprecated record
- No two active records may supersede the same deprecated record
- Circular supersession is prohibited
- Revision numbers must be monotonically increasing within a document

## Revision and Ambiguity

A revision may resolve a previously flagged ambiguity. When this occurs:

1. The original ambiguous record remains with `ambiguity_flag: true` and `status: deprecated`
2. The new record has `ambiguity_flag: false` (if the ambiguity is fully resolved)
3. The lineage chain documents the resolution path

Conversely, a revision may introduce new ambiguity. This is recorded with `ambiguity_flag: true` on the new record.

## Temporal Authority

At any point in time, the active record in a lineage chain represents current specification truth. Historical records (deprecated) provide audit trail and context but are not current obligations.

## Revision Posture

The `revision_posture` field (from `shared_enum_registry.json`) governs how records can be modified:

- `immutable` — cannot be changed; changes create new revision records
- `append_only` — new information can be added but existing content cannot be modified
- `revisable_with_audit` — changes are permitted with audit trail
- `draft` — freely editable before commitment
