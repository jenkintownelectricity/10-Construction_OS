# Revision Lineage Model

## Purpose

Defines how the Scope Kernel tracks changes to scope records over time. Every modification to scope truth creates a lineage entry that preserves the history of what was defined, when, and why.

## Lineage Principles

1. **No destructive updates.** Scope records are never overwritten in place. Changes create new versions; prior versions are deprecated.
2. **Every change has a reason.** Lineage entries record the rationale for the change.
3. **Traceability is mandatory.** Any current scope record can be traced back through its revision history to the original definition.

## Lineage Record Structure

Each revision in the lineage contains:
- **Revision ID**: Unique identifier for this revision
- **Object reference**: The scope object being revised
- **Prior version reference**: Link to the previous version (null for initial creation)
- **Change type**: `created`, `modified`, `deprecated`, `reinstated`
- **Change summary**: Human-readable description of what changed
- **Changed by**: Author or system that made the change
- **Change date**: Timestamp of the change
- **Reason**: Why the change was made

## Change Types

### Created
Initial definition of a scope record. No prior version exists.

### Modified
A scope record's content has changed. The prior version is deprecated and a new active version is created. Fields that may trigger a modification:
- Inclusions or exclusions changed
- Trade responsibility reassigned
- Sequencing dependencies modified
- Inspection or commissioning steps added or removed

### Deprecated
A scope record is no longer current. It is retained for lineage but no longer authoritative. Reasons include:
- Superseded by a new version
- Scope item removed from project
- Trade responsibility restructured

### Reinstated
A previously deprecated record is returned to active status. This is rare and requires explicit justification.

## Lineage Integrity Rules

1. Active records must have exactly one lineage chain leading to their creation.
2. Deprecated records must reference the active record that supersedes them.
3. Lineage gaps (records with no creation entry) are flagged as data integrity issues.
4. Lineage is append-only. Lineage entries are never modified or deleted.

## Relationship to Status Field

The `status` field on scope objects (`draft`, `active`, `deprecated`) reflects the current state. The revision lineage model records the full history of state transitions.
