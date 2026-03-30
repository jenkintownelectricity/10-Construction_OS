# Construction Scope Kernel V0.1

## Version

| Field | Value |
|---|---|
| **Kernel** | Construction Scope Kernel |
| **Version** | 0.1 |
| **Status** | Draft |
| **Created** | 2026-03-17 |
| **Domain** | CSI Division 07 -- Building Envelope Systems |
| **Family** | construction-kernel |
| **Registry** | ValidKernel_Registry |

## Scope of This Version

Version 0.1 establishes the foundational object model, schemas, and truth boundaries for scope-domain knowledge in the building envelope domain.

## Objects Defined

1. **Scope of Work** -- Root object defining work boundaries with inclusions, exclusions, and trade responsibilities.
2. **Work Operation** -- Individual work activities within a scope.
3. **Sequence Step** -- Ordered installation steps with predecessor/successor dependencies.
4. **Trade Responsibility** -- Trade-to-scope mappings with coordination interfaces.
5. **Inspection Step** -- Quality verification checkpoints with hold points.
6. **Commissioning Step** -- BECx phase milestones with acceptance criteria.
7. **Closeout Requirement** -- Warranty, documentation, and handoff deliverables.
8. **Warranty Handoff Record** -- Warranty transfer documentation with conditions.
9. **Scope Entry** -- Atomic scope fact records (inherited from baseline).

## Schema Version

All schemas in V0.1 use `schema_version: "0.1"` except `scope_entry.schema.json` which uses `schema_version: "v1"` (inherited from baseline).

## Truth Boundaries

- Owns: scope boundaries, inclusion/exclusion rules, trade coordination, work-breakdown, sequencing, inspection, commissioning, closeout.
- Does not own: specifications, assemblies, material properties, chemistry, reference intelligence content.

## Known Limitations

- Division 07 only. Other CSI divisions are future scope.
- No runtime integration. Runtime maps are stubs.
- No digital twin integration. Digital twin maps are stubs.
- Climate and geometry context are recorded but not computationally evaluated.

## Migration Notes

No prior version exists. V0.1 is the initial release.
