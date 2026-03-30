# Trade Responsibility Model

## Purpose

Defines the trade-to-scope mapping model. Trade responsibility records assign specific trades to specific scope items, with explicit inclusions, exclusions, and interface coordination requirements. Trade responsibility at interfaces is the most critical scope coordination challenge.

## Definition

A trade responsibility record assigns a single trade to a portion of a scope of work. It defines what that trade includes in their work, what they exclude, and which interface zones require coordination with other trades.

## Trade Enumeration

| Trade | Typical CSI Sections | Division 07 Role |
|---|---|---|
| `roofing` | 07 50 00 | Membrane roofing systems |
| `waterproofing` | 07 10 00 | Below-grade and above-grade waterproofing |
| `sheet_metal` | 07 60 00 | Copings, flashing, gutters, downspouts |
| `glazing` | 08 40 00+ | Windows, curtain wall (Division 08 interface) |
| `masonry` | 04 20 00+ | Masonry walls (Division 04 interface) |
| `concrete` | 03 30 00+ | Concrete substrates (Division 03 interface) |
| `steel` | 05 10 00+ | Structural steel (Division 05 interface) |
| `insulation` | 07 21 00 | Thermal insulation installation |
| `air_barrier` | 07 27 00 | Air barrier systems |
| `fireproofing` | 07 81 00, 07 84 00 | Spray fireproofing, firestopping |
| `sealant` | 07 92 00 | Joint sealants |
| `general_contractor` | Multiple | General conditions, coordination |

## Interface Coordination

The most critical aspect of trade responsibility is coordination at interfaces. Common coordination failures:

### Responsibility Gaps
No trade claims responsibility for work at the interface. Example: who installs the sealant bead between the window frame and the air barrier membrane?

### Responsibility Overlaps
Multiple trades claim the same work item. Example: both the roofing contractor and the sheet metal contractor believe they install the edge metal.

### Sequencing Miscommunication
Trades arrive at the interface at the wrong time. Example: the insulation installer covers the air barrier before the pre-cover inspection.

## Coordination Notes

Trade responsibility records carry a `coordination_notes` field for documenting specific coordination requirements at interface zones. These notes are scope truth -- they define required coordination actions.

## Schema Reference

See `schemas/trade_responsibility.schema.json` for the formal schema definition.
