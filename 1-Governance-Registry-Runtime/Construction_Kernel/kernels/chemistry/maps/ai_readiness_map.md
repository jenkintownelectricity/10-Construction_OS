# AI Readiness Map

## Purpose

Documents the machine-readability posture of the Construction Chemistry Kernel and confirms that no execution leakage exists.

## Machine-Readability Status

| Criterion | Status | Notes |
|---|---|---|
| All schemas are JSON Schema 2020-12 | Complete | Every entity has a validating schema with `additionalProperties: false`. |
| All records are JSON | Complete | No prose-only records. All data is structured and parseable. |
| Enum values are consistent | Complete | Chemistry families, status, and type enums are standardized across schemas. |
| Cross-references use string IDs | Complete | No embedded objects. All references are resolvable by ID lookup. |
| Contracts define validation rules | Complete | Five contracts cover the primary entity types. |
| Evidence traceability | Complete | Evidence references link claims to external lab tests and manufacturer data. |

## No Execution Leakage

| Check | Result |
|---|---|
| No executable code in schemas | Confirmed |
| No API endpoints defined | Confirmed |
| No runtime logic in contracts | Confirmed |
| No prompt injection vectors in records | Confirmed |
| No embedded scripts in example files | Confirmed |
| No dynamic evaluation or templating | Confirmed |

## AI Consumption Patterns

- **Schema validation:** AI systems can validate records against JSON Schema without custom logic.
- **Lookup by ID:** All entities are addressable by their primary ID field.
- **Filtering by enum:** Chemistry family, system type, cure type, and status support direct filtering.
- **Relationship traversal:** References between entities enable graph-style queries.
- **Natural language grounding:** Titles and notes fields provide human-readable context for AI responses.

## Data Quality for AI

- Required fields ensure minimum viable records.
- Enum constraints prevent free-text drift in classification fields.
- Schema enforcement prevents undocumented field proliferation.
- Evidence references support AI systems that need to cite sources.

## Limitations

- Climate context in degradation mechanisms uses a free-form object (not strictly typed).
- Evidence records are external; AI systems must handle missing evidence gracefully.
- No semantic versioning on individual records; only schema-level versioning exists.

## Conclusion

The Construction Chemistry Kernel is fully machine-readable, schema-validated, and free of execution leakage. It is ready for consumption by AI assistants, intelligence layers, and automated validation pipelines.
