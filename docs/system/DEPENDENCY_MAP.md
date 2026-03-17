# DEPENDENCY_MAP — Construction_Runtime

## Stack Position

**Layer 6 — Domain Runtime**

## Upstream Dependencies

| Dependency | Layer | Relationship |
|---|---|---|
| Universal_Truth_Kernel | Layer 0 — Nucleus | Conceptual, transitive via Construction_Kernel. Ultimate ground of truth. |
| Construction_Kernel | Layer 5 — Domain Kernel | Defines construction truth this runtime executes. Direct upstream authority. |
| ValidKernel-Governance | Layer 1 — Control Plane | Governance rules constraining runtime behavior. |
| ValidKernel_Runtime | Layer 4 — Execution | Generic runtime patterns (conceptual/pattern alignment; no code inheritance). |

## Downstream Consumers

| Consumer | Layer | Relationship |
|---|---|---|
| Construction_Application_OS | Layer 7 — Application Shell | Apps consume runtime capabilities. |

## Internal Zones

| Zone | Contents | Role |
|---|---|---|
| `contracts/` | 6 JSON schemas | Pipeline stage boundary definitions |
| `validators/` | structural, domain, generation | Three-stage fail-closed validation |
| `runtime/parsers/` | assembly_parser, spec_parser | Input normalization |
| `runtime/models/` | drawing_instruction, runtime models | Execution data structures |
| `runtime/engines/` | assembly, constraint, spec | Domain execution engines |
| `geometry/` | engine, rules | Deterministic geometry computation |
| `generator/` | dxf_writer, svg_writer | Dual output from DrawingInstructionSet |
| `runtime/pipeline/` | construction_pipeline | Pipeline orchestration |
| `runtime/logging/` | audit logging | Append-only, cryptographic hashes |
| `standards/` | error_codes, layer_standards, svg_standards | Canonical standards |
| `adapters/` | translation adapters | External interface translation |
| `apps/` | assembly_parser_app, spec_intelligence_app | Demo applications |
| `tests/` | parser, engine, pipeline, mutation, golden, snapshots | 6 test categories |

## Relationship to Universal_Truth_Kernel

Executes applied construction truth ultimately grounded in the nucleus. Does not originate or redefine truth at any layer. Truth flows: Universal_Truth_Kernel → Construction_Kernel → Construction_Runtime (execution only).
