# Penetration Model — Construction Assembly Kernel

## Definition

A penetration condition records how an element passes through a building enclosure assembly. Every penetration interrupts one or more control layers and requires a specific seal method to restore continuity. Penetrations are among the highest-risk conditions in any enclosure.

## Penetration Structure

| Property | Required | Description |
|---|---|---|
| penetration_id | Yes | Unique identifier |
| title | Yes | Human-readable description |
| penetration_type | Yes | pipe, conduit, structural, equipment, anchor, vent |
| assembly_ref | Yes | Assembly being penetrated |
| status | Yes | active, draft, deprecated |
| control_layers_affected | No | Control layers interrupted by the penetration |
| seal_method | No | Method used to restore control-layer continuity |
| detail_ref | No | Reference to penetration detail drawing |
| risk_level | No | critical, high, medium, low |

## Penetration Types

### pipe

Plumbing vent pipes, condensate drains, and supply/return piping passing through roof or wall assemblies. Typically sealed with pipe boots (roof) or sleeve-and-sealant (wall).

### conduit

Electrical conduit, cable trays, and communication conduit. Often smaller diameter but may occur in clusters. Sealed with boots, grommets, or firestopping.

### structural

Steel columns, beams, or concrete elements passing through the enclosure. Large penetrations requiring custom flashing and counter-flashing. Often the most difficult to seal.

### equipment

Mechanical equipment supports, ductwork, and exhaust fans mounted through the roof or wall. Typically mounted on curbs that raise the penetration above the membrane plane.

### anchor

Post-installed anchors, handrail supports, and equipment attachment points that penetrate the membrane or air barrier. Small but numerous; each one interrupts control layers.

### vent

Plumbing vents, exhaust vents, and relief vents. Require weatherproof termination above the roof plane.

## Control Layers Affected

A penetration through a roof membrane typically affects:
- bulk_water_control — membrane is cut
- air_control — air barrier is interrupted (if membrane serves as air barrier)
- thermal_control — insulation may be displaced around the penetration
- vapor_control — vapor retarder is cut

The `control_layers_affected` array records which layers are actually interrupted.

## Seal Methods

Common seal methods recorded in the kernel:

| Method | Application |
|---|---|
| pipe_boot | Prefabricated rubber or metal boot sealed to membrane around pipe |
| pitch_pocket | Metal frame filled with sealant or pourable sealer around irregular penetrations |
| curb_mount | Equipment mounted on raised curb; membrane extends up curb |
| sleeve_and_seal | Penetrating element passes through a sleeve; gap sealed with sealant or firestopping |
| field_fabricated_flashing | Sheet metal or membrane flashing custom-fabricated around penetration |
| prefabricated_flashing | Factory-made flashing assembly for standard penetration sizes |

## Penetration Risk Factors

- **Density**: More penetrations per area = higher cumulative risk
- **Size**: Larger penetrations are harder to seal and more susceptible to movement
- **Location**: Penetrations near low points or drainage paths have higher consequence of failure
- **Movement**: Penetrations involving elements that move (thermal expansion of pipes, vibrating equipment) require flexible seals
- **Temperature**: Hot pipes or exhaust vents may degrade adjacent membrane materials

## Penetration Density Thresholds

- < 1 per 100 SF: Low density; standard individual details adequate
- 1-5 per 100 SF: Moderate density; enhanced inspection recommended
- > 5 per 100 SF: High density; consider consolidated curb platform or equipment screen

## Limitations

- The kernel records penetration conditions as configured. It does not prescribe seal methods.
- Seal method effectiveness data belongs to the Reference Intelligence layer.
- Material compatibility between sealants and membranes belongs to the Chemistry Kernel.
