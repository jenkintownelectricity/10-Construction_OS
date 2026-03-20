# Mirror Blueprint Principles

## Purpose

These principles govern the creation of visual blueprints — diagrams, architecture maps, flow charts, and structural visualizations — for the mirror integration system. Blueprints are governance artifacts, not decoration. They must communicate structure, boundaries, and relationships with precision.

A blueprint that cannot be understood without a verbal explanation has failed.

---

## Core Principles

### 1. Clarity Over Decoration
Every visual element must serve a communicative purpose. Drop shadows, gradients, textures, and decorative borders are prohibited unless they encode specific meaning. White space is a tool for clarity, not wasted space. If removing a visual element does not reduce understanding, remove it.

**Test:** Can a new team member understand the diagram's key message within 60 seconds? If not, simplify.

### 2. Every Box Has a Purpose
Each bounded region (box, container, group) in a blueprint represents a specific architectural element: a system, a service, a module, a data store, a boundary, or a governance domain. No box exists merely for visual grouping. If a box is present, it must be labeled and its purpose must be immediately apparent.

**Test:** Point to any box and ask "what is this?" If the answer requires more than one sentence, the box is too vague or too overloaded.

### 3. Every Arrow Has a Direction
Arrows represent data flow, control flow, dependency, or temporal sequence. Every arrow must have a clear direction (one-way or explicitly bidirectional). Undirected lines are prohibited — they are ambiguous. The nature of what flows along the arrow must be inferable from context or labeled explicitly.

**Test:** For any arrow, you must be able to answer: "What moves along this arrow, and in which direction?" If you cannot, the arrow is incomplete.

### 4. Color Conveys Meaning Consistently
Color is a semantic channel, not an aesthetic choice. Each color used in a blueprint must have a defined meaning that is consistent across all blueprints in the mirror system. A color legend must be provided on every diagram that uses color. The same color must never mean different things in different diagrams.

**Recommended color semantics:**
- **Blue:** Construction OS core components
- **Green:** Mirror components (active, healthy)
- **Orange/Amber:** Warning states, frozen components, pending actions
- **Red:** Violations, errors, forbidden zones, breakaway triggers
- **Gray:** Retired, disabled, or archived components
- **Purple:** Trust boundaries and governance enforcement points
- **White/Light:** Data flows and schemas

**Test:** Remove all color from the diagram (grayscale). If the diagram becomes ambiguous, color is carrying too much meaning without adequate labeling. Add labels.

### 5. Diagrams Must Stand Alone Without Conversation Context
A blueprint must be fully understandable without access to the conversation, meeting, or document that prompted its creation. This means:

- All systems, services, and components are labeled with their full names
- Acronyms are defined in a legend or spelled out on first use
- The diagram has a title that describes what it shows
- The diagram has a date or version indicator
- Any assumptions or scope limitations are noted on the diagram itself

**Test:** Send the diagram to someone who was not in the room when it was created. Can they understand it? If not, add context.

### 6. Labels Are Explicit
Labels must use precise, unambiguous language. Avoid generic labels like "Service," "Module," "Data," or "Process" without qualification. Every label should answer the question "which one?" Labels must match the terminology used in the kernel documentation — not colloquial or partner-specific terms.

**Good labels:** "Detail Normalization Slice," "GCP Shop Drawing Source," "Parity Verification Engine"
**Bad labels:** "Service A," "The Module," "Data Flow," "Processing"

**Test:** Could two different people read the same label and point to different things? If yes, the label is ambiguous.

### 7. Avoid Ambiguous Groupings
When multiple elements are grouped visually (inside a bounding box, close together, connected by a bracket), the grouping must be semantically meaningful. Proximity on a diagram implies relationship. If elements are close together but unrelated, they must be visually separated. If elements are related but far apart, the relationship must be made explicit with arrows or annotations.

**Grouping rules:**
- Elements inside a trust boundary box are inside that trust boundary
- Elements inside a mirror box are part of that mirror
- Elements inside a core box are part of Construction OS core
- Overlapping groups must have the overlap region explicitly labeled and explained
- Ungrouped elements floating in diagram space must be annotated with their governance context

**Test:** For any two elements that appear close together, ask: "Are these related because of their proximity, or is the proximity accidental?" If accidental, separate them.

---

## Blueprint Types

### Architecture Blueprints
Show the structural relationship between core, mirrors, trust boundaries, and external systems. These are the highest-level diagrams and must emphasize boundaries and ownership.

### Data Flow Blueprints
Show how data moves through the system — from source through reflection to consumption. Every crossing of a trust boundary must be visually marked. Data classification levels should be indicated.

### Lifecycle Blueprints
Show the state transitions of mirrors and slices through their lifecycle stages (PROPOSED → CHARTERED → STAGED → ACTIVE → FROZEN → RETIRED). These are temporal diagrams and must show conditions that trigger each transition.

### Dependency Blueprints
Show the dependency graph between slices, mirrors, and core components. Direction of dependency must be explicit. Circular dependencies must be visually flagged.

### Breakaway Blueprints
Show what happens when a mirror is separated. These diagrams must clearly show which connections are severed, what is archived, and what remains in core.

---

## Anti-Patterns in Blueprints

1. **The Kitchen Sink.** A single diagram that tries to show everything — architecture, data flow, lifecycle, and dependencies simultaneously. Split into multiple focused diagrams.

2. **The Mystery Arrow.** An arrow connecting two elements with no label and no obvious meaning. Every arrow must be interpretable.

3. **The Invisible Boundary.** Core and mirror components mixed together without a clear boundary line. Trust boundaries must always be visually explicit.

4. **The Orphan Element.** A box or label floating in the diagram with no connections to anything. Either connect it or remove it.

5. **The Rainbow Diagram.** Using many colors without a legend or consistent meaning. Colors without semantics are noise.

6. **The Stale Diagram.** A diagram without a date or version that may or may not reflect current architecture. All diagrams must be versioned.

7. **The Conversation Artifact.** A diagram that only makes sense if you were in the meeting where it was drawn. Diagrams must stand alone.

---

## Blueprint Review Checklist

Before a blueprint is considered complete, verify:

- [ ] Every box is labeled with a specific name
- [ ] Every arrow has a direction and an inferable or labeled meaning
- [ ] Colors are used consistently and a legend is provided
- [ ] The diagram has a title, date, and version
- [ ] Trust boundaries are visually explicit
- [ ] The diagram is understandable without external context
- [ ] No decorative elements exist without semantic meaning
- [ ] Groupings are semantically meaningful
- [ ] The diagram type is appropriate for what it shows
- [ ] Terminology matches kernel documentation
