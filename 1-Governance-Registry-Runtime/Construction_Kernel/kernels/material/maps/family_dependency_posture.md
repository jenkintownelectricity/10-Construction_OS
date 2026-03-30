# Family Dependency Posture — Construction Material Kernel

## Dependency Direction

This kernel has a clean dependency posture with no circular references:

```
Shared Artifacts (Intelligence) ──> Material Kernel ──> Sibling Kernels
                                                    ──> Intelligence Layer
```

## Inbound Dependencies

| Source | Type | Criticality |
|---|---|---|
| shared_enum_registry.json | Vocabulary | Critical — schema validation fails without it |
| shared_taxonomy.json | Taxonomy | Critical — material class enum source |
| shared_standards_registry.json | Standards | High — test method reference format |
| control_layers.json | Registry | Medium — control layer mapping |
| interface_zones.json | Registry | Medium — interface zone context |
| division_07_posture.json | Alignment | Low — informational alignment |

## Outbound Dependencies

| Consumer | Data Type | Breakage Impact |
|---|---|---|
| Specification Kernel | Material properties | Spec requirements lose material reference data |
| Assembly Kernel | Properties, compatibility | Assembly design loses material constraints |
| Chemistry Kernel | Class, compatibility | Chemistry analysis loses material context |
| Scope Kernel | Class references | Scope boundaries lose material references |
| Intelligence Layer | All material truth | Cross-kernel correlation loses material dimension |

## Dependency Health Rules

1. This kernel must never depend on sibling kernel data
2. Shared artifact availability is a prerequisite for schema validation
3. Outbound consumers must handle missing data gracefully (fail-closed)
4. Dependency versions are tracked in BASELINE_STATE.json
5. Breaking changes to shared artifacts require family-wide coordination

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Shared enum registry unavailable | Cache last-known-good enum values locally |
| Sibling kernel references broken material IDs | Validate at integration layer, not here |
| Circular dependency introduced | Architectural review required for any new dependency |
| Shared artifact version mismatch | Baseline state tracks validated versions |
