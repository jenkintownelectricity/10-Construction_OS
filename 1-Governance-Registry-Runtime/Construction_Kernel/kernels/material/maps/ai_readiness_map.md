# AI Readiness Map — Construction Material Kernel

## Purpose
Maps AI integration readiness for each kernel object type and data surface.

## Object-Level AI Readiness

| Object Type | Machine Readable | Schema Validated | Enum Controlled | AI Ready |
|---|---|---|---|---|
| Material Class | Yes | Yes | Yes (12 classes) | Ready for consumption |
| Material Form | Yes | Yes | Yes (11 forms) | Ready for consumption |
| Material Property | Yes | Yes | Partial (property names) | Ready for consumption |
| Material Performance | Yes | Yes | Partial | Ready for consumption |
| Compatibility Record | Yes | Yes | Yes (4 results) | Ready for consumption |
| Weathering Behavior | Yes | Yes | Yes (6 exposure types) | Ready for consumption |
| Hygrothermal Property | Yes | Yes | Yes (5 property types) | Ready for consumption |
| Standards Reference | Yes | Yes | No (free text titles) | Ready for consumption |

## AI Use Case Readiness

| Use Case | Data Ready | Interface Ready | Overall |
|---|---|---|---|
| Property value lookup | Yes | No (no API) | Blocked by interface |
| Compatibility query | Yes | No (no API) | Blocked by interface |
| Material classification | Yes | No (no API) | Blocked by interface |
| TDS data extraction | Target schema ready | No (no ingestion) | Blocked by pipeline |
| Compatibility gap analysis | Matrix data ready | No (no analysis engine) | Blocked by tooling |
| Weathering pattern detection | Data ready | No (no ML model) | Blocked by model |
| Property anomaly detection | Data ready | No (no ML model) | Blocked by model |

## AI Governance Constraints

| Constraint | Enforcement |
|---|---|
| No AI writes to active records | Schema + access control |
| AI-generated drafts require human review | Status field governance |
| AI must present evidence refs | Contract obligation |
| AI must surface ambiguity flags | Contract obligation |
| AI must not extrapolate beyond data | Interpretation limitations doctrine |

## Readiness Advancement Path

1. Current: Structured data ready (Level 2)
2. Next: API interface layer (Level 3)
3. Future: AI-assisted data ingestion (Level 4)
4. Long-term: AI-augmented analysis with human oversight (Level 5)
