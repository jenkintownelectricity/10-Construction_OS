# Frozen Seams

## Purpose

Documents the stable integration points between the Scope Kernel and other kernels or systems. A frozen seam is an interface that has been defined, validated, and locked. Changes to frozen seams require coordinated updates across all connected systems.

## Frozen Seam Registry

### Seam 1: Scope-to-Specification Reference
- **Interface**: `spec_ref` field on scope records
- **Direction**: Scope Kernel --> Spec Kernel (outbound pointer)
- **Contract**: Scope records may reference spec section IDs. The Spec Kernel resolves them.
- **Status**: Frozen
- **Change protocol**: Requires coordinated schema update in both kernels.

### Seam 2: Scope-to-Assembly Reference
- **Interface**: `assembly_ref` field on scope records
- **Direction**: Scope Kernel --> Assembly Kernel (outbound pointer)
- **Contract**: Scope records may reference assembly IDs. The Assembly Kernel resolves them.
- **Status**: Frozen
- **Change protocol**: Requires coordinated schema update in both kernels.

### Seam 3: Control Layer References
- **Interface**: `control_layers_affected` field on scope records
- **Direction**: Scope Kernel --> Reference Intelligence (shared registry)
- **Contract**: Values must exist in `shared/control_layers.json`.
- **Status**: Frozen
- **Change protocol**: Registry changes in Reference Intelligence require scope record validation.

### Seam 4: Interface Zone References
- **Interface**: `interface_zones` field on scope records
- **Direction**: Scope Kernel --> Reference Intelligence (shared registry)
- **Contract**: Values must exist in `shared/interface_zones.json`.
- **Status**: Frozen
- **Change protocol**: Registry changes in Reference Intelligence require scope record validation.

### Seam 5: Schema Version Contract
- **Interface**: `schema_version` field on all scope objects
- **Direction**: Internal
- **Contract**: All scope objects carry `schema_version: "0.1"`. Consumers must validate version before parsing.
- **Status**: Frozen
- **Change protocol**: Version bump requires migration plan for all existing records.

## Seam Integrity Rules

1. Frozen seams are never modified without explicit human authorization.
2. All seam changes are tracked in revision lineage.
3. Breaking changes require a new schema version.
4. Non-breaking additions (new optional fields) do not require seam updates.
