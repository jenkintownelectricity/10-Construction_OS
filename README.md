# Construction Runtime v0.1

**Construction_Runtime** is the execution layer for **Construction_Kernel**.

It executes workflows based on Construction_Kernel truth boundaries.

> **Construction_Runtime does not define construction truth.**
> **Construction_Runtime executes against truth boundaries defined in Construction_Kernel.**

## Architecture

```
Universal_Truth_Kernel
        ↓
Construction_Kernel
        ↓
Construction_Runtime
        ↓
Construction Applications
```

## Responsibilities

The runtime is responsible for:

- **Input ingestion** — accepting raw assembly or specification data
- **Normalization** — cleaning and standardizing input before parsing
- **Parsing** — extracting structured data from normalized input
- **Kernel-boundary validation** — ensuring parsed data respects Construction_Kernel truth
- **Assembly/spec runtime modeling** — building runtime objects from parsed data
- **Deliverable generation** — producing structured outputs (drawings, reports)
- **Runtime reporting** — logging and summarizing execution outcomes

## Runtime Layers

| Layer | Purpose |
|---|---|
| **Parsers** | Ingest, normalize, and extract structured data from raw input |
| **Adapters** | Translate Construction_Kernel concepts into runtime-usable objects |
| **Models** | Runtime data structures (assembly, geometry, material, deliverable, report) |
| **Engines** | Combine runtime objects, enforce constraints, produce buildable structures |
| **Validators** | Fail-closed validation of parsed fields, references, and runtime integrity |
| **Generators** | Produce structured deliverables (shop drawings, exports, previews) |
| **Pipeline** | Orchestrate the full runtime flow from ingestion to report |
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
python -m pytest tests/
```
