# Standards Reference Model

## Purpose

Defines how the Scope Kernel references industry standards without owning or interpreting their content. Standards references are pointers that provide traceability between scope records and the standards that inform them.

## Reference Structure

Each standards reference in a scope record contains:
- **Standard identifier** (e.g., "ASTM E2357")
- **Standard title** (human-readable, for context only)
- **Relevance** (why this standard is referenced by this scope record)

## Standards Referenced by Scope Category

### Roofing
| Standard | Relevance to Scope |
|---|---|
| ASTM D4811 | Nonvulcanized rubber sheet waterproofing |
| FM 4470 | Single-ply roof assemblies (wind uplift) |
| SPRI RP-4 | Wind design for ballasted roofing |
| UL 790 | Fire resistance of roof covering materials |

### Waterproofing
| Standard | Relevance to Scope |
|---|---|
| ASTM D4263 | Moisture testing of concrete substrates |
| ASTM C836 | Below-grade waterproofing membrane performance |
| ASTM D5957 | Flood testing of horizontal waterproofing |

### Air Barriers
| Standard | Relevance to Scope |
|---|---|
| ASTM E2357 | Air leakage of building envelopes |
| ASTM E3158 | Air barrier material, assembly, whole-building testing |
| ASTM E783 | Air leakage of windows and doors |

### Commissioning
| Standard | Relevance to Scope |
|---|---|
| ASTM E2813 | Building enclosure commissioning process |
| NIBS Guideline 3 | Exterior enclosure technical requirements |

### Firestopping
| Standard | Relevance to Scope |
|---|---|
| ASTM E814 | Fire test of through-penetration firestops |
| ASTM E2307 | Fire resistance of perimeter fire barriers |
| UL 1479 | Fire resistance of through-penetrations |

## Reference Rules

1. Standards references are outbound pointers only. The Scope Kernel does not store standards content.
2. Standards references do not imply compliance. The Scope Kernel records which standards are relevant, not whether requirements are met.
3. Standards references are version-agnostic in the scope record. Version resolution is the responsibility of the Reference Intelligence layer.
4. Test method references on inspection steps point to the standard that defines the test procedure.
