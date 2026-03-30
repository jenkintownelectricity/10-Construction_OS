# Consumer Readiness Contract — Construction_ALEXANDER_Engine

**Document ID:** CPLOS-CONTRACT-ALEXANDER-001
**Date:** 2026-03-22
**Authority:** Armand Lefebvre, L0
**Status:** ACTIVE

## Purpose

This contract defines the interface, guarantees, and constraints that
Construction_ALEXANDER_Engine may rely upon when consuming pattern data
from Construction_Pattern_Language_OS.

## Consumer Identity

| Field | Value |
|---|---|
| Consumer | Construction_ALEXANDER_Engine |
| Provider | Construction_Pattern_Language_OS |
| Contract Type | Read-only consumption |
| Schema Version | 1.0.0 |
| Pattern Language Version | 1.0.0 |

## What ALEXANDER May Consume

### 1. Pattern Hierarchy

| Entity Type | ID Prefix | Schema File | Guaranteed Fields |
|---|---|---|---|
| PatternFamily | `DNA-CONSTR-FAM-*` | `schemas/pattern_family.schema.json` | `id`, `name`, `description`, `patterns` |
| Pattern | `DNA-CONSTR-PAT-*` | `schemas/pattern.schema.json` | `id`, `name`, `description`, `family_id`, `variants` |
| PatternVariant | `CHEM-CONSTR-VAR-*` | `schemas/pattern_variant.schema.json` | `id`, `name`, `description`, `pattern_id`, `method`, `materials` |

### 2. Pattern Relationships

| Relationship Type | ID Prefix | Schema File |
|---|---|---|
| adjacency | `SOUND-CONSTR-REL-*` | `schemas/pattern_relationship.schema.json` |
| conflict | `SOUND-CONSTR-REL-*` | `schemas/pattern_relationship.schema.json` |
| dependency | `SOUND-CONSTR-REL-*` | `schemas/pattern_relationship.schema.json` |

### 3. Constraint Profiles

| Constraint Type | ID Prefix | Schema File |
|---|---|---|
| manufacturer | `TEXTURE-CONSTR-CNS-*` | `schemas/constraint_profile.schema.json` |
| code | `TEXTURE-CONSTR-CNS-*` | `schemas/constraint_profile.schema.json` |
| dimensional | `TEXTURE-CONSTR-CNS-*` | `schemas/constraint_profile.schema.json` |
| environmental | `CLIMATE-CONSTR-CNS-*` | `schemas/constraint_profile.schema.json` |

### 4. Artifact Intents

| Artifact Type | ID Prefix | Schema File |
|---|---|---|
| shop_drawing | `COLOR-CONSTR-ART-*` | `schemas/artifact_intent.schema.json` |
| specification | `COLOR-CONSTR-ART-*` | `schemas/artifact_intent.schema.json` |
| submittal | `COLOR-CONSTR-ART-*` | `schemas/artifact_intent.schema.json` |
| inspection | `COLOR-CONSTR-ART-*` | `schemas/artifact_intent.schema.json` |

### 5. Indexes

| Index | File | Purpose |
|---|---|---|
| Canonical ID Index | `docs/CANONICAL_ID_INDEX.yaml` | Resolve ID to file path and entity type |
| Alias Lookup | `docs/ALIAS_LOOKUP.yaml` | Resolve human-readable terms to canonical IDs |

## Provider Guarantees

1. **ID immutability** — Once assigned, an entity ID never changes
2. **ID uniqueness** — No two entities share the same ID within the kernel
3. **Hierarchy integrity** — Every variant belongs to exactly one pattern; every pattern belongs to exactly one family
4. **Relationship integrity** — All source and target references in relationships point to existing entities
5. **Dependency acyclicity** — The dependency subgraph is always a DAG (no circular dependencies)
6. **Conflict symmetry** — If A conflicts with B, B conflicts with A
7. **Schema compliance** — All entities conform to their JSON Schema definitions in `schemas/`
8. **Version compatibility** — All entities use the same `schema_version` and `pattern_language_version`
9. **No deprecated references** — Active entities do not reference deprecated entities
10. **Fail-closed validation** — All validators reject invalid state; no partial pass

## Consumer Constraints

1. **Read-only** — ALEXANDER must not write to Construction_Pattern_Language_OS
2. **Reference by canonical ID** — All references must use canonical IDs, not aliases or names
3. **No truth redefinition** — ALEXANDER must not redefine pattern semantics, relationships, or constraints
4. **No inference caching as truth** — ALEXANDER may cache pattern data for performance but must not treat cached inferences as canonical
5. **Validation before use** — ALEXANDER should validate consumed data against schemas before processing
6. **Deprecation compliance** — If an entity is deprecated, ALEXANDER must stop referencing it

## Data Access Patterns

### Recommended Consumption Order

```
1. Load CANONICAL_ID_INDEX.yaml        → build entity registry
2. Load ALIAS_LOOKUP.yaml              → build alias resolver
3. Load pattern_families/*.yaml        → enumerate families
4. Load patterns/*.yaml                → enumerate patterns per family
5. Load pattern_variants/*.yaml        → enumerate variants per pattern
6. Load pattern_relationships/*.yaml   → build relationship graph
7. Load constraint_profiles/*.yaml     → attach constraints
8. Load artifact_intents/*.yaml        → attach artifact intents
```

### Graph Construction

```
ALEXANDER should build an internal graph where:
  - Nodes = families, patterns, variants
  - Edges = adjacency (bidirectional), conflict (symmetric), dependency (directed DAG)
  - Constraint profiles attach to nodes via applies_to references
  - Artifact intents attach to nodes via pattern_refs references
```

### Conflict Resolution

When ALEXANDER encounters a pattern arrangement:
1. Check adjacency rules — are the patterns valid neighbors?
2. Check conflict rules — are any patterns incompatible?
3. Check dependency rules — are all required patterns present?
4. Check constraint profiles — are dimensional/code/environmental limits met?

## Versioning Contract

| Version Change | Impact | ALEXANDER Action |
|---|---|---|
| Patch (1.0.x) | Bug fixes, typo corrections | No action required |
| Minor (1.x.0) | New entities added, no breaking changes | Re-index, pick up new entities |
| Major (x.0.0) | Schema changes, ID format changes, entity removal | Full re-validation required |

## Current Inventory (v1.0.0)

| Entity Type | Count |
|---|---|
| Pattern Families | 5 |
| Patterns | 10 |
| Pattern Variants | 20 |
| Pattern Relationships | 8 |
| Artifact Intents | 5 |
| Constraint Profiles | 5 |
| **Total Entities** | **53** |

## Validation Entry Point

ALEXANDER (or any consumer) can validate the kernel state before consumption:

```bash
python validators/graph_validator.py /path/to/Construction_Pattern_Language_OS
python validators/hierarchy_validator.py /path/to/Construction_Pattern_Language_OS
python validators/identifier_validator.py /path/to/Construction_Pattern_Language_OS
```

All three must return `RESULT: PASS` before consumption is safe.

## Non-Guarantees

- This contract does NOT guarantee pattern completeness (more families will be added)
- This contract does NOT guarantee rendering instructions (ALEXANDER must source those elsewhere)
- This contract does NOT guarantee condition evaluation logic (owned by Construction_Kernel)
- This contract does NOT guarantee runtime execution behavior (owned by Construction_Runtime)
