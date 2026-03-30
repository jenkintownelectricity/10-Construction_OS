# Chemistry Kernel Geometry Posture

## Purpose

Defines how the Chemistry Kernel addresses the relationship between joint geometry and sealant chemistry performance without owning geometric data.

## Geometry Effects on Chemistry

### Joint Width and Depth
- **Width-to-depth ratio** affects sealant cure and movement capability. Proper ratio (typically 2:1) ensures the sealant cures correctly and distributes stress through cohesive body rather than at adhesion surfaces.
- **Excessive depth** in moisture-cure sealants prevents full cure at depth. Silicone moisture cure proceeds from surface inward; deep joints may never fully cure at the bond line.
- **Backer rod chemistry** must be compatible with sealant. Closed-cell polyethylene backer rod is standard; open-cell can outgas and cause bubbling in some sealants.

### Joint Configuration
- **Butt joints** place adhesion surfaces parallel to movement direction — maximum stress on adhesion.
- **Lap joints** distribute shear across the adhesion surface — different adhesion stress profile.
- **Fillet joints** have three-sided adhesion which restricts sealant movement — generally avoided for moving joints.

### Substrate Surface Geometry
- **Surface roughness** affects mechanical adhesion. Rough concrete provides better adhesion than smooth steel for most sealants.
- **Porosity** affects primer penetration. Porous substrates may require different primer chemistry than non-porous substrates.
- **Joint angle** at transitions affects sealant bead geometry and cure profile.

## What This Kernel Records

- Adhesion rules reference substrate types which imply surface geometry characteristics
- Cure mechanism limitations that are geometry-dependent (depth-of-cure limits)
- Incompatibility rules for backer rod materials with sealant chemistries

## What This Kernel Does NOT Own

- Joint dimension specifications (Assembly Kernel)
- Movement calculations (Assembly Kernel)
- Geometric tolerances (Material Kernel)
- Detail drawings (Assembly Kernel)

## Boundary

This kernel records the chemistry facts that geometry-dependent decisions consume. The geometry itself — dimensions, tolerances, movement ranges — belongs to the Assembly and Material Kernels.
