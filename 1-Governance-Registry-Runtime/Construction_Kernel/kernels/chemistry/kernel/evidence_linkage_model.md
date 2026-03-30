# Evidence Linkage Model

## Purpose

Defines how chemistry truth records link to their supporting evidence. Every active chemistry record must trace to at least one evidence source.

## Evidence Structure

An evidence reference is a structured citation that includes:
- **evidence_id**: Unique identifier (e.g., `EVID-ASTM-C920-2018`)
- **source_type**: Category of source (tier 1-4)
- **citation**: Human-readable citation string
- **document_ref**: Document identifier (SDS number, ASTM designation, DOI)
- **date**: Publication or test date
- **relevance**: How this evidence supports the chemistry record

## Source Tiers

| Tier | Source Type | Confidence | Example |
|---|---|---|---|
| 1 | Peer-reviewed research, accredited lab test | Highest | ASTM C794 test report from accredited lab |
| 2 | Manufacturer SDS, TDS | Standard | Dow Corning 795 SDS, Section 10 |
| 3 | Industry association publication | Acceptable | NRCA Roofing Manual, Chapter 4 |
| 4 | Documented field observation | Low (flagged) | Field report with photos, dated |

## Linkage Rules

1. **Active records** require at least one Tier 1-3 evidence reference
2. **Draft records** may have Tier 4 evidence pending higher-tier confirmation
3. **Incompatibility rules** should have Tier 1 or Tier 2 evidence (chemical conflicts must be well-documented)
4. **Adhesion rules** with status `verified` require Tier 1 evidence (test report)
5. **Degradation mechanisms** may reference accelerated aging test standards as evidence type

## Evidence Fields in Schemas

| Schema | Evidence Field | Required |
|---|---|---|
| adhesion_rule | `evidence_refs` | Optional (recommended for active) |
| incompatibility_rule | `evidence_refs` | Optional (recommended for active) |
| degradation_mechanism | `evidence_refs` | Optional (recommended for active) |
| adhesion_rule | `test_method_ref` | Optional (ASTM/ISO test method ID) |
| chemical_hazard_record | `sds_ref` | Optional (SDS document reference) |

## Evidence Integrity

- Evidence references are immutable once linked to an active record
- If evidence is retracted or superseded, the chemistry record must be reviewed
- Evidence does not transfer between chemistry families by analogy
