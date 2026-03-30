# Kernel-to-Runtime Map — Construction Material Kernel

## Status: Stub

No runtime layer currently exists. This map will be populated when a runtime consumption layer is implemented.

## Planned Runtime Integration Points

| Integration Point | Description | Status |
|---|---|---|
| Material property query API | REST or GraphQL endpoint for property lookup | Not implemented |
| Compatibility check service | Real-time compatibility validation | Not implemented |
| Schema validation service | Runtime schema validation for ingested records | Not implemented |
| Evidence verification service | Verify evidence pointer validity | Not implemented |

## Runtime Design Constraints

1. Runtime layer reads from kernel; never writes to active records
2. All runtime queries must pass schema validation
3. Runtime responses must include record status and evidence references
4. Fail-closed behavior: missing data returns explicit "not found," never defaults

## Prerequisites

- Stable kernel baseline with frozen seam contracts
- API schema derived from frozen seam definitions
- Authentication and authorization model for kernel access
- Audit logging for all runtime queries
