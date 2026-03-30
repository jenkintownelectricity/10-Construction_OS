# Identifier System

## Overview

Construction_Pattern_Language_OS uses a **natural-system identifier scheme** that maps construction entities to natural classification metaphors.

## Identifier Classes

| Class | Metaphor | Used For |
|-------|----------|----------|
| `DNA` | Genetic blueprint | Pattern families, patterns (core identity) |
| `CHEM` | Chemical composition | Pattern variants (material/method composition) |
| `COLOR` | Visual signature | Artifact intents (visual output references) |
| `SOUND` | Acoustic/relational signal | Pattern relationships (connections between entities) |
| `TEXTURE` | Surface/interface quality | Constraint profiles (surface-level rules) |
| `CLIMATE` | Environmental context | Environmental constraint profiles |

## Identifier Format

```
<CLASS>-CONSTR-<TYPE>-<NAME>-<INDEX>-R<REV>
```

### Fields

| Field | Description | Example |
|-------|-------------|---------|
| `CLASS` | Natural-system class | `DNA`, `CHEM`, `COLOR`, `SOUND`, `TEXTURE`, `CLIMATE` |
| `CONSTR` | Domain prefix (always `CONSTR` for construction) | `CONSTR` |
| `TYPE` | Entity type abbreviation | `FAM`, `PAT`, `VAR`, `REL`, `ART`, `CNS`, `DTL` |
| `NAME` | Human-readable name segment | `EDGE`, `PARAPET`, `MECHANICAL` |
| `INDEX` | Numeric index (zero-padded 3 digits) | `001`, `010`, `101` |
| `REV` | Revision number | `R1`, `R2` |

### Entity Type Abbreviations

| Abbreviation | Entity |
|-------------|--------|
| `FAM` | PatternFamily |
| `PAT` | Pattern |
| `VAR` | PatternVariant |
| `REL` | PatternRelationship |
| `ART` | ArtifactIntent |
| `CNS` | ConstraintProfile |
| `DTL` | DetailIntent |

## Examples

| ID | Entity | Description |
|----|--------|-------------|
| `DNA-CONSTR-FAM-EDGE-001-R1` | PatternFamily | Roof Edge family |
| `DNA-CONSTR-PAT-EDGE-METAL-010-R1` | Pattern | Edge metal pattern |
| `CHEM-CONSTR-VAR-MECHANICAL-101-R1` | PatternVariant | Mechanical fastening variant |
| `COLOR-CONSTR-ART-BLUEPRINT-001-R1` | ArtifactIntent | Blueprint artifact intent |
| `SOUND-CONSTR-REL-ADJACENT-001-R1` | PatternRelationship | Adjacency relationship |
| `TEXTURE-CONSTR-CNS-MEMBRANE-001-R1` | ConstraintProfile | Membrane constraint profile |
| `CLIMATE-CONSTR-CNS-WINDZONE-003-R1` | ConstraintProfile | Wind zone constraint profile |

## Rules

1. **Immutable** — Once assigned, an identifier never changes
2. **Unique** — No two entities share the same identifier
3. **Human-readable** — Identifiers convey meaning at a glance
4. **Canonical references** — All cross-references use canonical IDs
5. **No reuse** — Deprecated identifiers are never reassigned
6. **Revision tracking** — New revisions increment the `R<n>` suffix
