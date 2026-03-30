# Polymer Family Model

## Purpose

Defines the Polymer Family object — a classification of polymer chemistry with characteristic behaviors that govern performance in building envelope applications.

## Object Definition

A Polymer Family represents a class of polymers sharing:
- **Chemical backbone structure** — the fundamental polymer chain composition
- **Characteristic properties** — inherent behaviors driven by chemistry (not physical test values)
- **Typical applications** — how this chemistry is used in Division 07
- **Known incompatibilities** — chemistry-level conflicts with other families

## Polymer Families in Division 07

| Family | Backbone | Key Chemical Characteristic |
|---|---|---|
| Polyurethane | Isocyanate + polyol | Versatile; moisture-sensitive cure; aromatic vs. aliphatic UV behavior |
| Silicone | Polydimethylsiloxane | Inorganic Si-O backbone; UV stable; wide temp range; surface contamination |
| Polysulfide | Sulfur-linked polymer | Chemical/fuel resistant; two-component cure; odor |
| Acrylic | Polyacrylate | Water-based; paintable; limited elasticity |
| Epoxy | Epoxide resin | High crosslink density; rigid; excellent adhesion; brittle |
| Bituminous | Asphalt hydrocarbon | Waterproof; UV-sensitive; solvent-susceptible |
| Polyolefin | PP/PE blend | Thermoplastic; chemical resistant; heat weldable |
| PVC | Vinyl chloride polymer | Plasticizer-dependent flexibility; solvent weldable; migration risk |
| EPDM | Ethylene propylene diene | Vulcanized rubber; excellent weathering; petroleum-sensitive |
| Butyl | Polyisobutylene | Non-curing; low permeability; pressure-sensitive |
| SBS | Styrene-butadiene-styrene | Flexible modified bitumen; cold-weather performance |
| APP | Atactic polypropylene | Heat-resistant modified bitumen; torch-applied |
| PMMA | Polymethyl methacrylate | Fast cure; excellent adhesion; liquid-applied |
| Polyurea | Isocyanate + amine | Rapid cure; spray-applied; flexible; moisture-insensitive cure |
| Hybrid | Silyl-modified polyether/urethane | Isocyanate-free; paintable; moisture cure |

## Identity

- **ID prefix:** PFAM-
- **Example:** PFAM-SILICONE (silicone polymer family)

## Schema Reference

`schemas/polymer_family.schema.json`

## Relationship to Chemical Systems

Multiple Chemical Systems may share the same Polymer Family. For example:
- CSYS-SIL-SEAL-001 (silicone sealant) → PFAM-SILICONE
- CSYS-SIL-COAT-001 (silicone coating) → PFAM-SILICONE

The Polymer Family provides family-level behavior. The Chemical System adds formulation-specific details (additives, cure mechanism, solvent system).
