# Manufacturer Atlas

**Domain:** Building Envelope
**Classification:** MANUFACTURER_KNOWLEDGE_GRAPH
**Status:** FOUNDATION (Wave 1)
**Parent:** 2-Engines-Tools-Datasets
**Authority:** Manufacturer-published system truth

---

## Purpose

Manufacturer Atlas is the system knowledge graph for building envelope
manufacturer data within Construction OS.

It provides the structured truth source for:
- Living Details
- Detail Graph resolution
- Assembly constraint validation
- Fail-closed bidding
- Governed installation verification

---

## Architecture

```
Manufacturer Atlas (knowledge graph)
  ├── graph/         Atlas node/edge primitives + domain graph
  ├── schemas/       JSON Schema definitions
  ├── lenses/        Atlas view lens definitions
  ├── constraints/   Assembly constraint sets
  ├── relations/     Detail graph relation layer
  └── surface/       Atlas navigation surface + view contract
```

---

## Relationship to Construction Atlas

Manufacturer Atlas prepares the system knowledge graph and assembly
constraint sets that will later feed Construction Atlas OMNI View
for visual detail resolution.

Manufacturer Atlas does NOT duplicate any CAD drawing engine.
Construction_Atlas remains READ ONLY from this wave.

---

## Honesty Discipline

Every node includes a status classification:
- `grounded` — verified manufacturer truth
- `derived` — logically derived from grounded data
- `scaffold` — placeholder structure, not yet verified
- `deferred` — known gap, intentionally deferred
- `unverified` — data present but not yet validated

Scaffold and grounded truth are never mixed silently.

---

## Wave 1 Scope

This wave builds truth structures only:
- Atlas graph primitives
- Manufacturer domain graph
- Atlas lenses
- Assembly constraint sets
- Detail graph relation layer
- Navigation surface

This wave does NOT build:
- CAD projection engines
- Revit/AutoCAD plugins
- Computer vision validation
- Signal bus runtime
- Detail compilers
- API servers
