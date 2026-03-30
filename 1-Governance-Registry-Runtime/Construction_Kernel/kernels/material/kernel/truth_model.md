# Truth Model — Construction Material Kernel

## What Constitutes Material Truth

Material truth is a verifiable fact about a building material's physical characteristics, derived from published test data, manufacturer technical data sheets, or documented field performance. Material truth is always:

1. **Measurable** — expressed as a numeric value with units
2. **Testable** — linked to a recognized test method (ASTM, AAMA, UL)
3. **Traceable** — connected to an evidence source (lab report, TDS, field study)
4. **Bounded** — valid only under stated conditions (temperature, humidity, age)

## Truth Categories

### Physical Properties
Directly measured characteristics: tensile strength, elongation at break, tear resistance, puncture resistance, dimensional stability, thickness, density, hardness. These are the foundational truth records.

### Thermal Properties
Heat transfer characteristics: R-value (thermal resistance), U-factor, thermal conductivity, specific heat capacity, thermal expansion coefficient. Measured per ASTM C518, C177, or equivalent.

### Moisture Properties
Water and vapor behavior: water vapor permeance (perms), moisture absorption (% by weight), water penetration resistance, capillary coefficient, sorption isotherm data. Measured per ASTM E96, D2247, or equivalent.

### Fire Properties
Fire response characteristics: flame spread index, smoke developed index, fire resistance rating, burning brand resistance. Measured per ASTM E84, E108, UL 790, or equivalent.

### Compatibility Facts
Pairwise material interaction results: compatible, incompatible, conditional, untested. Based on published compatibility data, manufacturer guidance, or documented field experience.

### Weathering Facts
Degradation behavior under environmental exposure: UV resistance, thermal cycling response, moisture cycling response, freeze-thaw resistance, chemical resistance, biological resistance.

## Truth Admission Rules

| Rule | Enforcement |
|---|---|
| Value must have units | Schema validation — required `unit` field |
| Value must have test method | Schema validation — required `test_method_ref` |
| Value must have evidence | Doctrine enforcement — `evidence_ref` required |
| Value must have conditions | Schema validation — optional but recommended |
| Untested = untested | Fail-closed — no inference from absence of data |

## Truth Exclusions

- Brand-specific claims without test method backing
- Marketing language or subjective performance descriptions
- Predicted values from simulation (not tested)
- Extrapolated values beyond tested conditions
- Opinions, recommendations, or design guidance
