# Spec Intelligence Workflow

## Spec to Opportunity

```
Raw Specification Text
  → Normalize (whitespace, control chars, line endings)
  → Parse (extract sections, requirements, product refs, basis-of-design)
  → Structural Validation (required fields, types)
  → Domain Validation (mandatory requirements, product references)
  → Adapter (parsed → runtime spec model)
  → Spec Engine (extract opportunities, analyze requirements)
  → Contract Validation (intelligence output schema)
  → DeliverableModel (intelligence package)
  → Audit Log (append-only events)
```

## Fail-Closed Behavior
If any validation stage fails, the pipeline halts. No partial intelligence outputs are emitted as final deliverables.
