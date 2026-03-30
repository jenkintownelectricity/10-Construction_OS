# Pattern Authoring Guide

This guide walks through adding a complete new pattern family to
Construction_Pattern_Language_OS, from initial planning through validation.

## Prerequisites

- Read `docs/pattern_language_overview.md` to understand the entity hierarchy.
- Read `docs/identifier_conventions.md` to understand the ID system.
- Review the JSON schemas in `schemas/` for the exact required and optional fields.
- Review the worked example in `examples/edge_metal/` to see a complete family.

## Step 1: Plan the Family

Before creating any files, answer these questions:

1. **Family name** -- What is the canonical name? (e.g., "Roof Edge", "Parapet")
2. **Domain** -- What building system does it belong to? (e.g., envelope, structural)
3. **Patterns** -- What are the distinct patterns within the family? Aim for at least 2.
4. **Variants per pattern** -- What material or method variations exist for each pattern?
   Aim for at least 2 per pattern.
5. **Relationships** -- How do the patterns relate to each other and to patterns in other
   families? (adjacency, conflict, dependency)

## Step 2: Assign Identifiers

Use the identifier conventions to assign IDs for every entity you plan to create.
Do this before writing any YAML files -- all cross-references depend on these IDs.

### Family ID

Format: `DNA-CONSTR-FAM-<NAME>-<INDEX>-R1`

Check existing families to determine the next available INDEX. If the highest existing
family index is `005`, your new family should use `006`.

Example: `DNA-CONSTR-FAM-GUTTER-006-R1`

### Pattern IDs

Format: `DNA-CONSTR-PAT-<FAMILY_NAME>-<PATTERN_NAME>-<INDEX>-R1`

The NAME segment embeds the family context (e.g., `GUTTER-BOX` for a box gutter
pattern in the Gutter family). Indices start at `001` within the family.

Examples:
- `DNA-CONSTR-PAT-GUTTER-BOX-001-R1`
- `DNA-CONSTR-PAT-GUTTER-HALFROUND-002-R1`

### Variant IDs

Format: `CHEM-CONSTR-VAR-<NAME>-<INDEX>-R1`

Index ranges encode the parent pattern:
- First pattern's variants: `101`--`199`
- Second pattern's variants: `201`--`299`
- Third pattern's variants: `301`--`399`

Examples:
- `CHEM-CONSTR-VAR-COPPER-101-R1` (variant of first pattern)
- `CHEM-CONSTR-VAR-GALVANIZED-102-R1` (variant of first pattern)
- `CHEM-CONSTR-VAR-ALUMINUM-201-R1` (variant of second pattern)

### Relationship IDs

Format: `SOUND-CONSTR-REL-<NAME>-<INDEX>-R1`

Check the global relationship index to determine the next available number.

### Artifact Intent IDs

Format: `COLOR-CONSTR-ART-<NAME>-<INDEX>-R1`

### Constraint Profile IDs

Format: `TEXTURE-CONSTR-CNS-<NAME>-<INDEX>-R1` (physical)
Format: `CLIMATE-CONSTR-CNS-<NAME>-<INDEX>-R1` (environmental)

## Step 3: Create the PatternFamily YAML File

Place the file in `pattern_language/pattern_families/`.

Naming convention: `<family_name>_family.yaml` (lowercase, underscores).

Required fields:
- `id` -- The DNA-class family ID
- `name` -- Human-readable name
- `description` -- What this family covers, its scope and purpose
- `schema_version` -- `"1.0.0"`
- `pattern_language_version` -- `"1.0.0"`
- `entity_revision` -- `1` for new entities
- `created_at` -- ISO 8601 timestamp
- `domain` -- Building system (envelope, structural, mechanical, electrical)
- `patterns` -- Array of child pattern IDs (must match actual pattern files)

Optional fields:
- `detail_intents` -- Array of high-level design intent descriptions
- `notes` -- Free-form commentary

Example:

