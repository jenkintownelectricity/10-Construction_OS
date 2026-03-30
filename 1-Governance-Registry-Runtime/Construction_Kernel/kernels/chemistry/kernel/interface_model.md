# Interface Model

## Purpose

Defines how chemistry truth applies at interface zones — locations where different materials, assemblies, or building systems meet and chemical interactions govern performance.

## Interface Zones Relevant to Chemistry

### 1. Sealant Joints
- **Chemistry concern:** Sealant-to-substrate adhesion, sealant-to-sealant compatibility at intersections
- **Key objects:** Adhesion rules, incompatibility rules, cure mechanisms
- **Typical chemistries:** Silicone, polyurethane, polysulfide, hybrid

### 2. Membrane Laps and Seams
- **Chemistry concern:** Welding chemistry (heat or solvent), adhesive compatibility, seam primer chemistry
- **Key objects:** Chemical systems (adhesives, primers), incompatibility rules
- **Typical chemistries:** EPDM splice adhesive, PVC solvent weld, TPO heat weld

### 3. Membrane-to-Flashing Transitions
- **Chemistry concern:** Adhesion between dissimilar materials, primer requirements, incompatibility at material boundaries
- **Key objects:** Adhesion rules with primer requirements, incompatibility rules
- **Example:** EPDM membrane transitioning to metal flashing — requires compatible adhesive and primer

### 4. Waterproofing-to-Substrate Bond
- **Chemistry concern:** Adhesion to concrete, masonry, metal; moisture tolerance during application; primer chemistry
- **Key objects:** Adhesion rules, cure mechanisms (substrate moisture sensitivity)
- **Example:** Fluid-applied polyurethane waterproofing on concrete — requires dry substrate and primer

### 5. Insulation-to-Adhesive Contact
- **Chemistry concern:** Solvent attack on foam insulation, plasticizer migration from PVC into polystyrene
- **Key objects:** Incompatibility rules, solvent systems
- **Example:** Solvent-based contact adhesive dissolving EPS insulation board

### 6. Coating-to-Substrate Interface
- **Chemistry concern:** Surface preparation chemistry, primer compatibility, intercoat adhesion
- **Key objects:** Adhesion rules, chemical systems (primers and coatings)

### 7. Sealant-to-Backer-Rod Interface
- **Chemistry concern:** Backer rod material compatibility with sealant chemistry, outgassing causing bubbles
- **Key objects:** Incompatibility rules
- **Example:** Open-cell backer rod outgassing into uncured silicone sealant

## Interface Risk Assessment

At every interface zone, the Chemistry Kernel provides:
1. **Adhesion status**: verified, conditional, not_recommended, or untested
2. **Incompatibility flags**: known chemical conflicts at that interface
3. **Primer requirements**: whether primer is needed and which chemistry
4. **Cure constraints**: environmental conditions required for cure at that interface

The Assembly Kernel consumes this data to validate interface details. This kernel does not design the interface — it provides the chemical constraints.
