# Kernel-to-Assistant Map — Construction Specification Kernel

## Status: RESERVED — Not Implemented

This map is reserved for future definition of AI assistant interfaces that will consume specification kernel data.

## Planned Assistant Capabilities

When assistant interfaces are implemented, they are expected to support:

1. **Specification Lookup** — retrieve requirements, prohibitions, and submittals by section
2. **Ambiguity Reporting** — present flagged ambiguities for human resolution
3. **Interface Gap Analysis** — identify specification gaps at interface zones
4. **Revision History** — present specification evolution through revision lineage
5. **Standards Cross-Reference** — show which standards govern which requirements
6. **Compliance Checklist Generation** — produce requirement checklists from active spec records

## Assistant Constraints

Future assistants must:

- Present specification facts as-written without interpretation
- Clearly indicate ambiguity flags to users
- Distinguish between mandatory (shall), recommended (should), and permissive (may) requirements
- Never present deprecated records as current without clear labeling
- Attribute all facts to their source pointers

## Implementation Timeline

No assistant hooks are implemented in v0.1. This map will be populated when assistant interfaces are designed.