```yaml
id: "DNA-CONSTR-FAM-EDGE-001-R1"
name: "Roof Edge"
description: >
  Pattern family for roof edge metal termination details. Covers drip edges,
  gravel stops, fascia metals, and coping terminations at the perimeter of
  low-slope and steep-slope roof systems.
schema_version: "1.0.0"
pattern_language_version: "1.0.0"
entity_revision: 1
created_at: "2026-03-22T00:00:00Z"
domain: "envelope"
patterns:
  - "DNA-CONSTR-PAT-EDGE-DRIP-001-R1"
  - "DNA-CONSTR-PAT-EDGE-GRAVELSTOP-002-R1"
detail_intents:
  - "Provide weathertight termination at roof perimeter"
  - "Direct water away from fascia and into gutter system"
  - "Retain aggregate or ballast on built-up roof systems"
```

## Step 4: Create Pattern YAML Files

Place each file in `pattern_language/patterns/`.

Naming convention: `<family>_<pattern>.yaml` (lowercase, underscores).

Required fields:
- `id` -- The DNA-class pattern ID
- `name` -- Human-readable name
- `description` -- What this pattern does, the problem it solves, the solution it provides
- `schema_version` -- `"1.0.0"`
- `pattern_language_version` -- `"1.0.0"`
- `entity_revision` -- `1`
- `created_at` -- ISO 8601 timestamp
- `family_id` -- Canonical ID of the parent PatternFamily
- `variants` -- Array of child variant IDs

Optional fields:
- `detail_intents` -- Array of specific design intent descriptions
- `artifact_intent_refs` -- Array of ArtifactIntent IDs
- `constraint_profile_refs` -- Array of ConstraintProfile IDs

## Step 5: Create PatternVariant YAML Files

Place each file in `pattern_language/pattern_variants/`.

Naming convention: `<pattern>_<variant>.yaml` (lowercase, underscores).

Required fields:
- `id` -- The CHEM-class variant ID
- `name` -- Human-readable name
- `description` -- How this variant differs from others, when to use it
- `schema_version` -- `"1.0.0"`
- `pattern_language_version` -- `"1.0.0"`
- `entity_revision` -- `1`
- `created_at` -- ISO 8601 timestamp
- `pattern_id` -- Canonical ID of the parent Pattern
- `method` -- The construction technique (e.g., "mechanical_fastening", "adhesive_bond")
- `materials` -- Array of material objects, each with at least a `name` field

Optional fields:
- `dimensional_constraints` -- Object with min/max thickness, width, height, tolerance
- `manufacturer_refs` -- Array of manufacturer names
- `notes` -- Free-form notes

### Materials Array

Each entry in the `materials` array is an object with:
- `name` (required) -- Material name (e.g., "26-gauge galvanized steel")
- `specification` (optional) -- Standard reference (e.g., "ASTM A653/A653M")
- `role` (optional) -- Functional role (e.g., "edge_flashing", "fastener", "sealant")

## Step 6: Define Relationships

Place each file in the appropriate subdirectory under `pattern_relationships/`:
- `adjacency_rules/` for adjacency, terminates_at, transitions_to, seals_against,
  drains_into, penetrates
- `conflict_rules/` for conflicts_with
- `dependency_rules/` for depends_on

Required fields:
- `id` -- The SOUND-class relationship ID
- `name` -- Human-readable name
- `description` -- What the relationship means in construction terms
- `schema_version`, `pattern_language_version`, `entity_revision`, `created_at`
- `relationship_type` -- One of: `adjacency`, `conflict`, `dependency`
- `source_id` -- Canonical ID of the source entity
- `target_id` -- Canonical ID of the target entity

Optional fields:
- `conditions` -- Array of condition strings describing when the relationship applies
- `notes` -- Free-form commentary

## Step 7: Define Artifact Intents (Optional)

Place each file in the appropriate subdirectory under `artifact_intents/`:
- `shop_drawing/`, `specification/`, `submittal/`, `inspection/`

Required fields:
- `id` -- The COLOR-class artifact intent ID
- `name`, `description`
- `schema_version`, `pattern_language_version`, `entity_revision`, `created_at`
- `artifact_type` -- One of: `shop_drawing`, `specification`, `submittal`, `inspection`
- `pattern_refs` -- Array of pattern IDs this artifact covers

