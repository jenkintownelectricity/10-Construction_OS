# Chemistry Kernel Truth Boundary

## What This Kernel Owns

The Construction Chemistry Kernel owns **chemistry-domain truth**: the verified chemical behavior of construction materials and systems within CSI Division 07 — Building Envelope Systems.

### Chemistry truth includes:

- **Chemical compatibility rules** — which chemistries can coexist without adverse reaction
- **Cure mechanisms** — moisture cure, heat cure, UV cure, chemical cure, evaporative cure
- **Adhesion behavior** — substrate-specific adhesion profiles, primer requirements, surface prep chemistry
- **Solvent interactions** — solvent types, VOC content, flash points, evaporation behavior
- **Degradation pathways** — oxidation, hydrolysis, UV chain scission, plasticizer migration, thermal decomposition
- **Incompatibility rules** — specific chemical conflicts (e.g., silicone on bitumen causes adhesion failure)
- **Chemical hazard posture** — flammability, toxicity, sensitization from SDS data

## What This Kernel Does NOT Own

### Material Physical Properties (Material Kernel)
- Tensile strength, elongation, hardness, density
- Dimensional properties, thickness, weight
- Thermal conductivity, R-value
- Color, texture, surface finish

### Specification Truth (Specification Kernel)
- Specification section clauses
- Submittal requirements, product approvals
- Quality assurance procedures

### Assembly Truth (Assembly Kernel)
- Installation sequences, layer order
- Mechanical attachment patterns
- Flashing details, lap dimensions

### Scope Truth (Scope Kernel)
- Trade responsibilities, work breakdown
- Division of work at transitions

### Reference Intelligence
- Cross-kernel synthesis and recommendations
- Risk scoring, decision support

## The Boundary with Material Kernel

This is the most critical boundary. The dividing line:

| Chemistry Kernel | Material Kernel |
|---|---|
| Polymer base chemistry | Product trade name |
| Cure mechanism and conditions | Shelf life |
| Adhesion to substrates | Tensile strength |
| Chemical compatibility | Elongation at break |
| Solvent system and VOC | Shore A hardness |
| Degradation pathways | Service temperature range |
| Plasticizer migration risk | Dimensional tolerances |

A material record in the Material Kernel may reference a chemistry record here via `chemistry_ref`. This kernel does not import material properties.
