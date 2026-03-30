# Kernel-to-Runtime Map — Construction Specification Kernel

## Status: RESERVED — Not Implemented

This map is reserved for future definition of runtime hooks that will consume specification kernel data.

## Planned Runtime Consumption Patterns

When runtime systems are implemented, they are expected to:

1. **Validate records** against published schemas before processing
2. **Query by section** — retrieve all requirements, prohibitions, and submittals for a given CSI section
3. **Query by control layer** — retrieve all specification records relevant to a specific control layer
4. **Query by interface zone** — retrieve all specification records addressing a specific transition
5. **Filter by status** — select only active records for current truth
6. **Filter by ambiguity** — identify records requiring human resolution
7. **Traverse lineage** — follow revision chains to understand specification evolution

## Runtime Constraints

Future runtime systems must:

- Treat this kernel as read-only — no runtime writes to kernel data
- Respect schema version declarations — process records according to their declared version
- Honor ambiguity flags — do not auto-resolve ambiguous records
- Maintain source traceability — preserve source_ref pointers in any derived data

## Implementation Timeline

No runtime hooks are implemented in v0.1. This map will be populated when runtime integration begins.
