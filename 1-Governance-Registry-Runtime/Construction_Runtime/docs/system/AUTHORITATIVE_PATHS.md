# AUTHORITATIVE_PATHS — Construction_Runtime

## Cross-Repo Reading Order

Before reading this repo, read:
1. `Universal_Truth_Kernel` → `nucleus/NUCLEUS_DOCTRINE.md`
2. `ValidKernel_Registry` → topology surfaces

Then read this repo's surfaces:
3. `docs/system/REPO_MANIFEST.md`
4. `docs/system/AUTHORITATIVE_PATHS.md`
5. `docs/system/DEPENDENCY_MAP.md`
6. `docs/system/FROZEN_SEAMS.md`

Then repo-specific authoritative files:
7. `contracts/*.schema.json`
8. `standards/error_codes.py`
9. Only then targeted implementation files

## Authoritative

These files define the runtime's v0.2 contract surface and governed runtime standards. Changes here require careful review. Note: "authoritative" here means governing within the runtime's scope — kernel-level canonical truth lives in Construction_Kernel.

- `contracts/*.schema.json` — 6 JSON schemas defining pipeline stage boundaries
- `standards/error_codes.py` — Runtime error taxonomy (62 codes, 11 categories)
- `standards/layer_standards.py` — 10 governed A- layers with ACI color indices
- `runtime/models/drawing_instruction.py` — DrawingInstructionSet (governed intermediate representation)
- `runtime/pipeline/construction_pipeline.py` — Pipeline orchestrator (stage order is frozen)
- `runtime/drawing_engine/contract_loader.py` — Governed contract loader (loads kernel contracts)

## Supporting

Implementation files that execute against frozen contracts. Internals may evolve; interfaces are constrained by authoritative files above.

- `validators/` — Structural, domain, generation validators
- `geometry/` — Deterministic geometry engine and rules
- `generator/` — DXF writer, SVG writer (dual output from DrawingInstructionSet)
- `runtime/parsers/` — Assembly and spec parsers
- `runtime/engines/` — Assembly, constraint, spec engines
- `adapters/` — Translation adapters

## Skip Unless Needed

- `.gitignore` — Standard exclusions
- `apps/` — Demo applications only (assembly_parser_app, spec_intelligence_app); application shell belongs to Construction_Application_OS

## Reserved for Audit and Debug

- `tests/mutation/` — Mutation testing
- `tests/golden/` — Golden fixture tests
- `tests/snapshots/` — Snapshot tests
- `runtime/logging/` — Append-only audit logging (cryptographic hashes, 9 event types)
