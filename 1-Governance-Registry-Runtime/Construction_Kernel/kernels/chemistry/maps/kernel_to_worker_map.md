# Kernel-to-Worker Map

## Purpose

Documents the relationship between the Construction Chemistry Kernel and any worker or background processing layer.

## Status

Reserved for future worker integration. No worker is implemented.

## Design Intent

- The chemistry kernel contains only static truth records.
- No background workers, job queues, or processing pipelines exist in this kernel.
- Future workers would consume kernel data as read-only input for batch operations.

## Placeholder Notes

- Workers could batch-validate chemical system records against updated schemas.
- Incompatibility scanning across large material databases could be a worker task.
- No timeline is established for worker integration.

## Constraints

- Kernel records must never contain processing logic.
- Workers must treat kernel data as immutable source truth.
- Any future worker must log results separately from kernel records.

## References

- See `kernel_map.md` for entity overview.
- See contracts for validation rules that workers would enforce.
