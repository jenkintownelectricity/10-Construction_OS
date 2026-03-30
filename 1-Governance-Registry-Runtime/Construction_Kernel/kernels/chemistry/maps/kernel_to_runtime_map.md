# Kernel-to-Runtime Map

## Purpose

Documents the relationship between the Construction Chemistry Kernel and any runtime execution layer.

## Status

Reserved for future runtime integration. No runtime is implemented.

## Design Intent

- The chemistry kernel contains only static truth records.
- No executable code, API endpoints, or runtime logic exists in this kernel.
- Future runtime integration would consume kernel data as read-only input.

## Placeholder Notes

- Runtime consumers would validate field conditions against cure mechanism constraints.
- VOC compliance checks could be implemented as runtime queries against chemical system records.
- No timeline is established for runtime integration.

## Constraints

- Kernel records must never contain execution logic.
- Runtime layers must treat kernel data as immutable during a session.
- Any future runtime must read from validated, schema-compliant records only.

## References

- See `kernel_map.md` for entity overview.
- See contracts for validation rules that a runtime would enforce.
