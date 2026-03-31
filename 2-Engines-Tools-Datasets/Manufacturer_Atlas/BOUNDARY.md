# Manufacturer Atlas — Boundary

## Classification

| Property | Value |
|----------|-------|
| Type | MANUFACTURER_KNOWLEDGE_GRAPH |
| Domain | building_envelope |
| Plane | domain_plane |
| Parent | 2-Engines-Tools-Datasets |
| Write Authority | 10-Construction_OS only |

## What This Directory Contains

- Atlas graph primitives (AtlasNode, AtlasEdge)
- Manufacturer domain graph data
- Atlas lens definitions
- Assembly constraint sets
- Detail graph relation layer
- Atlas navigation surface and view contracts

## What This Directory Does NOT Contain

- CAD drawing engines (owned by Construction_Atlas OMNI View)
- Runtime execution logic (owned by Construction_Runtime)
- UI application surfaces (owned by Construction_Application_OS)
- Signal bus infrastructure (owned by ValidKernelOS_VKBUS)

## Cross-References (READ ONLY)

- Construction_Atlas: spatial context truth layer
- Construction_Runtime: execution consumer
- Construction_Application_OS: UI rendering consumer
- Constraint-Port: constraint evaluation patterns
- Construction_Pattern_Language_OS: pattern constraint profiles
