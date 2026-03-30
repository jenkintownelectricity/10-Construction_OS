# Kernel-to-Worker Map — Construction Material Kernel

## Status: Stub

No worker processes currently exist. This map will be populated when automated data processing workers are implemented.

## Planned Worker Types

| Worker | Purpose | Status |
|---|---|---|
| TDS Ingestion Worker | Parse manufacturer TDS documents into draft records | Not implemented |
| Schema Validation Worker | Validate incoming records against schemas | Not implemented |
| Evidence Linking Worker | Verify and link evidence references | Not implemented |
| Compatibility Matrix Builder | Generate pairwise compatibility reports | Not implemented |
| Revision Lineage Tracker | Maintain revision chains on record updates | Not implemented |

## Worker Design Constraints

1. Workers create draft records only; activation requires human review
2. Workers must log all actions for audit trail
3. Workers must respect fail-closed governance
4. Workers must not modify active or deprecated records
