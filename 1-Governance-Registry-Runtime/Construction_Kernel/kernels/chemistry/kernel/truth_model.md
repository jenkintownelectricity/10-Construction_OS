# Chemistry Truth Model

## Purpose

Defines what constitutes chemistry truth in this kernel and how truth is sourced, verified, and maintained.

## Definition of Chemistry Truth

Chemistry truth is a verified statement about chemical behavior that is:
1. Sourced from a documented, identifiable origin
2. Specific to a chemistry family or chemical system
3. Testable or reproducible under stated conditions
4. Expressed as structured data with explicit confidence

## Truth Categories

| Category | Example | Schema |
|---|---|---|
| Chemical system composition | Urethane sealant: MDI-based polyurethane, moisture cure | chemical_system.schema.json |
| Cure behavior | Moisture cure requires 40-100°F, >40% RH, 7-day full cure | cure_mechanism.schema.json |
| Adhesion performance | Urethane on concrete: verified with primer, ASTM C794 tested | adhesion_rule.schema.json |
| Chemical incompatibility | Silicone sealant causes adhesion failure on bituminous substrate | incompatibility_rule.schema.json |
| Degradation pathway | Aromatic polyurethane undergoes UV chain scission, causing chalking | degradation_mechanism.schema.json |
| Solvent properties | Solvent-based primer: 350 g/L VOC, 0°F flash point | solvent_system.schema.json |
| Chemical hazard | MDI-based system: sensitizer via inhalation | chemical_hazard_record.schema.json |

## Evidence Hierarchy

### Tier 1 — Highest Confidence
- Peer-reviewed published research
- ASTM/ISO test reports from accredited laboratories
- Independent third-party testing

### Tier 2 — Standard Confidence
- Manufacturer SDS (Safety Data Sheets)
- Manufacturer Technical Data Sheets (TDS)
- Manufacturer technical bulletins

### Tier 3 — Acceptable Confidence
- Industry association technical publications (NRCA, SMACNA, SWRI)
- Consensus standards committee commentary

### Tier 4 — Low Confidence (Flagged)
- Documented field observations with photographic evidence
- Manufacturer verbal guidance (must note source and date)
- Analogous chemistry inference (must be explicitly flagged)

## Truth Maintenance

- Records are created as `draft`, promoted to `active` after evidence review
- Active records are reviewed when new evidence contradicts existing truth
- Deprecated records carry a `superseded_by` reference and deprecation reason
- No record is ever deleted from the kernel
