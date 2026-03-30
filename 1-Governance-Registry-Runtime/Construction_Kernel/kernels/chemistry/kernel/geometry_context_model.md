# Geometry Context Model

## Purpose

Records how joint geometry and substrate configuration affect sealant chemistry performance. This kernel owns the chemistry implications; dimensional specifications belong to the Assembly and Material Kernels.

## Joint Geometry and Chemistry

### Width-to-Depth Ratio
- **Standard rule:** 2:1 width-to-depth ratio for field-molded sealants
- **Chemistry reason:** Proper ratio ensures the sealant's cohesive body absorbs movement rather than concentrating stress at adhesion surfaces
- **Excessive depth:** In moisture-cure systems, limits cure penetration. Silicone moisture cure proceeds from the exposed surface inward at approximately 2mm per 24 hours. A 25mm deep joint may take 12+ days for full depth cure.
- **Insufficient depth:** Sealant cross-section too thin to distribute movement stress; cohesive failure risk

### Joint Width and Movement
- **Chemistry implication:** Sealant chemistry determines movement capability (±25% for urethane, ±50% for silicone). Joint width must accommodate design movement within that capability.
- **This kernel provides:** Movement capability as a chemistry property of the polymer family
- **Assembly kernel determines:** Required joint width based on movement calculation

### Backer Rod Geometry
- **Chemistry concern:** Backer rod material and diameter affect cure and compatibility
- **Closed-cell polyethylene:** Standard — prevents three-sided adhesion, compatible with most sealants
- **Open-cell polyurethane:** Risk of outgassing into uncured sealant, causing bubbles
- **Bond-breaker tape:** Used for shallow joints where backer rod won't fit

### Substrate Surface Profile
- **Smooth surfaces (glass, metal):** Require chemical adhesion — primer may be needed
- **Rough surfaces (concrete, masonry):** Provide mechanical adhesion enhancement
- **Porous surfaces:** Primer penetration depth affects adhesion quality
- **Coated surfaces:** Adhesion is to the coating, not the substrate — coating adhesion becomes the weak link

## Fillet Joints vs. Bridge Joints
- **Fillet (three-sided):** Sealant adheres to three surfaces — restricts movement, causes cohesive failure. Avoid for movement joints.
- **Bridge (two-sided):** Sealant adheres to two opposing surfaces with backer rod or bond breaker — allows movement

## Data Representation

Geometry context influences chemistry records indirectly:
- Adhesion rules reference substrate types with implicit surface characteristics
- Cure mechanisms include depth-of-cure limitations
- Incompatibility rules cover backer rod material interactions
- Chemistry model records movement capability as a polymer family property
