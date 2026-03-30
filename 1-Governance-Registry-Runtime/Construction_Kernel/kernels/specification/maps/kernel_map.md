# Kernel Map — Construction Specification Kernel

## Entity Relationship Overview

This map shows the high-level relationships between the core entities in the specification kernel.

## Primary Entity Graph

```
specification_document
  |
  +---> specification_section (1:many)
          |
          +---> requirement (1:many)
          |       |
          |       +---> source_pointer (many:1)
          |       +---> reference_standard (many:many)
          |       +---> requirement_condition (1:many)
          |
          +---> prohibition (1:many)
          |       +---> source_pointer (many:1)
          |
          +---> allowance (1:many)
          |       +---> source_pointer (many:1)
          |
          +---> submittal_requirement (1:many)
          |
          +---> qualification_requirement (1:many)
          |
          +---> warranty_requirement (1:many)
          |
          +---> testing_requirement (1:many)
                  +---> reference_standard (many:1)

specification_revision ---> specification_document (many:1)
specification_revision --supersedes--> specification_revision (1:1)
```

## Shared Registry Linkages

- `specification_section.control_layers_served` references `control_layers.json`
- `requirement.control_layers` references `control_layers.json`
- `requirement.interface_zones` references `interface_zones.json`
- `requirement.lifecycle_stage` references `shared_enum_registry.json`
- `requirement.climate_context` references `shared_enum_registry.json`
- `requirement.geometry_context` references `shared_enum_registry.json`

## Cross-Kernel Pointers (Outbound)

This kernel does not maintain outbound pointers to sibling kernels. Sibling kernels reference specification records by ID. The intelligence layer reads from this kernel.

## Key Relationship Rules

1. Every specification fact traces to at least one source_pointer
2. Specification sections are the primary containers for all obligation records
3. Requirements are the most granular truth unit
4. Revision records create supersession chains between specification versions
5. All entities validate against frozen schemas at the current baseline version
