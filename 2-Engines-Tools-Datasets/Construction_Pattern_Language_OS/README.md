# Construction_Pattern_Language_OS

> Canonical construction pattern language kernel for the ValidKernel architecture.

This repository defines the **construction pattern language** — the authoritative source of truth for construction detail patterns, pattern families, variants, relationships, artifact intents, and constraint profiles.

This system operates within the truth boundary defined by Universal_Truth_Kernel.
Structural patterns are derived from ValidKernel_Patterns. No logic is inherited.
This repository does not own or redefine root-level doctrine.

## Kernel Identity

| Field | Value |
|-------|-------|
| **Kernel Name** | Construction_Pattern_Language_OS |
| **Kernel Type** | domain_pattern_language |
| **Domain Scope** | construction_patterns |
| **Grown From** | ValidKernel_Patterns |
| **Lineage Status** | FROZEN |
| **Schema Version** | 1.0.0 |
| **Pattern Language Version** | 1.0.0 |

## Entity Hierarchy

```
PatternFamily
  → Pattern
    → PatternVariant
```

### Supporting Entities

- **PatternRelationship** — adjacency, conflict, and dependency between patterns
- **DetailIntent** — what a pattern is intended to detail
- **ArtifactIntent** — what artifacts a pattern produces (shop drawings, specifications, submittals, inspections)
- **ConstraintProfile** — manufacturer, code, dimensional, and environmental constraints

## Identifier System

Natural-system identifiers using classes: `DNA`, `CHEM`, `COLOR`, `SOUND`, `TEXTURE`, `CLIMATE`

Format: `<CLASS>-CONSTR-<TYPE>-<NAME>-<INDEX>-R<REV>`

See [kernel_manifest/identifier_system.md](kernel_manifest/identifier_system.md) for full specification.

## Structure

```
kernel_manifest/          Kernel identity, lineage, identifier system
pattern_language/         Pattern families, patterns, variants
pattern_relationships/    Adjacency, conflict, dependency rules
artifact_intents/         Shop drawing, specification, submittal, inspection intents
constraint_profiles/      Manufacturer, code, dimensional, environmental constraints
schemas/                  JSON Schema definitions for all entities
validators/               Python validators for structural integrity
docs/                     Documentation
examples/                 Starter pattern family examples
```

## Starter Pattern Families

1. **Roof Edge** — Edge metal termination patterns
2. **Parapet** — Parapet wall cap and flashing patterns
3. **Roof Drain** — Roof drain and overflow patterns
4. **Pipe Penetration** — Pipe and conduit penetration patterns
5. **Expansion Joint** — Expansion and control joint patterns

## Authority Boundaries

This repository **defines**:
- Pattern families, patterns, and variants
- Pattern relationships (adjacency, conflict, dependency)
- Artifact intents (shop drawing, specification, submittal, inspection)
- Constraint profiles (manufacturer, code, dimensional, environmental)

This repository **does not define**:
- Reasoning or inference logic
- Runtime behavior or execution
- Rendering or visualization
- Assistant or UI logic
- Canonical truth or root doctrine

## Reading Order

1. `kernel_manifest/kernel_manifest.yaml`
2. `kernel_manifest/lineage.yaml`
3. `kernel_manifest/identifier_system.md`
4. `schemas/` (all schema files)
5. `pattern_language/pattern_families/`
6. `docs/pattern_language_overview.md`
