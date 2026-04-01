# Projection Posture v0.1

**SYSTEM PLANE:** domain_plane
**ROLE:** consume_manufacturer_truth

---

## Projection Purpose

`projection/` contains passive, read-only artifacts that translate
upstream manufacturer truth into formats consumable by Construction_OS
runtime components.

## What Projection Contains

- Detail resolution path mappings (condition -> system -> constraint -> detail)
- Lens definitions for downstream view consumers

## What Projection Does NOT Contain

- Runtime services or execution code
- UI surfaces or rendered views
- Adapters with sovereign behavior
- External sync logic
- Mutation logic that writes back to upstream truth

## Posture

Projection is a passive translation surface. It reads from `truth-cache/`
and `schemas/` and produces mapping artifacts for Construction_OS
runtime consumers. It has no authority of its own.
