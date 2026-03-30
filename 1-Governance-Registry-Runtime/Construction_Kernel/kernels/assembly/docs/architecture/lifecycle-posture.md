# Lifecycle Posture — Construction Assembly Kernel

## Principle

Assemblies span the full building lifecycle from design through replacement. The kernel records lifecycle context as metadata on assembly records, enabling lifecycle-aware queries without owning lifecycle management logic.

## Lifecycle Stages

From the shared enum registry (`shared_enum_registry.json#lifecycle_stages`):

| Stage | Assembly Kernel Relevance |
|---|---|
| design | Assembly configuration is specified: layer stack, control-layer assignments, interface details |
| procurement | Components are sourced; tested assembly configurations constrain substitutions |
| installation | Layer sequencing, attachment methods, and interface detailing are executed |
| commissioning | Assembled systems are verified: air leakage testing, water testing, visual inspection |
| operation | Assembly performs its control-layer functions under service conditions |
| maintenance | Periodic inspection, repair, and re-coating of assembly components |
| failure | Assembly or component failure triggers forensic analysis and remediation |
| replacement | Assembly reaches end of service life; re-roofing, re-cladding, or overlay |

## Lifecycle-Sensitive Assembly Properties

### Design Phase

- Layer stack definition and control-layer assignments are established
- Tested assembly configurations constrain material selections
- Climate and geometry context determine vapor retarder position and insulation strategy
- Interface details are designed for each transition, penetration, and edge condition

### Installation Phase

- Installation sequence matters: substrate preparation before membrane, air barrier before cladding
- Attachment method (mechanically attached, fully adhered, ballasted) affects wind uplift performance
- Weather windows constrain installation timing for temperature-sensitive materials

### Operation and Maintenance

- Weathering surface degrades under UV, thermal cycling, and precipitation
- Sealant joints have finite service life (typically 10-20 years) requiring replacement
- Roof membranes require periodic inspection for punctures, seam failures, and drainage issues

### Failure and Replacement

- Tested assembly records document the as-built configuration for forensic comparison
- Tie-in conditions become relevant when partial replacement creates new-to-existing boundaries
- Overlay vs. tear-off decisions depend on existing assembly composition and condition

## Lifecycle Tracking in Kernel Objects

- `assembly_system.status` — active, draft, deprecated — tracks the record's current standing
- `lineage` object — tracks revision history, supersession, and creation/modification dates
- `tested_assembly_record.test_date` — temporal anchor for test validity
- `tie_in_condition.tie_in_type` — repair_boundary type directly addresses lifecycle transitions

## Relationship to Other Kernels

- **Material Kernel** owns material service life, degradation curves, and compatibility aging
- **Specification Kernel** owns warranty durations and maintenance specification requirements
- **Scope Kernel** owns phasing sequences and replacement scope delineation
- **Reference Intelligence** owns lifecycle pattern analysis and failure trend intelligence
