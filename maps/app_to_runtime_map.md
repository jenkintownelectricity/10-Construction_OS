# App-to-Runtime Map — Construction Application OS v0.1

## Assembly Parser App → Construction_Runtime v0.2

| App Capability | Runtime Component | Runtime Path |
|---------------|------------------|-------------|
| Parse assembly text | Assembly parser | `runtime/parsers/assembly_parser/` |
| Normalize input | Normalizer | `runtime/parsers/assembly_parser/normalizer.py` |
| Structural validation | Structural validator | `validators/structural_validator.py` |
| Domain validation | Domain validator | `validators/domain_validator.py` |
| Adapt to model | Assembly adapter | `adapters/assembly_adapter.py` |
| Check constraints | Constraint engine | `runtime/engines/constraint_engine/` |
| Run assembly engine | Assembly engine | `runtime/engines/assembly_engine/` |
| Build geometry | Geometry engine | `geometry/geometry_engine.py` |
| Validate generation | Generation validator | `validators/generation_validator.py` |
| Generate DXF | DXF writer | `generator/dxf_writer.py` |
| Generate SVG | SVG writer | `generator/svg_writer.py` |
| Package deliverable | Deliverable model | `runtime/models/deliverable_model.py` |
| Log audit events | Audit logger | `runtime/logging/runtime_log.py` |
| Orchestrate pipeline | Pipeline | `runtime/pipeline/construction_pipeline.py` |

## Spec Intelligence App → Construction_Runtime v0.2

| App Capability | Runtime Component | Runtime Path |
|---------------|------------------|-------------|
| Parse spec text | Spec parser | `runtime/parsers/spec_parser/` |
| Normalize input | Normalizer | `runtime/parsers/spec_parser/normalizer.py` |
| Structural validation | Structural validator | `validators/structural_validator.py` |
| Domain validation | Domain validator | `validators/domain_validator.py` |
| Run spec engine | Spec engine | `runtime/engines/spec_engine/` |
| Package deliverable | Deliverable model | `runtime/models/deliverable_model.py` |
| Log audit events | Audit logger | `runtime/logging/runtime_log.py` |
| Orchestrate pipeline | Pipeline | `runtime/pipeline/construction_pipeline.py` |
