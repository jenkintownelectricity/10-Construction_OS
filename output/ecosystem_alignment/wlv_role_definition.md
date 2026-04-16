# WLV Role Definition

## Role: DESIGN WORKSTATION

10-White-Lightning_Vision_OS is the interactive design workstation for the construction intelligence platform. It is NOT the production detail compiler.

## Capabilities
- Experimental condition creation and exploration
- Parametric assembly sandbox
- Visual geometry inspection (interactive viewport)
- Design exploration with real-time rendering
- System simulation and assembly visualization
- Interactive SVG/DXF/PDF export via web UI

## Rules
1. WLV must NOT own production drawing truth
2. WLV must NOT be the canonical exporter for batch detail generation
3. WLV must remain design-friendly, non-restrictive, sandbox-capable
4. WLV may export interactively for design review purposes
5. Production batch exports are owned by Construction_OS tools/
6. WLV's export renderers (TypeScript) are reference implementations, not canonical

## What WLV Does Well
- Zone-based sheet composition (drawing/callout/titleblock zones)
- Interactive annotation and callout placement
- Real-time geometry editing
- 3D preview rendering
- Detail sheet exporter with material callouts and scale bars

## What WLV Does NOT Do
- Pattern/hatch rendering (no concrete stipple, no insulation hatch)
- Non-crossing leader routing algorithm
- Batch rendering of multiple conditions
- PDF compilation from SVGs
- DXF generation with proper CAD layering

## Relationship to Construction_OS
WLV → (design input) → Construction_OS → (compile) → artifacts
Construction_OS → (geometry JSON) → WLV → (interactive preview)
