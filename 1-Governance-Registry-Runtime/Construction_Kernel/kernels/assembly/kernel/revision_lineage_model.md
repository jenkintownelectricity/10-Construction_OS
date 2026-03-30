# Revision Lineage Model — Construction Assembly Kernel

## Purpose

Defines how assembly records track their revision history, supersession chains, and authoring provenance. The kernel uses append-only revision: records are versioned, never overwritten.

## Lineage Object

From the shared taxonomy, each kernel record may include a `lineage` object:

```json
{
  "lineage": {
    "supersedes": "ASSY-ROOF-TPO-001-v1",
    "superseded_by": null,
    "revision": "v2",
    "created": "2026-01-15",
    "last_modified": "2026-03-10"
  }
}
```

## Revision Postures

From `shared_enum_registry.json#revision_postures`:

| Posture | Meaning | Typical Use |
|---|---|---|
| immutable | Cannot be changed after creation | Tested assembly records with certified results |
| append_only | New versions may be added; old versions are preserved | Active assembly system configurations |
| revisable_with_audit | May be revised with full audit trail | Draft assembly records under development |
| draft | Freely editable; not yet committed as truth | New records being authored |

## Supersession Rules

1. When an assembly record is revised, the new record includes `supersedes` pointing to the previous version ID.
2. The previous record is updated to set `superseded_by` pointing to the new version and `status` changed to `deprecated`.
3. Both records remain in the kernel. Old records are never deleted.
4. At any point in time, exactly one version of a record should have `status: active`.

## Revision Triggers

Assembly records are revised when:
- A tested assembly record provides new performance data affecting the configuration
- A field observation reveals the as-built condition differs from the as-designed record
- A standards update changes compliance requirements
- A component substitution changes a layer's material reference
- An error is discovered in the original record

## Lineage Chains

For records with multiple revisions, the supersession chain is traversable:

```
ASSY-ROOF-TPO-001-v1  (deprecated, superseded_by: v2)
    -> ASSY-ROOF-TPO-001-v2  (deprecated, superseded_by: v3)
        -> ASSY-ROOF-TPO-001-v3  (active)
```

## Tested Assembly Record Immutability

Tested assembly records use `immutable` revision posture. A test result cannot be retroactively changed. If a test is re-run with different results, a new tested assembly record is created, and the assembly system record may be revised to reference the updated test.

## Audit Trail

Every revision should include:
- The date of revision (`last_modified`)
- The reason for revision (in `notes`)
- The previous version reference (`supersedes`)

The kernel does not track who made a change (author identity). Author attribution, if needed, is managed by the version control system (git) rather than the kernel data model.
