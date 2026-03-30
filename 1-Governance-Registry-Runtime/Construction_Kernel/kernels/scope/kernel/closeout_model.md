# Closeout Model

## Purpose

Defines project closeout requirements, warranty handoff, and as-built documentation within scope. Closeout is scope truth because it defines what must be delivered, by whom, and when for the scope to be considered complete.

## Definition

A closeout requirement is a deliverable that must be provided at project completion to satisfy scope obligations. Closeout requirements span warranty submissions, documentation, training, and final inspections.

## Closeout Types

| Type | Description | Typical Responsible Party |
|---|---|---|
| `warranty_submission` | Warranty certificates and NDL letters | Trade contractor |
| `as_built_documentation` | Drawings reflecting actual construction | Trade contractor / architect |
| `maintenance_manual` | O&M manuals for envelope systems | Trade contractor / manufacturer |
| `training` | Facility staff training on maintenance | Trade contractor |
| `spare_materials` | Attic stock and spare materials | Trade contractor |
| `final_inspection` | Final walkthrough and sign-off | Owner's representative |
| `punch_list` | Deficiency list resolution | Trade contractor |

## Warranty Handoff

Warranty handoff records are a specialized closeout requirement. They document the transfer of warranty obligations from the trade contractor (and manufacturer) to the owner.

### Warranty Types
- **Manufacturer's material warranty**: Covers material defects
- **No-Dollar-Limit (NDL) warranty**: Full system coverage from manufacturer
- **Contractor's workmanship warranty**: Covers installation defects
- **Extended warranty**: Additional coverage beyond standard terms

### Warranty Start Triggers
| Trigger | Description |
|---|---|
| `substantial_completion` | Warranty starts at substantial completion of the project |
| `final_completion` | Warranty starts at final completion |
| `occupancy` | Warranty starts at certificate of occupancy |
| `roof_completion` | Warranty starts at completion of roofing work |

## Closeout Sequencing

Closeout requirements follow a general sequence:
1. Punch list generation and resolution
2. Final inspection and sign-off
3. Warranty submissions collected
4. As-built documentation delivered
5. Maintenance manuals delivered
6. Training conducted
7. Spare materials delivered

## Due Date Convention

Closeout requirements use `due_date_relative` to express timing relative to project milestones (e.g., "30 days after substantial completion") rather than absolute dates.

## Schema References

See `schemas/closeout_requirement.schema.json` and `schemas/warranty_handoff_record.schema.json` for formal schema definitions.
