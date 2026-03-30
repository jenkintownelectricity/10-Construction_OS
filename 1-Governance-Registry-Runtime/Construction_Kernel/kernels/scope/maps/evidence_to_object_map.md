# Evidence-to-Object Map — Construction Scope Kernel

## Purpose

This map documents how evidence artifacts (inspection reports, commissioning reports, photos, test results) relate to scope records in the Construction Scope Kernel.

## Evidence Sources

Evidence is generated during construction and links back to scope kernel records:

| Evidence Type | Source Activity | Scope Entity Reference |
|--------------|----------------|----------------------|
| Inspection report | Field inspection | inspection_step.inspection_id |
| Inspection photo | Field inspection | inspection_step.inspection_id |
| Test result | Performance testing | inspection_step.test_method_ref |
| Commissioning report | BECx activity | commissioning_step.step_id |
| Commissioning checklist | BECx observation | commissioning_step.step_id |
| Warranty certificate | Closeout | warranty_handoff_record.handoff_id |
| As-built drawing | Closeout | closeout_requirement.requirement_id |
| Maintenance manual | Closeout | closeout_requirement.requirement_id |
| Training record | Closeout | closeout_requirement.requirement_id |

## Linkage Model

```
Evidence Record (external)
├── references ──► inspection_step.inspection_id
├── references ──► commissioning_step.step_id
├── references ──► closeout_requirement.requirement_id
└── references ──► warranty_handoff_record.handoff_id
```

## Evidence Requirements in Scope Records

- `inspection_step.evidence_required` — When true, documented evidence MUST be captured.
- `commissioning_step.documentation_required` — Lists documents that MUST be produced.
- `closeout_requirement` — Each closeout type implies specific evidence deliverables.
- `warranty_handoff_record.documentation_required` — Lists warranty activation documents.

## Evidence Storage

- The scope kernel does NOT store evidence artifacts.
- The scope kernel declares what evidence is required.
- Evidence artifacts are stored in an external evidence management system.
- Evidence links back to scope records via the record's primary key.

## Traceability Chain

```
scope_of_work
  └── inspection_step (evidence_required: true)
        └── Evidence Record (photo, report) ──► stored externally
              └── references inspection_step.inspection_id
```

## Principles

- The scope kernel is the authority on what evidence is required, not on what evidence exists.
- Evidence completeness is validated outside the kernel by comparing requirements to collected artifacts.
- Missing evidence does not invalidate scope records; it indicates an incomplete verification process.
