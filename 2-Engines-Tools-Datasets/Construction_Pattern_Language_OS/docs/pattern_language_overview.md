# Construction Pattern Language -- Overview

## What Is a Construction Pattern Language?

A construction pattern language is a structured, canonical vocabulary of construction
patterns organized into families. It encodes repeatable building solutions -- edge metals,
parapets, drains, penetrations, expansion joints -- as formal entities with defined
hierarchies, relationships, constraints, and artifact intents.

Construction_Pattern_Language_OS is the authoritative source of truth for these patterns.
It defines _what_ patterns exist, _how_ they relate to one another, and _what constraints_
govern their use. It does not implement reasoning, runtime behavior, rendering, or
assistant logic. Those concerns belong to downstream consumers.

## Architecture -- Layer Position

```
Universal_Truth_Kernel              (Layer 0 -- Root Doctrine)
  +-- ValidKernel_Patterns          (Infrastructure -- Structural Patterns)
       +-- Construction_Pattern_Language_OS   (Domain Pattern Language)
```

Construction_Pattern_Language_OS sits at the domain kernel layer. It operates within the
truth boundary defined by Universal_Truth_Kernel and inherits structural patterns (not
logic) from ValidKernel_Patterns. Its lineage is FROZEN -- the parent relationship is
immutable and may never be reparented.

## Entity Hierarchy

The pattern language defines a three-tier primary hierarchy and four supporting entity
types.

### Primary Entities

```
PatternFamily
  +-- Pattern
       +-- PatternVariant
```

#### PatternFamily

A PatternFamily is the top-level grouping. A family represents a broad category of
construction details that share a common domain and purpose. Each family owns one or
more child Patterns.

| Family | Domain | Covers |
|--------|--------|--------|
| Roof Edge | envelope | Drip edges, gravel stops, fascia metals, coping terminations |
| Parapet | envelope | Parapet caps, wall copings, through-wall flashings |
| Roof Drain | envelope | Internal drains, scuppers, overflow systems, conductor heads |
| Pipe Penetration | envelope | Pipe boots, pitch pockets, curb flashings, conduit seals |
| Expansion Joint | structural | Roof expansion joints, wall joints, structural movement joints |

Each family carries a `DNA`-class identifier (e.g., `DNA-CONSTR-FAM-EDGE-001-R1`) and
lists its child patterns by canonical ID in the `patterns` array. The `domain` field
records the building system the family belongs to (envelope, structural, etc.).

#### Pattern

A Pattern is a specific, canonical construction pattern within a family. A pattern
encodes a repeatable building solution for a defined problem. It references its parent
family via `family_id` and lists one or more child variants in its `variants` array.

Examples within the Roof Edge family:

- **Drip Edge** -- Angled metal flashing installed at eaves and rakes to direct water
  away from fascia and into gutters. Typically an L-shaped or T-shaped profile with a
  kick-out hem at the lower edge.
- **Gravel Stop** -- L-shaped metal edge that retains aggregate on built-up or ballasted
  roof systems while providing a finished termination at the roof perimeter.

Each pattern carries a `DNA`-class identifier with a multi-segment name that embeds its
family context (e.g., `DNA-CONSTR-PAT-EDGE-DRIP-001-R1`). Patterns may optionally
reference artifact intents (`artifact_intent_refs`) and constraint profiles
(`constraint_profile_refs`) by canonical ID.

#### PatternVariant

A PatternVariant is a concrete material or method variation of a pattern. Variants
capture the specific materials, fastening methods, gauges, dimensions, and manufacturer
references that differentiate one installation approach from another.

Examples for the Drip Edge pattern:

- **Mechanical Fastening** -- Drip edge secured with exposed or concealed fasteners
  through a nailing hem to the roof deck or fascia board.
- **Adhered** -- Drip edge bonded to substrate using roofing adhesive, peel-and-stick
  membrane, or hot-applied bitumen.

Each variant carries a `CHEM`-class identifier (e.g., `CHEM-CONSTR-VAR-MECHANICAL-101-R1`)
and references its parent pattern via `pattern_id`. Required fields include `method`
(the construction technique) and `materials` (a list of material objects with name, role,
and specification). Optional fields include `dimensional_constraints` and
`manufacturer_refs`.

### Supporting Entities

#### PatternRelationship

PatternRelationship defines how patterns and variants relate to each other within the
language. Relationships are directed: they have a `source_id` and a `target_id`. They
are stored under `pattern_relationships/` in subdirectories by classification.

| Classification | Relationship Type | Meaning | Example |
|---------------|-------------------|---------|---------|
| `adjacency` | `adjacent_to` | Physically adjacent on the building | Drip edge adjacent to gutter |
| `adjacency` | `terminates_at` | Membrane or flashing ends at this element | Roof membrane terminates at edge metal |
| `adjacency` | `transitions_to` | One detail transitions into another | Drip edge transitions to rake edge |
| `adjacency` | `seals_against` | Creates a weathertight seal | Pipe boot seals against roof membrane |
| `adjacency` | `drains_into` | Water flow path between elements | Scupper drains into conductor head |
| `adjacency` | `penetrates` | Passes through another assembly | Conduit penetrates roof assembly |
| `conflict` | `conflicts_with` | Cannot coexist at the same location | Gravel stop conflicts with drip edge at same edge |
| `dependency` | `depends_on` | Requires another pattern to be present | Edge metal depends on membrane termination |

Each relationship uses a `SOUND`-class identifier (e.g., `SOUND-CONSTR-REL-ADJACENT-001-R1`).
The `conditions` array optionally describes when the relationship applies.

