# Interface Model — Construction Specification Kernel

## Purpose

This model defines how specifications address interface zones — the transitions and connections between different building envelope systems where control layer continuity is most vulnerable.

## Interface Zones

The ten canonical interface zones are defined in `shared/interface_zones.json`:

- **roof_to_wall** — where roofing meets vertical wall assembly
- **parapet_transition** — where roof membrane terminates at parapet
- **penetration** — where pipes, conduits, or equipment pass through the envelope
- **fenestration_edge** — perimeter of windows, doors, curtain wall frames
- **below_grade_transition** — where above-grade wall meets below-grade waterproofing
- **expansion_joint** — designed movement joints between building sections
- **deck_to_wall** — where horizontal deck meets vertical wall
- **roof_edge** — perimeter edge including fascia, drip edge, coping
- **curb_transition** — where roof membrane transitions over equipment curbs
- **drain_transition** — where membrane connects to roof drains and scuppers

## How Specs Address Interfaces

Specification sections address interface zones through:

### Explicit Interface Requirements
Direct requirements for materials, methods, and performance at transitions. Example: "Extend membrane roofing minimum 8 inches above finished roof surface at roof-to-wall transitions."

### Referenced Details
Requirements to comply with details shown on drawings. The kernel records the requirement; the detail lives in the drawing set (outside kernel scope).

### Manufacturer Requirements
Requirements to follow manufacturer's published details for transitions. Recorded with `ambiguity_flag: true` if the manufacturer is not specified.

### Cross-Section Coordination
Requirements that reference another specification section for interface work. Example: Section 07 54 00 references Section 07 62 00 for sheet metal counter-flashing at roof-to-wall transitions.

## Interface Coverage Assessment

For each specification section, the kernel can assess interface coverage by checking whether the section's `control_layers_served` have corresponding requirements at each relevant interface zone. Missing coverage is flagged but not inferred.

## Interface Risk

Specification gaps at interfaces create the highest risk for building envelope failures. The kernel flags these gaps through:

1. `interface_zones` field on requirements — identifies which zone a requirement addresses
2. Absence of interface-specific requirements — flagged as gaps
3. `ambiguity_flag` — set when interface requirements are vague or incomplete

## Multi-Section Interfaces

Many interface zones require coordination across multiple specification sections. The roof-to-wall transition may involve:

- 07 54 00 (membrane roofing — base flashing)
- 07 62 00 (sheet metal — counter-flashing)
- 07 27 00 (air barrier — continuity at transition)
- 07 92 00 (sealants — joint treatment)

Each section records its own interface requirements. Cross-section gap identification is performed by the intelligence layer.
