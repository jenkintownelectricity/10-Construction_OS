# Frozen Seams — Construction Assembly Kernel

## Purpose

Frozen seams define the interfaces between this kernel and other systems that are locked and must not be changed without explicit cross-system coordination.

## Frozen Interface: Shared Enum Consumption

- **Seam**: This kernel consumes enum values from `Construction_Reference_Intelligence/shared/shared_enum_registry.json`.
- **Frozen fields**: `control_layer_ids`, `interface_zone_ids`, `lifecycle_stages`, `climate_exposure_flags`, `geometry_contexts`, `risk_levels`, `confidence_levels`, `evidence_types`.
- **Rule**: This kernel must not define alternative values for these fields. If a new value is needed, it must be added to the shared registry first.

## Frozen Interface: Control Layer IDs

- **Seam**: All `control_layer_id` fields in assembly schemas reference `Construction_Reference_Intelligence/shared/control_layers.json`.
- **Frozen values**: `bulk_water_control`, `capillary_control`, `air_control`, `vapor_control`, `thermal_control`, `fire_smoke_control`, `movement_control`, `weathering_surface`, `drainage_plane`, `protection_layer`, `vegetation_support_layer`.
- **Rule**: Adding, removing, or renaming a control layer ID requires coordinated changes across all six family repos.

## Frozen Interface: Interface Zone IDs

- **Seam**: All `interface_zone` fields reference `Construction_Reference_Intelligence/shared/interface_zones.json`.
- **Frozen values**: `roof_to_wall`, `parapet_transition`, `penetration`, `fenestration_edge`, `below_grade_transition`, `expansion_joint`, `deck_to_wall`, `roof_edge`, `curb_transition`, `drain_transition`.
- **Rule**: Same coordination requirement as control layer IDs.

## Frozen Interface: Schema Version Contract

- **Seam**: All schemas declare `schema_version` as a required field with value `"v1"`.
- **Rule**: Changing schema version requires a migration plan. Consumers must be notified before version change. Old versions must remain parseable during transition.

## Frozen Interface: Status Enum

- **Seam**: All kernel objects use `status` with values `active`, `draft`, `deprecated`.
- **Rule**: Adding new status values requires updating all schemas simultaneously and notifying downstream consumers.

## Frozen Interface: Cross-Kernel References

- **Seam**: `material_ref` points to Construction_Material_Kernel entries. `spec_ref` points to Construction_Specification_Kernel entries.
- **Rule**: Reference format (string ID) is frozen. Changing the identifier format in a sibling kernel requires coordinated migration.

## Change Protocol

Any change to a frozen seam requires:
1. Written proposal documenting the change and its impact
2. Review by all affected kernel maintainers
3. Coordinated implementation across all affected repos
4. Version bump in all affected schemas
