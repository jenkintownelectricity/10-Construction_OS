# Lifecycle Context Model

## Purpose

Defines how the Chemistry Kernel records chemical behavior changes across the lifecycle of a building envelope system — from application through degradation.

## Lifecycle Phases

### Application Phase Chemistry
- **Pot life:** Time available before mixed multi-component systems begin to gel
- **Open time:** Time after application before skin formation prevents tooling
- **Flash-off:** Solvent evaporation period before membrane can be covered or coated
- **Tack development:** Time for adhesive to develop sufficient tack for bonding
- **Relevant objects:** Cure mechanisms (cure_time_hours), solvent systems (evaporation_rate)

### Cure Phase Chemistry
- **Initial cure:** Tack-free state; surface is no longer sticky but full properties not developed
- **Full cure:** Complete crosslinking or polymer development; full mechanical and adhesion properties achieved
- **Depth of cure:** Distance from exposed surface that cure mechanism penetrates (relevant for moisture-cure silicones in deep joints)
- **Relevant objects:** Cure mechanisms (full_cure_days, moisture_sensitive, min/max temp and humidity)

### Service Phase Chemistry
- **Chemical stability:** Polymer chain integrity under normal service conditions
- **Plasticizer retention:** Flexible PVC and some sealants depend on plasticizer remaining in the matrix
- **Adhesion durability:** Long-term adhesion under thermal cycling, moisture exposure, UV
- **Chemical resistance:** Resistance to cleaning agents, atmospheric pollutants, biological growth
- **Relevant objects:** Chemical systems, adhesion rules, incompatibility rules

### Degradation Phase Chemistry
- **Oxidation:** Oxygen attacks polymer chains, causing brittleness
- **UV chain scission:** Ultraviolet radiation breaks polymer backbone bonds
- **Hydrolysis:** Water breaks ester or other hydrolyzable bonds
- **Plasticizer loss:** Plasticizer migrates out of the matrix or evaporates
- **Biological attack:** Microorganisms consume organic components
- **Relevant objects:** Degradation mechanisms (degradation_type, rate_factors)

### End-of-Life Chemistry
- **Removal chemistry:** Solvents or mechanical methods to remove aged sealants
- **Substrate contamination:** Residual chemistry on substrate affecting new installation (silicone contamination)
- **Re-application compatibility:** New chemistry must be compatible with any residue
- **Relevant objects:** Incompatibility rules (silicone residue), adhesion rules (contaminated substrates)

## Lifecycle Data in Records

Chemistry records do not carry a lifecycle phase field. Instead, lifecycle context is implicit in the record type:
- Cure mechanisms → Application and Cure phases
- Adhesion rules → Service phase (verified under cured conditions)
- Degradation mechanisms → Degradation phase
- Incompatibility rules → All phases (some incompatibilities manifest only over time)
