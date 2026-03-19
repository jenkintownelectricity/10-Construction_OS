# Construction Material Taxonomy

## Purpose

Define the canonical material class vocabulary for the Construction domain. This taxonomy provides the bounded set of material references that assemblies, compositions, compatibility rules, and truth events may use.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Composition Model
    → Material Taxonomy  ← this document
    → Material Compatibility Model
    → Interface Model
    → Scope Boundary Model
    → View Intent Model
    → Construction_Runtime
```

The Material Taxonomy defines what materials exist in the canonical vocabulary. The Composition Model references materials as component properties. The Compatibility Model defines interactions between material classes.

---

## Material Physics Categories

| Category | Description |
|---|---|
| polymer | Synthetic or natural polymer-based materials |
| metal | Ferrous and non-ferrous metals and alloys |
| mineral | Cement,ite,ite, calcium silicate, mineral-based materials |
| organic | Wood, cellulose, natural fiber materials |
| composite | Multi-phase materials combining distinct material physics |
| glass | Silicate-based transparent or translucent materials |
| bituminous | Asphalt and coal-tar derived materials |
| elastomeric | Rubber and synthetic elastomer materials |
| cementite | Cement-bonite composite materials |
| ceramic | Fired clay and sintered mineral materials |

---

## Canonical Material Classes

### Roofing Membranes

| Material Class | Physics | Description |
|---|---|---|
| `tpo_membrane` | polymer | Thermoplastic polyolefin roofing membrane |
| `pvc_membrane` | polymer | Polyvinyl chloride roofing membrane |
| `epdm_membrane` | elastomeric | Ethylene propylene diene monomer rubber membrane |
| `mod_bit_membrane` | bituminous | Modified bitumen sheet membrane |
| `built_up_roofing` | bituminous | Multi-ply built-up roofing membrane |
| `fluid_applied_membrane` | polymer | Liquid-applied waterproofing membrane |
| `spray_foam_roofing` | polymer | Spray polyurethane foam roofing system |

### Metals

| Material Class | Physics | Description |
|---|---|---|
| `galvanized_steel` | metal | Zinc-coated carbon steel |
| `stainless_steel` | metal | Chromium-nickel alloy steel |
| `aluminum_sheet` | metal | Aluminum alloy sheet stock |
| `copper_sheet` | metal | Copper sheet or strip |
| `zinc_sheet` | metal | Zinc sheet or strip |
| `galvalume_steel` | metal | Aluminum-zinc coated steel |
| `painted_steel` | metal | Factory-coated steel with organic finish |
| `lead_sheet` | metal | Lead sheet for flashing applications |

### Insulation

| Material Class | Physics | Description |
|---|---|---|
| `polyiso_insulation` | polymer | Polyisocyanurate rigid board insulation |
| `xps_insulation` | polymer | Extruded polystyrene rigid board insulation |
| `eps_insulation` | polymer | Expanded polystyrene rigid board insulation |
| `mineral_wool_insulation` | mineral | Mineral fiber board or batt insulation |
| `spray_foam_insulation` | polymer | Spray-applied polyurethane foam insulation |
| `perlite_insulation` | mineral | Expanded perlite board insulation |
| `fiberglass_insulation` | glass | Glass fiber batt or board insulation |

### Substrates and Sheathing

| Material Class | Physics | Description |
|---|---|---|
| `steel_deck` | metal | Corrugated steel roof or floor deck |
| `concrete_deck` | cementite | Cast-in-place or precast concrete deck |
| `wood_deck` | organic | Plywood or OSB structural sheathing |
| `gypsum_board` | mineral | Gypsum wallboard or sheathing |
| `cement_board` | cementite | Fiber-reinforced cement board |
| `plywood` | organic | Structural plywood panel |
| `osb` | organic | Oriented strand board panel |
| `lightweight_concrete` | cementite | Lightweight insulating concrete fill |

### Sealants and Adhesives

| Material Class | Physics | Description |
|---|---|---|
| `silicone_sealant` | polymer | Silicone-based joint sealant |
| `polyurethane_sealant` | polymer | Polyurethane-based joint sealant |
| `butyl_sealant` | polymer | Butyl rubber sealant or tape |
| `bituminous_adhesive` | bituminous | Asphalt-based bonding adhesive |
| `urethane_adhesive` | polymer | Urethane-based bonding adhesive |
| `contact_adhesive` | polymer | Contact-bond adhesive |

### Flashings and Accessories

| Material Class | Physics | Description |
|---|---|---|
| `membrane_flashing` | polymer | Prefabricated or field-formed membrane flashing |
| `metal_flashing` | metal | Sheet metal flashing (inherits base metal class) |
| `liquid_flashing` | polymer | Fluid-applied flashing material |
| `bituminous_flashing` | bituminous | Modified bitumen or SBS flashing |
| `peel_stick_membrane` | polymer | Self-adhering membrane sheet |

### Fasteners

| Material Class | Physics | Description |
|---|---|---|
| `steel_fastener` | metal | Carbon steel mechanical fastener |
| `stainless_fastener` | metal | Stainless steel mechanical fastener |
| `insulation_plate` | metal | Stress distribution plate for insulation attachment |

### Vapor and Air Barriers

| Material Class | Physics | Description |
|---|---|---|
| `vapor_retarder_sheet` | polymer | Sheet-type vapor retarder |
| `air_barrier_membrane` | polymer | Air barrier membrane (self-adhered or fluid-applied) |
| `vapor_retarder_coating` | polymer | Coating-type vapor retarder |

---

## Taxonomy Governance

- This taxonomy defines the canonical material class vocabulary for Construction OS.
- New material classes may be admitted through governed determination only.
- Material classes must be grounded in material physics, not manufacturer branding.
- Runtime, VKBUS, and downstream consumers must not invent material classes.
- Manufacturer products map to canonical material classes as external references.

---

## Taxonomy Boundaries

This taxonomy is bounded. It covers construction materials commonly encountered in commercial building envelope and roofing applications. Expansion to other construction domains (structural, MEP, interior) requires governed admission.

The taxonomy is not a product database, manufacturer catalog, or specification library.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Governance doctrine: `Construction_Kernel/docs/governance/construction-material-doctrine.md`
