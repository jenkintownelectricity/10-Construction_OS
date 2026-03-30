# Revision Lineage Model — Construction Material Kernel

## Purpose

This model governs how material records evolve over time. Active records are immutable. Changes produce new revision records with lineage pointers to the superseded record. No record is ever deleted.

## Record Lifecycle States

| Status | Mutable | Description |
|---|---|---|
| draft | Yes | Under preparation; may be edited freely |
| active | No | Committed and immutable; canonical truth |
| deprecated | No | Superseded by a newer revision; retained for lineage |

## State Transitions

```
draft ──(commit)──> active ──(supersede)──> deprecated
                                │
                                └──> new draft ──(commit)──> active (new revision)
```

- **draft to active**: Record passes schema validation, evidence check, and review
- **active to deprecated**: A new revision supersedes this record
- **deprecated records persist**: Never deleted; available for lineage queries

## Lineage Fields

Each record includes optional lineage fields:

| Field | Description |
|---|---|
| revision | Revision number (integer, starts at 1) |
| supersedes | ID of the record this revision replaces |
| superseded_by | ID of the record that replaced this one |
| revision_date | Date of this revision |
| revision_reason | Brief description of why the revision was made |

## Lineage Rules

1. A new revision must reference the record it supersedes
2. The superseded record's `superseded_by` field is updated to point to the new revision
3. Only one active revision of a given material fact exists at any time
4. Lineage chains are unbroken — every deprecated record points forward
5. Draft records do not have lineage fields until committed

## Lineage Query Patterns

| Query | Returns |
|---|---|
| Current value of property X for material Y | Active revision only |
| History of property X for material Y | Full lineage chain, ordered by revision |
| What changed in revision N | Diff between revision N and N-1 |
| Why was record Z deprecated | Revision reason on the superseding record |

## Revision Triggers

- Updated manufacturer TDS with new property values
- New laboratory test data superseding older data
- Correction of data entry errors (with reason documented)
- Standards revision changing test method reference
- Evidence quality upgrade (e.g., lab data replacing TDS-only data)

## Governance

Revision lineage is enforced at the data entry layer. No system may modify an active record in place. All changes flow through the draft-commit-supersede cycle.
