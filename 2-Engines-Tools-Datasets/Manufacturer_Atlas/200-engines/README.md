# 200-engines

**Purpose:** Deterministic logic consuming truth (000) and graph (100).

## Subdirectories

| Directory | Purpose |
|-----------|----------|
| 210-manufacturer-atlas-engine | Core atlas traversal and query logic |
| 220-assembly-constraint-resolver | Resolves assembly constraint sets against conditions |
| 230-detail-graph-resolver | Resolves detail graph paths from condition to detail |
| 240-compatibility-engine | Product compatibility validation |
| 250-coverage-engine | Coverage analysis and gap detection |
| 260-validation-engine | Schema and integrity validation |

## Dependency Rules

- **Reads from:** 000-governance-truth, 100-knowledge-graph
- **MUST NOT write to:** 000 or 100
- **Consumed by:** 300-tools, 400-adapters

## Status

All engine directories are placeholders for future wave implementation.
This wave establishes the taxonomy structure only.
