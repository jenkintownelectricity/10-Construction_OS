# Manufacturer Domain OS

**Domain:** Building Envelope Manufacturer
**Classification:** MANUFACTURER_DOMAIN_OPERATING_SYSTEM
**Version:** v1.0
**Status:** FROZEN

---

## Taxonomy

```
Manufacturer_Atlas/
├── 000-governance-truth/     Canonical manufacturer authority (FROZEN)
│   ├── 010-manufacturers/
│   ├── 020-systems/
│   ├── 030-products/
│   ├── 040-rules/
│   ├── 050-assemblies/
│   ├── 060-conditions/
│   ├── 070-details/
│   ├── 080-constraint-sets/
│   └── 090-schemas/
├── 100-knowledge-graph/     Atlas graph and detail graph structures
│   ├── 110-atlas-nodes/
│   ├── 120-atlas-edges/
│   ├── 130-atlas-lenses/
│   ├── 140-detail-graph/
│   ├── 150-resolution-patterns/
│   ├── 160-coverage-models/
│   └── 170-integrity/
├── 200-engines/             Deterministic logic
│   ├── 210-manufacturer-atlas-engine/
│   ├── 220-assembly-constraint-resolver/
│   ├── 230-detail-graph-resolver/
│   ├── 240-compatibility-engine/
│   ├── 250-coverage-engine/
│   └── 260-validation-engine/
├── 300-tools/               Operator-facing tools
│   ├── 310-manufacturer-atlas-ui/
│   ├── 320-detail-inspector/
│   ├── 330-coverage-explorer/
│   ├── 340-system-browser/
│   ├── 350-rule-browser/
│   └── 360-operator-workstation/
├── 400-adapters/            External system bridges
│   ├── 410-omni-view-bridge/
│   ├── 420-cad-export/
│   ├── 430-bim-export/
│   ├── 440-importers/
│   ├── 450-signal-emitters/
│   ├── 460-projection-contracts/
│   └── 470-external-connectors/
└── 900-archive-immutable/   Append-only lineage archive
    ├── 910-receipts/
    ├── 920-audits/
    ├── 930-phase-logs/
    ├── 940-migration-notes/
    └── 950-frozen-snapshots/
```

---

## Architecture Law

**FUNCTIONS CANNOT LIVE WITH GOVERNANCE**

```
000 → 100 → 200 → 300 → 400
              ↓
             900
```

Lower layers consume higher layers. Higher layers never overwrite lower.

---

## Governance

- Constitution: DOMAIN_OS_CONSTITUTION_v1.0.md
- Layer Boundaries: LAYER_BOUNDARY_RULES_v1.0.md
- Versioning: VERSIONING_RULES_v1.0.md
- Change Protocol: THAW_REFREEZE_PROTOCOL_v1.0.md

---

## Current State

- **000-governance-truth:** FROZEN v1.0 — 6 schemas, 3 constraint sets
- **100-knowledge-graph:** 27 nodes, 36 edges, 5 lenses, 3 detail graph paths
- **200-engines:** Taxonomy established (implementation deferred)
- **300-tools:** Atlas explorer surface active
- **400-adapters:** Taxonomy established (implementation deferred)
- **900-archive-immutable:** Wave 1 receipt + migration note archived
