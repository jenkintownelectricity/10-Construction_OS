# Interface Risk Map

## Purpose

Documents chemistry risks at interface zones — sealant joints, adhesion boundaries, material transitions, and layered assemblies in Division 07 construction.

## High-Risk Interface Zones

| Interface Zone | Risk Type | Chemistry Entities Involved |
|---|---|---|
| Sealant-to-substrate joint | Adhesion failure | Adhesion Rule, Chemical System, Cure Mechanism |
| Sealant-to-sealant transition | Incompatibility | Incompatibility Rule (chemistry_a vs chemistry_b) |
| Membrane-to-flashing lap | Plasticizer migration | Degradation Mechanism, Incompatibility Rule |
| Coating over existing coating | Adhesion failure, cure inhibition | Adhesion Rule, Incompatibility Rule |
| Metal flashing to sealant | Corrosion, adhesion failure | Incompatibility Rule, Chemical Hazard Record |
| Concrete substrate to sealant | Conditional adhesion | Adhesion Rule (surface prep, primer requirements) |

## Risk Evaluation Flow

1. Identify the interface zone and the two materials in contact.
2. Retrieve chemical system records for both materials.
3. Check incompatibility rules for the chemistry pair.
4. Check adhesion rules for the chemistry-substrate combination.
5. Verify cure mechanism constraints against installation conditions.
6. Flag any active degradation mechanisms for the chemistries involved.

## Common Failure Modes at Interfaces

- **Adhesion failure:** Sealant pulls away from substrate due to inadequate surface prep or missing primer.
- **Plasticizer migration:** PVC plasticizers soften adjacent adhesives or sealants.
- **Cure inhibition:** Sulfur-containing substrates inhibit platinum-catalyzed silicone cure.
- **Staining:** Bituminous oils migrate into light-colored sealants or coatings.
- **Corrosion:** Acidic cure byproducts from acetoxy silicone attack ferrous metals.

## Mitigation Through Kernel Data

- Adhesion rules with `primer_required: true` enforce primer application.
- Incompatibility rules with `severity: critical` block incompatible pairings.
- Cure mechanism `min_temp_f` and `min_humidity_pct` prevent application under adverse conditions.
- Degradation mechanisms flag chemistries at risk in specific climate contexts.

## Constraints

- Interface risk evaluation is a read-only operation against kernel records.
- Risk decisions require human judgment; the kernel provides data, not determinations.
