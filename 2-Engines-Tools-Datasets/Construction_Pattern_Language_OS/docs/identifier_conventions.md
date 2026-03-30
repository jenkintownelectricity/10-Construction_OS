# Identifier Conventions

## Format

All identifiers in Construction_Pattern_Language_OS follow this canonical format:

```
<CLASS>-CONSTR-<TYPE>-<NAME>-<INDEX>-R<REV>
```

| Segment | Description | Constraints |
|---------|-------------|-------------|
| `CLASS` | Natural-system classification | One of: `DNA`, `CHEM`, `COLOR`, `SOUND`, `TEXTURE`, `CLIMATE` |
| `CONSTR` | Domain prefix | Always `CONSTR` for construction entities |
| `TYPE` | Entity type abbreviation | One of: `FAM`, `PAT`, `VAR`, `REL`, `DET`, `ART`, `CNS` |
| `NAME` | Human-readable name | Uppercase letters, digits, underscores; multi-segment names joined with hyphens |
| `INDEX` | Numeric index | Zero-padded 3-digit number (`001`--`999`) |
| `REV` | Revision | `R` followed by integer starting at `1` |

## Classes

Each class maps to a natural-system metaphor and is restricted to specific entity types.

| Class | Metaphor | Used For | Allowed Types |
|-------|----------|----------|---------------|
| `DNA` | Genetic blueprint | Core identity entities | `FAM`, `PAT`, `DET` |
| `CHEM` | Chemical composition | Material/method variants | `VAR` |
| `COLOR` | Visual signature | Artifact output intents | `ART` |
| `SOUND` | Acoustic/relational signal | Pattern relationships | `REL` |
| `TEXTURE` | Surface/interface quality | Physical constraints | `CNS` |
| `CLIMATE` | Environmental context | Environmental constraints | `CNS` |

## Type Codes

| Code | Entity | Required Class | Example |
|------|--------|---------------|---------|
| `FAM` | PatternFamily | `DNA` | `DNA-CONSTR-FAM-EDGE-001-R1` |
| `PAT` | Pattern | `DNA` | `DNA-CONSTR-PAT-EDGE-DRIP-001-R1` |
| `VAR` | PatternVariant | `CHEM` | `CHEM-CONSTR-VAR-MECHANICAL-101-R1` |
| `REL` | PatternRelationship | `SOUND` | `SOUND-CONSTR-REL-ADJACENT-001-R1` |
| `DET` | DetailIntent | `DNA` | `DNA-CONSTR-DET-EDGETERMINATION-001-R1` |
| `ART` | ArtifactIntent | `COLOR` | `COLOR-CONSTR-ART-SHOPDRW-001-R1` |
| `CNS` | ConstraintProfile | `TEXTURE` or `CLIMATE` | `TEXTURE-CONSTR-CNS-FLANGEWIDTH-001-R1` |

## Full Examples by Entity Type

### PatternFamily

```
DNA-CONSTR-FAM-EDGE-001-R1         Roof Edge family
DNA-CONSTR-FAM-PARAPET-002-R1      Parapet family
DNA-CONSTR-FAM-DRAIN-003-R1        Roof Drain family
DNA-CONSTR-FAM-PENETRATION-004-R1  Pipe Penetration family
DNA-CONSTR-FAM-JOINT-005-R1        Expansion Joint family
```

### Pattern

```
DNA-CONSTR-PAT-EDGE-DRIP-001-R1        Drip edge pattern (Roof Edge family)
DNA-CONSTR-PAT-EDGE-GRAVELSTOP-002-R1  Gravel stop pattern (Roof Edge family)
DNA-CONSTR-PAT-PARAPET-CAP-001-R1      Parapet cap pattern (Parapet family)
DNA-CONSTR-PAT-DRAIN-INTERNAL-001-R1   Internal drain pattern (Roof Drain family)
DNA-CONSTR-PAT-PENETRATION-BOOT-001-R1 Pipe boot pattern (Pipe Penetration family)
```

The NAME segment for patterns uses a multi-segment format: `<FAMILY_NAME>-<PATTERN_NAME>`.
This embeds the family context directly in the identifier.

### PatternVariant

```
CHEM-CONSTR-VAR-MECHANICAL-101-R1      Mechanical fastening variant
CHEM-CONSTR-VAR-ADHERED-102-R1         Adhered variant
CHEM-CONSTR-VAR-EXTRUDED-201-R1        Extruded aluminum variant
CHEM-CONSTR-VAR-FORMED-202-R1          Formed metal variant
```

Variant indices encode their parent pattern relationship:
- `101`--`199`: Variants of the first pattern in a family
- `201`--`299`: Variants of the second pattern in a family
- `301`--`399`: Variants of the third pattern, and so on

### PatternRelationship

```
SOUND-CONSTR-REL-ADJACENT-001-R1       Adjacency relationship
SOUND-CONSTR-REL-TERMINATES-002-R1     Termination relationship
SOUND-CONSTR-REL-CONFLICTS-003-R1      Conflict relationship
SOUND-CONSTR-REL-DEPENDS-004-R1        Dependency relationship
```

