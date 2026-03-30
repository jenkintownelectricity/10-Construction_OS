# Standards Reference Model

## Purpose

Defines how the Chemistry Kernel references external standards without reproducing their content.

## Reference Principles

1. Standards are cited by identifier only (e.g., ASTM C920, ISO 11600)
2. No standards text is reproduced in this kernel
3. Standards references appear in specific schema fields: `test_method_ref`, `evidence_refs`, `regulatory_refs`
4. Standards inform the structure of chemistry objects but do not govern kernel schema design

## Key Standards by Chemistry Domain

### Sealant Chemistry
| Standard | Title (abbreviated) | Kernel Usage |
|---|---|---|
| ASTM C920 | Elastomeric Joint Sealants | Chemistry family classification, cure type, movement capability |
| ASTM C794 | Adhesion-in-Peel | Adhesion rule test method reference |
| ASTM C1135 | Sealant Compatibility | Incompatibility rule evidence |
| ASTM C719 | Cyclic Movement | Cure performance validation |
| ASTM C1193 | Sealant Use Guide | Application condition references |
| ASTM C836 | Surface Preparation | Adhesion context for substrate prep |

### Membrane Chemistry
| Standard | Title (abbreviated) | Kernel Usage |
|---|---|---|
| ASTM D4637 | EPDM Membrane | EPDM chemistry classification |
| ASTM D6878 | TPO Membrane | TPO chemistry classification |
| ASTM D4434 | PVC Membrane | PVC chemistry classification |
| ASTM D6162 | SBS Modified Bitumen | SBS chemistry classification |

### Adhesion and Degradation Testing
| Standard | Title (abbreviated) | Kernel Usage |
|---|---|---|
| ASTM D4541 | Pull-Off Adhesion | Adhesion rule evidence |
| ASTM G154 | UV Fluorescent Exposure | Degradation mechanism evidence |
| ASTM G155 | Xenon Arc Exposure | Degradation mechanism evidence |
| ASTM D2565 | Xenon Arc for Plastics | Polymer degradation evidence |

### VOC and Regulatory
| Standard | Title (abbreviated) | Kernel Usage |
|---|---|---|
| SCAQMD Rule 1168 | Adhesive/Sealant VOC Limits | Solvent system regulatory classification |
| EPA Method 24 | VOC Content Determination | Solvent system VOC measurement reference |
| ASTM D2369 | VOC Content of Coatings | Solvent system VOC measurement reference |

## Standards-to-Schema Field Mapping

| Schema Field | Standards Referenced |
|---|---|
| `adhesion_rule.test_method_ref` | ASTM C794, D4541 |
| `degradation_mechanism.evidence_refs` | ASTM G154, G155, D2565 |
| `chemical_hazard_record.regulatory_refs` | OSHA PEL, ACGIH TLV, GHS |
| `solvent_system.regulatory_class` | SCAQMD, EPA Method 24 |
| `incompatibility_rule.evidence_refs` | ASTM C1135 |
