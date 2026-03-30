# Revision Lineage Model

## Purpose

Defines how chemistry records maintain revision history and lineage. No record is ever deleted; deprecated records are preserved with full traceability.

## Lineage Fields

Every chemistry record may carry these lineage fields:
- **created_date**: ISO 8601 date when the record was first created
- **updated_date**: ISO 8601 date of last modification
- **version**: Record version number (integer, starting at 1)
- **supersedes**: ID of the record this one replaces (if any)
- **superseded_by**: ID of the record that replaces this one (if deprecated)
- **deprecation_reason**: Text explanation of why the record was deprecated

## Status Transitions

```
draft ──(evidence review)──→ active ──(superseded)──→ deprecated
                               │
                               └──(invalidated)──→ deprecated
```

### draft → active
- Requires: at least one evidence reference at Tier 1-3
- Requires: schema validation passes
- Requires: no conflicting active record for the same chemistry fact

### active → deprecated
- Requires: deprecation_reason
- Requires: superseded_by reference (if a replacement exists)
- Effect: record remains queryable but flagged as not current truth

## Lineage Rules

1. **No deletion.** Records are never removed from the kernel. Deprecated records remain for historical traceability.
2. **Supersession chain.** When a record is superseded, the old record's `superseded_by` points to the new record, and the new record's `supersedes` points to the old.
3. **Version increment.** Minor corrections to an active record increment the version number and update `updated_date`. The record retains its ID.
4. **Breaking changes.** If a correction changes the fundamental chemistry fact (e.g., changing incompatibility type), a new record is created and the old is deprecated.
5. **Evidence update.** Adding new evidence to an active record is a version increment, not a new record.

## Query Behavior

- Default queries return only `active` records
- Historical queries may include `deprecated` records with explicit flag
- Lineage chain queries follow `supersedes`/`superseded_by` references
