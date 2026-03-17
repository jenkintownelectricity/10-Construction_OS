# REPO_MANIFEST — Construction_Runtime

## Identity

- **Repo Name:** Construction_Runtime
- **Purpose:** Construction execution engine aligned to Construction_Kernel. Executes against applied construction truth; does not originate or redefine truth.
- **Stack Layer:** Layer 6 — Domain Runtime
- **Authority:** v0.2
- **Branch:** claude/harden-kernel-security-dO723 (from claude/hardened-runtime-scaffold-zFniR)

## Owns

- v0.2 pipeline: parse → normalize → structural validate → domain validate → geometry engine → DrawingInstructionSet → generation validate → DXF/SVG → DeliverableModel → audit
- Contract schemas (6 JSON schemas): assembly_input, runtime_assembly, spec_input, runtime_spec, drawing_instruction, deliverable
- Structural, domain, and generation validators (three-stage, fail-closed)
- Canonical error taxonomy: 62 codes across 11 categories
- DrawingInstructionSet: canonical intermediate representation; sole input to all generation
- Deterministic geometry engine
- DXF writer and SVG writer (dual output from identical instruction set)
- Layer standards: 10 canonical A- layers with ACI color indices
- Deliverable model
- Audit logging: append-only, cryptographic hashes, 9 event types
- Assembly engine, constraint engine, spec engine
- Parsers: assembly parser, spec parser
- Adapters
- Runtime models
- Pipeline orchestrator
- Two demo apps: assembly_parser_app, spec_intelligence_app

## Does Not Own

- **Root truth:** Universal_Truth_Kernel
- **Construction truth ownership:** Construction_Kernel
- **Governance doctrine:** ValidKernel-Governance
- **Generic runtime logic:** ValidKernel_Runtime
- **Application shell behavior:** Construction_Application_OS

## Stack Position

- **Upstream:** Universal_Truth_Kernel (conceptual, transitive via Construction_Kernel), Construction_Kernel (defines construction truth this runtime executes), ValidKernel-Governance (governance rules), ValidKernel_Runtime (generic runtime patterns — conceptual/pattern alignment; no code inheritance)
- **Downstream:** Construction_Application_OS (apps consume runtime capabilities)

## Primary Directories

| Directory | Role |
|---|---|
| `runtime/` | Core: parsers, models, engines, generators, pipeline, logging, validators |
| `contracts/` | 6 JSON schemas defining pipeline stage boundaries |
| `validators/` | Structural, domain, generation validation |
| `geometry/` | Deterministic geometry engine and rules |
| `generator/` | DXF writer, SVG writer |
| `standards/` | Error codes, layer standards, SVG standards |
| `adapters/` | Translation adapters |
| `apps/` | Demo apps (assembly_parser_app, spec_intelligence_app) |
| `tests/` | Parser, engine, pipeline, mutation, golden, snapshots |

## Future Agent Reading Order

1. `Universal_Truth_Kernel` → `nucleus/NUCLEUS_DOCTRINE.md`
2. `ValidKernel_Registry` → topology surfaces
3. This repo → `docs/system/REPO_MANIFEST.md`
4. This repo → `docs/system/AUTHORITATIVE_PATHS.md`
5. This repo → `docs/system/DEPENDENCY_MAP.md`
6. This repo → `docs/system/FROZEN_SEAMS.md`
7. `contracts/`
8. Only then targeted implementation files

## Frozen

- Contract schemas (6 JSON schemas)
- Validation stages: structural → domain → generation
- Canonical error taxonomy (62 codes, 11 categories)
- DrawingInstructionSet as sole generation input
- DXF and SVG deriving from same instruction set
- Audit event model (append-only, cryptographic hashes)
- Provenance/authority handling: EXPLICIT / DERIVED / INFERRED / UNAPPROVED
- Layer standards (10 A- layers)

## Mutable

- Parser internals (extraction logic, accuracy improvements)
- Engine internals (assembly, constraint, spec)
- Geometry rules parameters and layout algorithms
- Test fixtures
- Adapter implementations

## Relationship to Universal_Truth_Kernel

Upstream conceptual dependency, transitive via Construction_Kernel. This runtime executes applied construction truth ultimately grounded in Universal_Truth_Kernel. It does not originate or redefine truth at any layer.

## Execution Notes

- **Language:** Python
- **Authority:** v0.2
- **Validation model:** Fail-closed, multi-layer (structural → domain → generation)
- **Output model:** Dual output (DXF + SVG from same DrawingInstructionSet)
- **Test categories:** Parser, engine, pipeline, mutation, golden fixtures, snapshots
