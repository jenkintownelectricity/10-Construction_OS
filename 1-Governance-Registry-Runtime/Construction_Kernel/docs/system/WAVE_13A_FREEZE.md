# Wave 13A Freeze — Detail DNA Baseline

**Status:** FROZEN
**Authority:** Construction_Kernel
**Freeze Date:** 2026-03-20
**Provenance:** Wave 13A confidence pass + hardening patch

## Scope

Wave 13A establishes the canonical Detail DNA layer:
- Deterministic detail classification taxonomy
- Canonical detail identifiers (immutable format)
- Taggable/searchable detail metadata
- Material DNA compatibility links
- Renderer consumption contracts
- Training data generation structures
- Detail relationship graph

## Frozen Artifacts

### Canonical ID Format
```
[SYS]-[CLASS]-[COND]-[VAR]-[ASM]-[NN]
```
Immutable. Future metadata must not alter this structure.

### detail_dna_schema.json
Frozen. Future changes must be additive only (new optional fields). No field removals or type changes.

### 9 Seed Detail Families

| # | Canonical ID | Condition |
|---|---|---|
| 1 | LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01 | Parapet termination |
| 2 | LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01 | Vertical wall termination |
| 3 | LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01 | Pipe penetration |
| 4 | LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01 | Curb penetration |
| 5 | LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01 | Roof drain |
| 6 | LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01 | Scupper |
| 7 | LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01 | Edge metal |
| 8 | LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01 | Expansion joint |
| 9 | LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01 | Roof-to-wall transition |

### Route Graph Baseline
11 edges. Acyclic on depends_on/precedes/blocks/follows. New routes may be added (additive only). Existing relationship types may not be removed or renamed.

### Synonym Policy
Synonyms are additive search aids only. They must never create alternate canonical family identities. Synonym-to-family resolution is many-to-one (multiple synonyms may resolve to the same family).

### Acknowledged Deferrals
- Drain family variant (`COPING`) is an awkward taxonomy fit. Deferred to future wave when variant enum is extended. Canonical ID is immutable and unaffected.

## Checksums (SHA-256)

```
0fc379d648a7eedcf320cab6b0ac8dd4b97163e9d8a3b0d516f1a5a5c97698da  schemas/detail_dna_schema.json
ae7980fa1e42fb43c375efe631645c18db7b1b5eae538e1bf6fadf7fe28be474  schemas/detail_relationship_schema.json
f7ef1c5859200db44a1d135d319714a30b4064caa066bca711f9a16171a9081f  data/detail_tag_index.json
548c409110e4a496061f21c6ce8d5522ffa45fee92f5d075c6601a826f84312d  data/detail_route_index.json
f730f5cbd3419f354dedc4f1d60275b66e99895863c500ccd856d172a0aa648f  data/detail_dna/LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01.json
a7707d02346d59d77690267488408dc52d2beb39db52b94e72291496e94817c1  data/detail_dna/LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01.json
8d696c3aa8f82b3ae029db169e1e91ff57c4c9b5a2838092427df2dc456f7e16  data/detail_dna/LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01.json
186498fac7720444c8879c3ee3e14ce035bbabc8d162d43e274bbd516d8f6081  data/detail_dna/LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01.json
d562e7669d93f4dece6c6ebe79693c92890283afb0a246ce039db0083b183b93  data/detail_dna/LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01.json
20b679d101a765442074e2ae6b9d1dc9e44b91c5834c6cdb6ea870892faa446d  data/detail_dna/LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01.json
384f69dac25da6ced9c23aa2de74722663b413dedae9703ebeb02a448837b4a4  data/detail_dna/LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01.json
ab38ff1f9f46e47290a197be7f67f34576e2bc2aae6b072fe4e1ffc4b1450728  data/detail_dna/LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01.json
3623877cfdd3173333ab582342d81c9679aca162e1a432a134705ef7fcf62e3d  data/detail_dna/LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01.json
```

## Freeze Statement

Wave 13A is frozen as the accepted Detail DNA baseline for downstream Wave 13B work.
