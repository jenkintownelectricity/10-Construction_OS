# Chemistry Model

## Purpose

Defines the Chemical System object — the central entity in the Chemistry Kernel. A chemical system represents a formulated chemistry used in building envelope construction.

## Object Definition

A Chemical System is a formulated product chemistry characterized by:
- **Polymer base** — the primary polymer (references Polymer Family)
- **Additives** — plasticizers, stabilizers, fillers, catalysts, pigments
- **Cure mechanism** — how the system transitions from application state to cured state
- **Solvent system** — carrier solvent type, VOC content, evaporation behavior
- **System type** — functional category (sealant, adhesive, coating, primer, cleaner, membrane_component)

## System Types

| Type | Description | Division 07 Examples |
|---|---|---|
| sealant | Fills and seals joints, accommodates movement | Joint sealants, weatherseals |
| adhesive | Bonds two substrates together | Membrane adhesives, insulation adhesives |
| coating | Applied layer for protection or waterproofing | Fluid-applied waterproofing, reflective roof coatings |
| primer | Enhances adhesion between sealant/adhesive and substrate | Sealant primers, membrane primers |
| cleaner | Removes contaminants to prepare surfaces | Surface cleaners, silicone removers |
| membrane_component | Chemistry of a sheet membrane system | EPDM compound, PVC compound, TPO compound |

## Object Relationships

```
Chemical System
  ├── polymer_base ──→ Polymer Family (PFAM-xxx)
  ├── additives[] ──→ Additive (ADTV-xxx)
  ├── cure_mechanism_ref ──→ Cure Mechanism (CURE-xxx)
  ├── solvent_system_ref ──→ Solvent System (SOLV-xxx)
  └── material_refs[] ──→ Material Kernel (MAT-xxx, external)
```

## Identity

- **ID prefix:** CSYS-
- **Example:** CSYS-URE-SEAL-001 (urethane sealant system 001)

## Chemistry Family Classification

Every Chemical System carries a `chemistry_family` value from the shared enum:
polyurethane, silicone, polysulfide, acrylic, epoxy, bituminous, polyolefin, pvc, epdm, butyl, sbs, app, pmma, polyurea, hybrid

## Schema Reference

`schemas/chemical_system.schema.json`

## Governance

- Chemical Systems are the hub object — most other chemistry objects reference a Chemical System
- A Chemical System must be `active` before adhesion rules, incompatibility rules, or degradation mechanisms can reference it as active
- VOC content (voc_g_per_l) is recorded here as a chemistry fact, not as a compliance determination