### ArtifactIntent

```
COLOR-CONSTR-ART-SHOPDRW-001-R1        Shop drawing intent
COLOR-CONSTR-ART-SPEC-002-R1           Specification intent
COLOR-CONSTR-ART-SUBMITTAL-003-R1      Submittal intent
COLOR-CONSTR-ART-INSPECT-004-R1        Inspection checklist intent
```

### ConstraintProfile

```
TEXTURE-CONSTR-CNS-FLANGEWIDTH-001-R1  Dimensional constraint (flange width)
TEXTURE-CONSTR-CNS-GAUGE-002-R1        Dimensional constraint (metal gauge)
TEXTURE-CONSTR-CNS-OVERLAP-003-R1      Dimensional constraint (lap joint overlap)
CLIMATE-CONSTR-CNS-WINDZONE-001-R1     Environmental constraint (wind zone)
CLIMATE-CONSTR-CNS-EXPOSURE-002-R1     Environmental constraint (exposure category)
```

## Rules for Creating New Identifiers

1. **Immutable** -- Once assigned, an identifier never changes. A new revision creates a
   new `R<n>` suffix; the base segments persist.

2. **Globally unique** -- No two entities across the entire kernel may share the same
   identifier.

3. **Human-readable** -- The `NAME` segment must convey the entity's purpose at a glance.
   Use domain terminology (e.g., `GRAVELSTOP`, not `TYPE2`; `FLANGEWIDTH`, not `DIM1`).

4. **Class-type agreement** -- The `CLASS` must be valid for the `TYPE`:
   - `DNA` is for `FAM`, `PAT`, and `DET` only
   - `CHEM` is for `VAR` only
   - `COLOR` is for `ART` only
   - `SOUND` is for `REL` only
   - `TEXTURE` is for `CNS` (physical constraints) only
   - `CLIMATE` is for `CNS` (environmental constraints) only

5. **No reuse** -- Deprecated identifiers are never reassigned to new entities.

6. **Canonical references** -- All cross-entity references (e.g., `family_id`,
   `pattern_id`, `source_id`, `target_id`) must use the full canonical identifier string.

7. **Index allocation** -- Within a type, indices are allocated sequentially:
   - Families: `001`--`099`
   - Patterns: `001`--`099` per family
   - Variants: `101`--`199` for first pattern, `201`--`299` for second, etc.
   - Relationships: `001`--`999` globally
   - Artifact intents: `001`--`999` globally
   - Constraint profiles: `001`--`999` globally

8. **Revision starts at 1** -- Every new entity begins at `R1`. Revisions increment
   monotonically. Never skip revision numbers.

## Regex Pattern

The validators enforce this regex:

```
^([A-Z]+)-CONSTR-([A-Z]+)-([A-Z][A-Z0-9_]*(?:-[A-Z][A-Z0-9_]*)*)-(\d{3})-R(\d+)$
```

This permits multi-segment names like `EDGE-DRIP` and `EDGE-GRAVELSTOP` for Pattern IDs
while keeping single-segment names like `EDGE` for Family IDs.

### Regex Breakdown

| Group | Captures | Example Match |
|-------|----------|---------------|
| `([A-Z]+)` | CLASS | `DNA`, `CHEM`, `SOUND` |
| `CONSTR` | Domain literal | Always `CONSTR` |
| `([A-Z]+)` | TYPE | `FAM`, `PAT`, `VAR` |
| `([A-Z][A-Z0-9_]*(?:-[A-Z][A-Z0-9_]*)*)` | NAME (one or more segments) | `EDGE`, `EDGE-DRIP` |
| `(\d{3})` | INDEX | `001`, `101` |
| `R(\d+)` | REV number | `1`, `2` |

## Quick Decision Table

Use this table when assigning an identifier to a new entity:

| I am creating a... | Use CLASS | Use TYPE | NAME format | INDEX range |
|--------------------|-----------|----------|-------------|-------------|
| New pattern family | `DNA` | `FAM` | Single segment: `EDGE` | `001`--`099` |
| New pattern | `DNA` | `PAT` | Multi-segment: `EDGE-DRIP` | `001`--`099` |
| New variant | `CHEM` | `VAR` | Single segment: `MECHANICAL` | See parent pattern |
| New relationship | `SOUND` | `REL` | Single segment: `ADJACENT` | `001`--`999` |
| New detail intent | `DNA` | `DET` | Single segment: `EDGETERMINATION` | `001`--`999` |
| New artifact intent | `COLOR` | `ART` | Single segment: `SHOPDRW` | `001`--`999` |
| New physical constraint | `TEXTURE` | `CNS` | Single segment: `FLANGEWIDTH` | `001`--`999` |
| New environmental constraint | `CLIMATE` | `CNS` | Single segment: `WINDZONE` | `001`--`999` |
