# Interface Risk Posture

## Purpose

Defines how the Scope Kernel treats interface zones as the highest-risk locations for scope miscoordination. Interface risk is a scope-domain concern because it arises where trade responsibilities meet.

## Principle

Every interface zone is a potential scope gap. The Scope Kernel assumes interface risk is present until explicitly resolved by trade responsibility assignments on both sides of the boundary.

## Risk Categories

### 1. Unassigned Interface
No trade has explicit responsibility for work at the interface. This is the highest-risk condition. The kernel flags it as a blocking scope gap.

### 2. Single-Sided Assignment
Only one trade is assigned at an interface that requires coordination from two or more trades. The kernel flags the missing assignment.

### 3. Overlapping Assignment
Multiple trades claim responsibility for the same interface work. The kernel flags the overlap for human resolution.

### 4. Sequencing Conflict
Two trades require access to the same interface zone at the same time, or predecessor/successor relationships are undefined. The kernel flags the sequencing gap.

## Interface Zone Categories (Division 07)

| Interface Zone | Trades Involved | Typical Risk |
|---|---|---|
| Roof-to-wall transition | Roofing, sheet metal, air barrier | Membrane termination responsibility |
| Window/door perimeter | Glazing, air barrier, sealant | Continuity of air and water barrier |
| Penetration sealing | MEP trades, roofing, firestopping | Sequencing of seal vs. penetration |
| Parapet cap | Roofing, sheet metal, masonry | Flashing lap and termination |
| Expansion joint | Sealant, structural, roofing | Movement accommodation |
| Below-grade to above-grade | Waterproofing, air barrier | Transition of control layers |

## Risk Mitigation Through Scope

1. Every interface zone must have explicit trade assignments on all sides.
2. Every interface zone must have a defined installation sequence.
3. Pre-cover inspection steps must be tied to interface zones.
4. Scope gaps at interfaces are never auto-resolved -- they require human review.

## Relationship to Other Kernels

Interface risk posture defines WHERE risk exists (scope domain). It does not define HOW to detail the interface (Assembly Kernel) or WHAT materials to use (Spec Kernel).
