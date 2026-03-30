# Kernel-to-Worker Map — Construction Assembly Kernel

## Status: Reserved for Future

This map is reserved for documenting how worker processes interact with assembly kernel truth.

## Anticipated Worker Types

| Worker | Function | Status |
|---|---|---|
| Assembly ingestion worker | Parses assembly data from external sources into kernel schema format | Not yet implemented |
| Evidence linker | Associates evidence records with assembly objects | Not yet implemented |
| Continuity auditor | Scans assemblies for continuity requirement violations | Not yet implemented |
| Transition completeness checker | Verifies all interface zones have documented transition conditions | Not yet implemented |

## Worker Interaction Rules

1. Workers produce records conforming to kernel schemas.
2. Workers do not bypass validation or contract requirements.
3. Worker output enters the kernel through the same validation pipeline as manual entries.
4. Workers log all actions for audit trail.

## Current State

No workers are implemented. All kernel records are manually authored.
