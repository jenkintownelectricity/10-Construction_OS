# AI Readiness Map — Construction Specification Kernel

## Readiness Assessment

This map evaluates the kernel's readiness for consumption by AI systems across key dimensions.

## Schema Structure — READY

- All entities have JSON Schema (2020-12) definitions
- `additionalProperties: false` prevents unexpected fields
- Required fields are explicit on every schema
- Enum values are controlled via shared registries
- Schema version is a const field enabling version detection

## Data Quality Signals — READY

- `ambiguity_flag` provides machine-readable ambiguity signal
- `status` field enables filtering to current truth (active only)
- `obligation_level` provides structured obligation classification
- `source_ref` enables provenance verification
- `evidence_required` flags records needing compliance evidence

## Relationship Traversal — READY

- Entities reference each other via ID pointers
- No deeply nested objects requiring recursive parsing
- Clear parent-child relationships (document > section > requirement)
- Supersession chains traversable via `supersedes` pointers
- Shared registry references resolvable against canonical files

## Vocabulary Control — READY

- Control layer IDs from `control_layers.json`
- Interface zone IDs from `interface_zones.json`
- Lifecycle stages from `shared_enum_registry.json`
- Climate and geometry contexts from shared enums
- Obligation levels (shall/should/may) as explicit enum

## Query Patterns Supported

| Query | Fields Used |
|---|---|
| "All requirements for section 07 54 00" | csi_section |
| "All mandatory requirements" | obligation_level = "shall" |
| "All ambiguous records" | ambiguity_flag = true |
| "Requirements at roof-to-wall transition" | interface_zones contains "roof_to_wall" |
| "Climate-dependent requirements" | climate_context is not null |
| "All active testing requirements" | test_type + status = "active" |
| "Requirements serving air control layer" | control_layers contains "air_control" |
| "Warranty requirements over 10 years" | warranty_type + duration_years > 10 |

## Consumption Constraints

- AI systems must validate records against schemas before processing
- AI systems must not auto-resolve `ambiguity_flag: true` records
- AI systems must treat `status: deprecated` as historical, not current
- AI systems must not write back to the kernel
- AI systems must preserve source_ref attribution in derived outputs

## Not Yet AI-Ready

- No full-text search index (structured fields only)
- No pre-computed embeddings for semantic search
- No automated change detection or notification hooks
- No streaming or event-based update protocol