#### DetailIntent

DetailIntent declares the design intent for a construction detail -- what problem the
detail solves, what performance criteria it must meet, and what the acceptable tolerance
ranges are. Uses `DNA`-class identifiers with the `DET` type code (e.g.,
`DNA-CONSTR-DET-EDGETERMINATION-001-R1`).

DetailIntent is a semantic declaration, not an executable specification. It tells
downstream consumers _why_ a detail exists and _what_ it is supposed to accomplish,
without prescribing _how_ to verify or render it.

#### ArtifactIntent

ArtifactIntent declares what documentation artifacts a pattern should produce. Each
artifact intent references one or more patterns by canonical ID and specifies:

- `artifact_type` -- One of: `shop_drawing`, `specification`, `submittal`, `inspection`
- `pattern_refs` -- Which patterns this artifact covers
- `output_format` -- Optional preferred format (PDF, DWG, CSV, IFC)
- `required_fields` -- Optional list of data points the artifact must contain

| Artifact Type | Real-World Equivalent |
|---------------|----------------------|
| `shop_drawing` | Fabrication and installation drawings sent to the sheet metal shop |
| `specification` | Written performance and material specs (CSI format, Section 07 62 00) |
| `submittal` | Product data, samples, and certifications submitted for architect approval |
| `inspection` | Field verification checklists used by the quality assurance inspector |

Artifact intents use `COLOR`-class identifiers (e.g., `COLOR-CONSTR-ART-SHOPDRW-001-R1`).

#### ConstraintProfile

ConstraintProfile defines constraints that govern a pattern's applicability. Each
constraint profile references one or more patterns and specifies measurable parameters
and thresholds.

| Constraint Type | Class | Example |
|----------------|-------|---------|
| `manufacturer` | `TEXTURE` | Manufacturer-specific hem width, sealant type, or fastener spacing |
| `code` | `TEXTURE` | IBC wind uplift requirements, FM Global 1-90 compliance |
| `dimensional` | `TEXTURE` | Minimum 4-inch flange width, 24-gauge minimum thickness |
| `environmental` | `CLIMATE` | Wind zone rating, climate zone, exposure category |

Physical constraints (manufacturer, code, dimensional) use `TEXTURE`-class identifiers.
Environmental constraints use `CLIMATE`-class identifiers.

The `parameters` object holds key-value pairs for specific constraint values. The
`thresholds` object defines `min`, `max`, `unit`, and optional `warning_threshold`.

## How Patterns Map to Real Construction

Every entity in the pattern language corresponds to a real-world construction element.
The mapping is intentional and direct:

| Pattern Language Entity | Real-World Equivalent |
|------------------------|----------------------|
| PatternFamily: Roof Edge | The full category of roof edge conditions on a building |
| Pattern: Drip Edge | A specific type of edge metal installed at eaves and rakes |
| Pattern: Gravel Stop | An L-shaped perimeter metal retaining ballast or aggregate |
| PatternVariant: Mechanical Fastening | Drip edge secured with nails or screws through a hem |
| PatternVariant: Adhered | Drip edge bonded with adhesive or peel-and-stick strip |
| PatternVariant: Extruded Aluminum | Gravel stop manufactured by aluminum extrusion |
| PatternVariant: Formed Metal | Gravel stop brake-formed from sheet metal stock |
| PatternRelationship: terminates_at | Physical condition where membrane stops at edge metal |
| PatternRelationship: conflicts_with | Gravel stop and drip edge cannot occupy the same edge |
| ArtifactIntent: shop_drawing | The fabrication drawing sent to the sheet metal shop |
| ArtifactIntent: specification | Section 07 62 00 spec for sheet metal flashing and trim |
| ConstraintProfile: dimensional | Minimum 4-inch flange width required by code or manufacturer |
| ConstraintProfile: environmental | Wind uplift rating for ASCE 7 exposure category |

The language does not model geometry, generate drawings, or simulate behavior. It defines
the canonical identity and relationships of these construction elements so that downstream
consumers (Construction_Kernel, Construction_Runtime, renderers) can reference them by
stable, immutable IDs.

## Identifier System

All entities use natural-system identifiers following the format:

```
<CLASS>-CONSTR-<TYPE>-<NAME>-<INDEX>-R<REV>
```

See [identifier_conventions.md](identifier_conventions.md) for the complete specification,
including class-to-type mapping, naming rules, index allocation, and regex patterns.

## Starter Pattern Families

The kernel ships with five starter families:

1. **Roof Edge** -- Edge metal, membrane terminations, drip edges, gravel stops
2. **Parapet** -- Parapet caps, wall copings, through-wall flashings
3. **Roof Drain** -- Internal drains, scuppers, overflow systems
4. **Pipe Penetration** -- Pipe boots, pitch pockets, curb flashings
5. **Expansion Joint** -- Roof expansion joints, wall control joints

See `examples/edge_metal/` for a fully worked example of the Roof Edge family with
patterns, variants, and supporting entities.

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
- Root-level doctrine (that belongs to Universal_Truth_Kernel)

## Governance Rules

1. Variants belong to exactly one pattern.
2. Patterns belong to exactly one family.
3. Relationships reference canonical IDs only.
4. IDs are immutable once assigned.
5. IDs are unique across the entire kernel.
6. All cross-entity references use full canonical identifier strings.
7. Deprecated entities are preserved, never deleted or reassigned.
8. Every entity must include `schema_version`, `pattern_language_version`,
   `entity_revision`, and `created_at`.
