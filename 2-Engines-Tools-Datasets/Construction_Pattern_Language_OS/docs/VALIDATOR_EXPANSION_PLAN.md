# Validator Expansion Plan

**Document ID:** CPLOS-GOV-VALIDATOR-001
**Date:** 2026-03-22
**Authority:** Armand Lefebvre, L0
**Status:** IMPLEMENTED

## Overview

This document records the validator expansion performed during the
VKGL03R hardening audit. All validators listed below are implemented
and passing.

## Validator Inventory

### 1. graph_validator.py — EXPANDED

**Status:** Implemented and passing
**Checks performed:**

| Check | Status | Description |
|---|---|---|
| Reference integrity | PASS | All source/target/applies_to/pattern_refs point to existing entities |
| Relationship type validation | PASS | All relationship types are `adjacency`, `conflict`, or `dependency` |
| Self-reference detection | PASS | No entity references itself in a relationship |
| Duplicate ID detection | PASS | No duplicate relationship IDs |
| **Dependency acyclicity** | PASS | Dependency subgraph is a DAG (no circular dependencies) |
| **Adjacency cycles allowed** | PASS | Adjacency relationships may form cycles (bidirectional adjacency is valid) |
| **Conflict symmetry** | PASS | Every conflict A→B has a corresponding B→A |
| **Schema/version compatibility** | PASS | All entities use compatible schema_version and pattern_language_version |
| **Deprecation/index integrity** | PASS | No active entity references a deprecated entity |

**Bugs fixed during hardening:**
- Relationships use nested `source.id`/`target.id`, not flat `source_id`/`target_id` — both formats now supported
- Relationships use `type`, not `relationship_type` — both keys now supported
- `applies_to` may contain dicts with `id` key or plain strings — both formats now handled

### 2. hierarchy_validator.py — STABLE

**Status:** Passing (no changes needed)
**Checks performed:**

| Check | Status | Description |
|---|---|---|
| Pattern-to-family integrity | PASS | Every pattern references an existing family_id |
| Variant-to-pattern integrity | PASS | Every variant references an existing pattern_id |
| Family patterns array | PASS | Every entry in a family's patterns array exists |
| Pattern variants array | PASS | Every entry in a pattern's variants array exists |
| Orphan pattern detection | PASS | No pattern exists outside a family's patterns array |
| Orphan variant detection | PASS | No variant exists outside a pattern's variants array |

### 3. identifier_validator.py — FIXED

**Status:** Implemented and passing
**Checks performed:**

| Check | Status | Description |
|---|---|---|
| Format compliance | PASS | All identifiers match `<CLASS>-CONSTR-<TYPE>-<NAME>-<INDEX>-R<REV>` |
| Class validation | PASS | All classes are in {DNA, CHEM, COLOR, SOUND, TEXTURE, CLIMATE} |
| Type validation | PASS | All types are in {FAM, PAT, VAR, REL, ART, CNS, DTL} |
| Revision validation | PASS | All revisions are >= 1 |
| **Definition uniqueness** | PASS | Each top-level entity ID is defined in exactly one file |

**Bug fixed during hardening:**
- Validator was counting cross-references as duplicate definitions. Now correctly distinguishes entity definitions (top-level `id`) from references in nested structures.

## Validation Results Summary

```
Graph Validation:      53 entities, 8 relationships, 5 artifact intents, 5 constraints → PASS
Hierarchy Validation:  5 families, 10 patterns, 20 variants → PASS
Identifier Validation: 53 files, 84 identifiers (53 definitions) → PASS
```

## Enforcement Model

- **Fail-closed:** Any single validation error fails the entire check
- **Pre-commit gate:** All three validators must pass before any commit to the kernel
- **Consumer gate:** Downstream consumers should run validators before consuming data