Optional fields:
- `output_format` -- Preferred format (PDF, DWG, CSV, IFC)
- `required_fields` -- Array of data point names
- `notes`

## Step 8: Define Constraint Profiles (Optional)

Place each file in the appropriate subdirectory under `constraint_profiles/`:
- `manufacturer/`, `code/`, `dimensional/`, `environmental/`

Required fields:
- `id` -- The TEXTURE-class or CLIMATE-class constraint ID
- `name`, `description`
- `schema_version`, `pattern_language_version`, `entity_revision`, `created_at`
- `constraint_type` -- One of: `manufacturer`, `code`, `dimensional`, `environmental`
- `applies_to` -- Array of pattern IDs this constraint governs

Optional fields:
- `parameters` -- Key-value pairs for specific constraint values
- `thresholds` -- Object with `min`, `max`, `unit`, `warning_threshold`
- `notes`

## Step 9: Validate

Run all three validators after creating or modifying any entities. All validators must
pass before your changes are considered valid.

```bash
python validators/identifier_validator.py
python validators/hierarchy_validator.py
python validators/graph_validator.py
```

### What Each Validator Checks

| Validator | Checks |
|-----------|--------|
| `identifier_validator.py` | ID format matches regex; class-type agreement; no duplicate IDs |
| `hierarchy_validator.py` | Every pattern references a valid family; every variant references a valid pattern; parent entities list their children |
| `graph_validator.py` | All relationship source/target IDs reference existing entities; no orphaned relationships; no self-referencing relationships |

### Common Validation Failures

| Failure | Cause | Fix |
|---------|-------|-----|
| "ID does not match pattern" | Typo in identifier format | Check CLASS, TYPE, NAME, INDEX, REV segments |
| "Class-type mismatch" | Wrong CLASS for the entity type | Consult the class-type mapping table |
| "Duplicate ID" | Two entities share the same identifier | Assign a unique INDEX or NAME |
| "Missing parent" | Pattern references a family that does not exist | Create the family file first |
| "Orphaned variant" | Variant references a pattern that does not exist | Create the pattern file first |
| "Dangling reference" | Relationship references a nonexistent entity | Verify source_id and target_id |

## Naming Conventions Summary

| Entity | File Location | File Name Convention |
|--------|--------------|---------------------|
| PatternFamily | `pattern_language/pattern_families/` | `<family>_family.yaml` |
| Pattern | `pattern_language/patterns/` | `<family>_<pattern>.yaml` |
| PatternVariant | `pattern_language/pattern_variants/` | `<pattern>_<variant>.yaml` |
| PatternRelationship | `pattern_relationships/<type>_rules/` | `<descriptive_name>.yaml` |
| ArtifactIntent | `artifact_intents/<artifact_type>/` | `<descriptive_name>.yaml` |
| ConstraintProfile | `constraint_profiles/<constraint_type>/` | `<descriptive_name>.yaml` |

## Checklist

Before submitting a new pattern family, verify:

- [ ] Family YAML file exists in `pattern_language/pattern_families/`
- [ ] At least 2 pattern YAML files exist in `pattern_language/patterns/`
- [ ] At least 2 variant YAML files per pattern exist in `pattern_language/pattern_variants/`
- [ ] Family `patterns` array lists all child pattern IDs
- [ ] Each pattern `family_id` references the correct family
- [ ] Each pattern `variants` array lists all child variant IDs
- [ ] Each variant `pattern_id` references the correct pattern
- [ ] All IDs follow the identifier conventions (class-type agreement, format, uniqueness)
- [ ] All cross-references use full canonical ID strings
- [ ] `schema_version`, `pattern_language_version`, `entity_revision`, `created_at` are present on every entity
- [ ] `python validators/identifier_validator.py` passes
- [ ] `python validators/hierarchy_validator.py` passes
- [ ] `python validators/graph_validator.py` passes
