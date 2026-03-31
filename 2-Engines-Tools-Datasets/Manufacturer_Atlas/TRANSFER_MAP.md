# Manufacturer Atlas — Transfer Map

**Date:** 2026-03-31
**Purpose:** Map Wave 1 artifacts to Domain OS taxonomy layers
**Origin Repo:** 10-Construction_OS
**Origin Commit:** 05a909260769de38eebe839494e2b00c277fbdff

---

## Wave 1 Artifact Inventory

| Origin Path | Target Layer | Target Path |
|------------|-------------|-------------|
| graph/atlas-primitives.ts | 000-governance-truth/090-schemas | Types remain in governance as canonical type authority |
| schemas/atlas_node.schema.json | 000-governance-truth/090-schemas | Schema is governance truth |
| schemas/atlas_edge.schema.json | 000-governance-truth/090-schemas | Schema is governance truth |
| schemas/atlas_lens.schema.json | 000-governance-truth/090-schemas | Schema is governance truth |
| schemas/assembly_constraint_set.schema.json | 000-governance-truth/090-schemas | Schema is governance truth |
| schemas/detail_graph_relation.schema.json | 000-governance-truth/090-schemas | Schema is governance truth |
| graph/manufacturer-domain-nodes.json | 100-knowledge-graph/110-atlas-nodes | Graph data is knowledge, not governance |
| graph/manufacturer-domain-edges.json | 100-knowledge-graph/120-atlas-edges | Graph data is knowledge, not governance |
| graph/integrity-report.json | 100-knowledge-graph/170-integrity | Integrity is knowledge audit |
| lenses/system-view.json | 100-knowledge-graph/130-atlas-lenses | Lenses define graph views |
| lenses/condition-view.json | 100-knowledge-graph/130-atlas-lenses | Lenses define graph views |
| lenses/product-view.json | 100-knowledge-graph/130-atlas-lenses | Lenses define graph views |
| lenses/rule-view.json | 100-knowledge-graph/130-atlas-lenses | Lenses define graph views |
| lenses/coverage-view.json | 100-knowledge-graph/130-atlas-lenses | Lenses define graph views |
| constraints/envelope-assembly-constraints.json | 000-governance-truth/080-constraint-sets | Constraints are governance truth |
| relations/detail-graph-relations.json | 100-knowledge-graph/140-detail-graph | Relations are knowledge structure |
| surface/atlas-explorer.html | 300-tools/310-manufacturer-atlas-ui | UI is a tool |
| surface/atlas-surface-contract.json | 300-tools/310-manufacturer-atlas-ui | Contract is tool-facing |
| MANUFACTURER_ATLAS_FOUNDATION_RECEIPT.md | 900-archive-immutable/910-receipts | Receipt is immutable archive |

---

## Architecture Law

FUNCTIONS CANNOT LIVE WITH GOVERNANCE

- Schemas and type definitions -> 000-governance-truth
- Graph data and lenses -> 100-knowledge-graph
- UI surfaces and tools -> 300-tools
- Receipts and audits -> 900-archive-immutable

---

## Dependency Direction

```
000-governance-truth     (canonical authority)
  ↓
100-knowledge-graph      (organized truth)
  ↓
200-engines              (deterministic logic)
  ↓
300-tools                (operator surfaces)
  ↓
400-adapters             (external bridges)
  ↓
900-archive-immutable    (append-only lineage)
```
