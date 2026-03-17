# Assembly Parser Workflow

## Assembly to Shop Drawing

```
Raw Assembly Letter
  → Normalize (whitespace, control chars, line endings)
  → Parse (extract name, components, constraints)
  → Structural Validation (required fields, types, enums)
  → Domain Validation (material compatibility, assembly rules)
  → Adapter (parsed → AssemblyModel)
  → Constraint Engine (interface, clearance, spacing validation)
  → Assembly Engine (enrich with geometry/material resolution)
  → Geometry Engine (build DrawingInstructionSet)
  → Generation Validation (geometry completeness, layers, sheet)
  → DXF Writer (from DrawingInstructionSet)
  → SVG Writer (from same DrawingInstructionSet)
  → DeliverableModel (dual-format package)
  → Audit Log (append-only events)
```

## Fail-Closed Behavior
If any validation stage fails, the pipeline halts. No partial outputs are emitted as final deliverables.
