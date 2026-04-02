# DXF Semantic Taxonomy v0.1

## Authority
10-Construction_OS (domain execution plane)

## Purpose
Lock the semantic classification framework for DXF-derived geometry entities. All manufacturer detail ingestion follows this taxonomy.

## Three Ownership Classes

### 1. SYSTEM_OWNED
Geometry belonging to the roofing / waterproofing assembly. These entities represent materials and components that the manufacturer's system is responsible for.

**Examples:**
- Membranes (sheet, fluid-applied, spray-applied)
- Primers and adhesives
- Flashings (base, counter, through-wall)
- Fleece / reinforcement layers
- Topcoats, basecoats, protection courses (when system-owned)
- Cant strips (when part of system)
- Termination bars (when manufacturer-specified)
- Sealants (when system-specified)

**Rule:** If the layer name matches a known product name or system component, classify as SYSTEM_OWNED.

### 2. CONTEXT_ONLY
Geometry shown for readability and installation context but NOT owned by the roofing / waterproofing system.

**Examples:**
- Substrate / structural slab / concrete deck
- Backup wall / masonry / CMU
- Overburden / pavers / ballast (unless system-owned)
- Adjacent construction context
- Steel framing / structural elements
- Insulation (when not system-specified)
- "Others" layer (default classification)

**Rule:** If the layer is not a known system component and is not annotation, classify as CONTEXT_ONLY. "Others" always defaults to CONTEXT_ONLY unless evidence proves otherwise.

### 3. ANNOTATION
Textual, callout, leader, and dimension content. Not geometry.

**Examples:**
- Text / MTEXT entities
- MULTILEADER entities
- Dimension entities
- "Text" layer
- "Defpoints" layer
- Note callouts
- Scale indicators

**Rule:** TEXT, MTEXT, MULTILEADER, and DIMENSION entity types are always ANNOTATION. Layers named "Text", "Defpoints", or similar are ANNOTATION.

## Entity Type Defaults

| Entity Type | Default Class | Override Allowed |
|-------------|--------------|-----------------|
| LWPOLYLINE | SYSTEM_OWNED or CONTEXT_ONLY (by layer) | Yes |
| HATCH | SYSTEM_OWNED or CONTEXT_ONLY (by layer) | Yes |
| LINE | SYSTEM_OWNED or CONTEXT_ONLY (by layer) | Yes |
| ARC | SYSTEM_OWNED or CONTEXT_ONLY (by layer) | Yes |
| CIRCLE | SYSTEM_OWNED or CONTEXT_ONLY (by layer) | Yes |
| TEXT | ANNOTATION | No |
| MTEXT | ANNOTATION | No |
| MULTILEADER | ANNOTATION | No |
| DIMENSION | ANNOTATION | No |
| INSERT | SYSTEM_OWNED or CONTEXT_ONLY (by block name) | Yes |
| SPLINE | SYSTEM_OWNED or CONTEXT_ONLY (by layer) | Yes |

## Default Layer Mappings

| Layer Name Pattern | Default Class | Semantic Role |
|-------------------|--------------|---------------|
| *membrane* / *sheet* | SYSTEM_OWNED | membrane |
| *primer* / *adhesive* | SYSTEM_OWNED | primer_adhesive |
| *flash* / *flashing* | SYSTEM_OWNED | flashing |
| *fleece* / *reinforcement* | SYSTEM_OWNED | reinforcement |
| *topcoat* / *basecoat* | SYSTEM_OWNED | coating |
| *protection course* | SYSTEM_OWNED | protection |
| *cant* / *cant strip* | SYSTEM_OWNED | transition |
| *termination* / *term bar* | SYSTEM_OWNED | termination |
| *sealant* / *caulk* | SYSTEM_OWNED | sealant |
| *substrate* / *slab* / *deck* / *concrete* | CONTEXT_ONLY | substrate |
| *wall* / *masonry* / *cmu* / *backup* | CONTEXT_ONLY | wall |
| *steel* / *framing* / *structural* | CONTEXT_ONLY | structure |
| *overburden* / *paver* / *ballast* | CONTEXT_ONLY | overburden |
| *insulation* / *insul* | CONTEXT_ONLY | insulation |
| *others* | CONTEXT_ONLY | unclassified_context |
| *text* / *defpoints* | ANNOTATION | annotation |

## Enrichment Posture

1. Raw DXF JSON is READ-ONLY — never modified
2. Semantic enrichment is ADDITIVE — stored in separate enrichment records
3. Enrichment references source JSON by file path and entity index
4. Lineage traces back to original DXF file path

## Ambiguity Handling

- If a layer cannot be classified by name pattern → default CONTEXT_ONLY
- If an entity type is unknown → default CONTEXT_ONLY
- Flag ambiguous classifications for operator review
- Never silently promote CONTEXT_ONLY to SYSTEM_OWNED without evidence

## Current State (2026-04-02)

- Config: `config/manufacturer/dxf_semantic_defaults.json`
- Config: `config/manufacturer/ownership_class_defaults.json`
- Schema: `schemas/manufacturer/dxf_semantic_enrichment_record.schema.json`
