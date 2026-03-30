# AI Readiness Posture — Construction Specification Kernel

## Design for Machine Consumption

This kernel is designed from the ground up for machine-readable consumption. Every specification fact is stored as structured data conforming to JSON Schema (2020-12), enabling reliable parsing, validation, and querying by AI systems, automation tools, and data pipelines.

## Structured Record Format

All specification entities use JSON with:

- **Explicit schemas** — every object type has a corresponding JSON Schema with `additionalProperties: false`
- **Required fields** — core identity and classification fields are always present
- **Controlled vocabularies** — enum fields draw from the shared registries (shared_enum_registry.json, shared_taxonomy.json)
- **Typed values** — no untyped free-text fields for structured data; notes fields are reserved for supplementary context
- **Consistent identifiers** — all entities use predictable ID patterns for cross-referencing

## Schema Validation as Quality Gate

Records that fail schema validation are rejected before entry. This guarantees that any record in the kernel can be parsed by a conforming consumer without encountering unexpected fields, missing required data, or unrecognized enum values.

## No Execution Leakage

The kernel contains data and metadata only. It does not contain:

- Executable code or scripts
- API endpoint definitions
- Database queries or stored procedures
- Workflow definitions or state machines
- Conditional logic that should run at consumption time

AI systems consume kernel data as input to their own reasoning processes. The kernel never prescribes how that reasoning should operate.

## Pointer-Based Relationships

Cross-references between entities use explicit pointer fields (IDs and reference strings) rather than embedded objects. This enables AI systems to traverse relationships without deep nesting and to resolve references selectively based on their needs.

## Ambiguity Transparency

The `ambiguity_flag` field provides a machine-readable signal that a specification fact requires human review. AI systems can filter, prioritize, or route ambiguous records without attempting to resolve ambiguity themselves.

## Versioned and Frozen

Schema versions are frozen per baseline. AI systems consuming kernel data can rely on schema stability within a baseline version. Schema changes produce new version numbers, allowing consumers to adapt.

## Consumption Patterns

AI systems are expected to:

1. Validate records against published schemas before processing
2. Respect `ambiguity_flag` as a halt signal for automated interpretation
3. Use `source_ref` pointers for provenance verification
4. Reference shared registries for enum expansion and context
5. Treat `status: deprecated` records as historical, not current
