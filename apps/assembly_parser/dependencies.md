# Assembly Parser Dependencies

## Runtime Dependencies (Construction_Runtime v0.2)
| Dependency | Component |
|-----------|-----------|
| Contract schemas | `contracts/assembly_input.schema.json`, `contracts/runtime_assembly.schema.json`, `contracts/drawing_instruction.schema.json`, `contracts/deliverable.schema.json` |
| Structural validator | `validators/structural_validator.py` |
| Domain validator | `validators/domain_validator.py` |
| Generation validator | `validators/generation_validator.py` |
| Assembly parser | `runtime/parsers/assembly_parser/` |
| Assembly adapter | `adapters/assembly_adapter.py` |
| Assembly engine | `runtime/engines/assembly_engine/` |
| Constraint engine | `runtime/engines/constraint_engine/` |
| Geometry engine | `geometry/geometry_engine.py` |
| DXF writer | `generator/dxf_writer.py` |
| SVG writer | `generator/svg_writer.py` |
| Audit logger | `runtime/logging/runtime_log.py` |
| Pipeline orchestrator | `runtime/pipeline/construction_pipeline.py` |

## Kernel Dependencies (Construction_Kernel)
| Kernel | Role |
|--------|------|
| Chemistry | Material truth — what products are made of |
| Assembly | Assembly truth — how components compose into buildable conditions |
| Geometry | Geometric truth — shapes, dimensions, spatial relationships |
| Deliverable | Deliverable truth — what is formally produced and issued |

## Upstream Truth
Consumes applied construction truth from Construction_Kernel, ultimately grounded in Universal_Truth_Kernel.
