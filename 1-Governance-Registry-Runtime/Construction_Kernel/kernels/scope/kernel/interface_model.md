# Interface Model

## Purpose

Defines how the Scope Kernel models interface zones -- the physical and contractual boundaries where scope responsibilities meet between trades. Interface zones represent the highest miscoordination risk in building envelope construction.

## Definition

An interface zone is a location where two or more trades' scopes of work physically overlap or adjoin. At an interface zone, the question of "who does what" is most likely to be ambiguous, contested, or undefined.

## Interface Zone Structure

Each interface zone is defined in the shared registry (`interface_zones.json`) and referenced by scope records. The Scope Kernel's responsibility is to:

1. Reference interface zones on scope of work records
2. Assign trade responsibilities at each side of the interface
3. Define sequencing at the interface
4. Attach inspection steps specific to the interface

## Division 07 Interface Zones

### Roof-to-Wall Transition
- **Trades**: Roofing, air barrier, sheet metal, possibly masonry
- **Scope risk**: Who terminates the membrane? Who installs the counter-flashing? Who seals the transition?
- **Required**: Explicit trade assignment on both sides, pre-cover inspection

### Window/Door Perimeter
- **Trades**: Glazing, air barrier, sealant
- **Scope risk**: Who installs the sill pan? Who ties the air barrier to the window frame?
- **Required**: Sequencing (air barrier before window installation), inspection of continuity

### Roof Penetration
- **Trades**: Roofing, MEP trades, firestopping (if rated)
- **Scope risk**: Who seals around the penetration? Who installs the pitch pan or boot?
- **Required**: Sequencing (penetration before membrane), coordination meeting

### Parapet
- **Trades**: Roofing, sheet metal, masonry, air barrier
- **Scope risk**: Membrane termination height, coping attachment, through-wall flashing
- **Required**: Multi-trade coordination, pre-cover inspection

### Below-Grade to Above-Grade Transition
- **Trades**: Waterproofing, air barrier
- **Scope risk**: Lap direction, material compatibility at transition
- **Required**: Continuity inspection, material compatibility review (deferred to Spec Kernel)

### Expansion Joint
- **Trades**: Sealant, roofing, structural
- **Scope risk**: Joint width accommodation, sealant vs. membrane responsibility
- **Required**: Design review of joint sizing (deferred to Assembly Kernel)

## Interface Risk Scoring

The Scope Kernel does not assign numerical risk scores. It classifies interfaces by coordination complexity:
- **Simple**: Two trades, clear boundary, standard detail
- **Complex**: Three or more trades, ambiguous boundary, custom detail required
- **Critical**: Life-safety interface (firestopping, structural waterproofing)

## Miscoordination Prevention

1. Every interface zone must have trade assignments on all sides.
2. Unassigned interfaces are flagged as scope gaps.
3. Interface inspections must be scheduled before concealment.
4. Scope overlap at interfaces triggers human review.
