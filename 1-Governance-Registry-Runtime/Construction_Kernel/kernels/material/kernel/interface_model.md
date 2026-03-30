# Interface Model — Construction Material Kernel

## Purpose

This model defines how materials behave at interface zones — locations where two or more materials meet, transition, or interact. The kernel records material-side interface data; assembly-level interface design belongs to the Assembly Kernel.

## Interface Zone Types

Interface zones where material behavior data is relevant:

| Zone | Material Data Required |
|---|---|
| Membrane-to-membrane seam | Weld/adhesion strength, chemical compatibility |
| Membrane-to-flashing transition | Adhesion, differential movement, compatibility |
| Membrane-to-substrate bond | Adhesion to substrate, primer requirements |
| Insulation-to-membrane contact | Chemical compatibility, compressive strength |
| Sealant-to-substrate adhesion | Adhesion, movement capacity, substrate compatibility |
| Vapor retarder laps | Seal strength, permeance at laps |
| Air barrier continuity | Adhesion, elongation at transitions |
| Penetration seals | Sealant compatibility with pipe/conduit materials |
| Expansion joint materials | Elongation, recovery, fatigue resistance |
| Through-wall flashing termination | Adhesion, drip edge compatibility |

## Material Interface Properties

Properties relevant to interface performance:

| Property | Unit | Test Method | Interface Relevance |
|---|---|---|---|
| Peel adhesion | lbf/in | ASTM D903 | Membrane-to-substrate bond |
| Lap shear strength | psi | ASTM D1002 | Membrane seam strength |
| Elongation at break | % | ASTM D412 | Movement accommodation |
| Recovery | % | ASTM D412 | Elastic return after movement |
| Chemical compatibility | enum | Manufacturer guidance | Contact compatibility |

## Interface Compatibility Matrix

The compatibility model captures pairwise interface compatibility. At interface zones, materials must be:

1. **Compatible** — may be placed in direct contact
2. **Conditional** — requires separator, primer, or specific condition
3. **Incompatible** — must not contact; requires physical separation
4. **Untested** — no data available; fail-closed posture applies

## Interface Data Boundaries

| This Kernel Records | Another Kernel Owns |
|---|---|
| Material adhesion values | Assembly detail configuration |
| Material compatibility at contact | Chemical mechanism of interaction |
| Material flexibility properties | Joint design dimensions |
| Material substrate requirements | Substrate preparation procedures |

## Interface Risk Flags

When interface-critical data is missing (e.g., untested compatibility at a common transition), the record carries `ambiguity_flag: true` and is surfaced to the intelligence layer for resolution.
