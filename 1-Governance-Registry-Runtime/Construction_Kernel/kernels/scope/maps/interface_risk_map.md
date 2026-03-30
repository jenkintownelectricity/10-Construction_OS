# Interface Risk Map — Construction Scope Kernel

## Purpose

This map documents trade coordination risks at interface zones where scope boundaries overlap or adjoin. Interface zones are the highest-risk areas for scope gaps and construction defects.

## Common Interface Zones

| Interface Zone | Trades Involved | Risk Level | Primary Risk |
|---------------|----------------|------------|--------------|
| roof_to_wall | Roofing, Sheet Metal, Air Barrier | High | Continuity break in air/water control layers |
| parapet_transition | Roofing, Sheet Metal, Masonry | High | Flashing termination and counterflashing coordination |
| penetration | Roofing, Mechanical (excluded), Fireproofing | Medium | Seal continuity around pipes, conduits, supports |
| roof_edge | Roofing, Sheet Metal | Medium | Edge metal sequencing and membrane termination |
| curb_transition | Roofing, Sheet Metal, Mechanical (excluded) | High | Curb flashing height and securement |
| drain_transition | Roofing, Plumbing (excluded) | Medium | Drain clamping ring and membrane integration |
| window_to_wall | Glazing, Air Barrier, Waterproofing | High | Air barrier continuity at frame perimeter |
| foundation_to_wall | Waterproofing, Concrete, Masonry | High | Below-grade to above-grade moisture transition |
| expansion_joint | Multiple trades | Medium | Movement accommodation across control layers |

## Risk Categories

1. **Scope Gap** — No trade is assigned responsibility for a specific interface task.
2. **Scope Overlap** — Multiple trades claim responsibility, creating conflict.
3. **Sequencing Conflict** — Trade A needs access before Trade B is finished.
4. **Control Layer Break** — Air, water, or thermal continuity is interrupted at the interface.

## Mitigation Through Scope Records

- `trade_responsibility.interface_zones` — Each trade declares its interface zone participation.
- `trade_responsibility.inclusions` / `exclusions` — Explicit boundary at each interface.
- `trade_responsibility.coordination_notes` — Sequencing and handoff expectations.
- `inspection_step` with `hold_point: true` — Verification before concealment at interfaces.

## Validation Rules

- Every interface zone MUST appear in at least two trade_responsibility records.
- Inclusions across trades at a shared interface zone MUST NOT have gaps.
- Exclusions across trades at a shared interface zone MUST NOT create orphaned work items.
- Pre-cover inspection hold points SHOULD exist at every high-risk interface zone.

## Principles

- Interface risks are identified through scope analysis, not runtime detection.
- Scope records declare interface participation; risk assessment is performed externally.
- The scope kernel does not calculate or score risk; it provides the data for risk analysis.
