# Kernel Scope — Construction Assembly Kernel

## Domain Scope

The Construction Assembly Kernel covers the full scope of building enclosure assembly truth for CSI Division 07 — Building Envelope Systems.

## Truth Surfaces

### Assembly Systems

Complete assembly definitions as ordered layer stacks. Each assembly has a type (roof, wall, below-grade, plaza, vegetated, hybrid), a set of layers, and control-layer continuity tracking. Assemblies are the primary organizing unit.

### Assembly Layers

Individual layers within an assembly. Each layer has a position number (1 = outermost), a control-layer assignment, a material reference, and an attachment method. Layers are always defined in context of their parent assembly.

### Assembly Components

Discrete components that participate in assemblies: membranes, insulation boards, cover boards, substrates, fasteners, adhesives, sealants, flashings, edge metals, drains, curbs, vapor retarders, air barriers, and firebreaks.

### Control-Layer Assignments

Mappings between assembly layers and the 11 control layers from the shared registry. A single layer may serve multiple control-layer functions (e.g., a self-adhered membrane serving both bulk water control and air control).

### Transition Conditions

Conditions at each of the 10 interface zones where one assembly type meets another. Transitions track which control layers are maintained, what details are used, and the risk level. Roof-to-wall, parapet, below-grade, and expansion joint transitions are typical examples.

### Penetration Conditions

Conditions where pipes, conduits, structural members, equipment supports, anchors, or vents pass through the building enclosure. Each penetration records which control layers are affected and the seal method used.

### Edge Conditions

Conditions at assembly perimeters: fascia, drip edge, gravel stop, coping, parapet cap, and termination bar. Edge conditions track how control layers are terminated or redirected.

### Tie-In Conditions

Conditions where assemblies connect at construction boundaries: new-to-existing transitions, phased construction joints, and repair boundaries.

### Tested Assembly Records

Records of assemblies validated by testing: fire ratings (NFPA 285, ASTM E119), wind uplift (FM 4470, UL 580), air leakage (ASTM E2357), water penetration (ASTM E331), structural, and thermal performance.

### Continuity Requirements

Rules governing which control layers must be continuous, may be interrupted, must terminate, or must transition at specific boundaries or conditions.

## Scope Boundaries

- Assemblies only — not standalone materials, products, or specifications.
- Division 07 initial focus — expandable to other divisions when kernel family matures.
- Configuration truth — not performance prediction or cost modeling.
