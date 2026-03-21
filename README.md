# Construction Runtime v0.2 — Hardened Execution Engine

**Construction_Runtime** is the deterministic execution layer for **Construction_Kernel**.

It executes workflows based on Construction_Kernel truth boundaries.

> **Construction_Runtime is the execution layer.** It consumes Atlas context for artifact generation.
> **Construction_Runtime does not define construction truth.**
> **Construction_Runtime executes against truth boundaries defined in Construction_Kernel.**

## Construction OS Core Architecture (FROZEN)

```
Universal_Truth_Kernel
├── ValidKernel_Geometry_Kernel
├── ValidKernel-Governance
└── Construction_Kernel
     ├── Construction_Atlas (formerly Construction_Atlas_UI)
     │        ↓
     Construction_Runtime               ← YOU ARE HERE
              ↓
     Construction_Application_OS
```

> **Architecture Status:** FROZEN
> **Construction_Atlas** (formerly Construction_Atlas_UI) provides spatial construction context that the Runtime consumes for artifact generation.
> **UI Authority:** Construction_Application_OS is the sole UI surface of Construction OS.

## Explicit Dependencies

| Dependency | Relationship |
|------------|-------------|
| **Construction_Kernel** | Executes against truth boundaries |
| **Construction_Atlas** | Consumes spatial context for artifact generation |

## Pipeline Architecture

```
Universal_Truth_Kernel
        ↓
Construction_Kernel
        ↓
Construction_Runtime (v0.2)
        ↓
Construction_Application_OS
```

## v0.2 Pipeline

```
INPUT
  → Parse
  → Normalize
  → Structural Validation
  → Domain Validation
  → Geometry Engine
  → DrawingInstructionSet
  → Generation Validation
  → DXF Writer
  → SVG Writer
  → DeliverableModel
  → Audit Log
```

## Responsibilities

- **Input ingestion** — accepting raw assembly or specification data
- **Normalization** — cleaning and standardizing input before parsing
- **Parsing** — extracting structured data from normalized input
- **Multi-layer validation** — structural, domain, and generation validation (fail-closed)
- **Contract enforcement** — JSON schema contracts at every pipeline stage
- **Geometry engine** — deterministic layout with provenance metadata
- **Drawing instruction generation** — canonical intermediate representation
- **DXF + SVG dual output** — both derive from DrawingInstructionSet
- **Deliverable packaging** — versioned multi-format output
- **Audit logging** — append-only structured event trail

## Runtime Layers

| Layer | Purpose |
|---|---|
| **Parsers** | Ingest, normalize, and extract structured data from raw input |
| **Adapters** | Translate Construction_Kernel concepts into runtime-usable objects |
| **Models** | Runtime data structures (assembly, geometry, material, deliverable, drawing instruction, report) |
| **Validators** | Multi-layer fail-closed validation: structural, domain, generation |
| **Contracts** | JSON schema contracts for every pipeline stage |
| **Geometry Engine** | Deterministic layout with provenance-tracked derived dimensions |
| **Engines** | Combine runtime objects, enforce constraints, produce buildable structures |
| **Generators** | DXF writer + SVG writer consuming DrawingInstructionSet only |
| **Pipeline** | Orchestrate the full runtime flow from ingestion to audit report |
| **Standards** | Error codes, layer standards, SVG standards |
| **Rules** | Geometry rules for panel layout, spacing, overlap detection |
| **Apps** | Lightweight entry points for specific use cases |

## Applications

1. **Assembly Parser App** — parses assembly input through the full runtime pipeline
2. **Spec Intelligence App** — parses specification text and extracts structured intelligence

## Running

```bash
# Assembly Parser App
python -m apps.assembly_parser_app.main

# Spec Intelligence App
python -m apps.spec_intelligence_app.main
```

## Testing

```bash
python -m pytest tests/ -v
```

Test categories:
- `tests/parser_tests/` — parser normalization and extraction
- `tests/engine_tests/` — assembly engine and constraint engine
- `tests/pipeline_tests/` — pipeline happy path and failure
- `tests/mutation/` — fail-closed mutation tests
- `tests/golden/` — golden fixture tests against known inputs
- `tests/snapshots/` — output structure stability tests
