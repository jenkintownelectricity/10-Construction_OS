# Evidence-to-Object Map — Construction Material Kernel

## Purpose
Maps evidence types to the kernel objects they support and validates evidence coverage.

## Evidence Type Coverage

| Evidence Type | Supports Objects | Typical Use |
|---|---|---|
| Laboratory test report (LAB) | Material Property, Hygrothermal Property | Independent verification of property values |
| Manufacturer TDS (TDS) | Material Property, Material Class | Published property values and material classification |
| Field performance study (FLD) | Weathering Behavior, Material Performance | In-service degradation and performance data |
| Forensic analysis report (FOR) | Weathering Behavior, Compatibility Record | Post-failure material interaction evidence |
| Accelerated weathering test (AWX) | Weathering Behavior | UV, thermal cycling, moisture exposure results |
| Peer-reviewed publication (PUB) | All objects | Research-backed property values and compatibility data |

## Object-to-Evidence Requirements

| Object Type | Minimum Evidence | Preferred Evidence |
|---|---|---|
| Material Property | 1 TDS or LAB report | LAB report with TDS confirmation |
| Compatibility Record | 1 evidence source | Multiple independent sources |
| Weathering Behavior | 1 AWX or FLD study | AWX + FLD correlation |
| Hygrothermal Property | 1 LAB or TDS | LAB per ASTM E96 |
| Material Performance | 1 evidence source | Multiple test result references |
| Material Class | TDS confirming classification | Standards compliance certification |

## Evidence Gap Indicators

| Gap Type | Detection Method | Resolution Path |
|---|---|---|
| No evidence for active property | Missing evidence_ref on active record | Flag for review; cannot remain active |
| Single-source evidence | Only one evidence_ref | Acceptable but flagged for confirmation |
| Aged evidence (>15 years) | Evidence date check | Flag for currency review |
| Conflicting evidence | Multiple sources disagree | Set ambiguity_flag; human resolution |
| Evidence from non-standard test | Test method not in standards registry | Review for acceptability |

## Evidence Integrity Rules

1. Every active property record must have at least one evidence reference
2. Evidence references must include type, source ID, and date
3. Evidence documents are not stored in the kernel — only references
4. Conflicting evidence triggers ambiguity flags, not silent override
5. Evidence quality hierarchy determines precedence (LAB > TDS > FLD)
