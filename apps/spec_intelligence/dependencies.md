# Spec Intelligence Dependencies

## Runtime Dependencies (Construction_Runtime v0.2)
| Dependency | Component |
|-----------|-----------|
| Contract schemas | `contracts/spec_input.schema.json`, `contracts/runtime_spec.schema.json`, `contracts/deliverable.schema.json` |
| Structural validator | `validators/structural_validator.py` |
| Domain validator | `validators/domain_validator.py` |
| Spec parser | `runtime/parsers/spec_parser/` |
| Spec engine | `runtime/engines/spec_engine/` |
| Audit logger | `runtime/logging/runtime_log.py` |
| Pipeline orchestrator | `runtime/pipeline/construction_pipeline.py` |

## Kernel Dependencies (Construction_Kernel)
| Kernel | Role |
|--------|------|
| Governance | Governance truth — contracts, specifications, scope |
| Chemistry | Material truth — product data, manufacturer documentation |
| Geometry | Geometric truth — plans, sections, dimensions |
| Intelligence | Intelligence truth — derived analysis, opportunity detection |

## Upstream Truth
Consumes applied construction truth from Construction_Kernel, ultimately grounded in Universal_Truth_Kernel.
