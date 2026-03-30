# Climate Context Model

## Purpose

Records how temperature, humidity, and UV exposure affect chemical behavior in building envelope systems. This kernel stores the chemistry facts; climate-zone-specific analysis is a Reference Intelligence function.

## Temperature Effects on Chemistry

### Cure Chemistry
| Temperature Range | Effect on Cure |
|---|---|
| Below 32°F (0°C) | Most cure mechanisms stop. Water-based systems freeze. |
| 32-40°F (0-4°C) | Moisture-cure urethanes: severely slowed. Epoxies: may not crosslink. |
| 40-50°F (4-10°C) | Minimum for many moisture-cure sealants. Epoxy cure very slow. |
| 50-80°F (10-27°C) | Optimal range for most cure mechanisms. |
| 80-100°F (27-38°C) | Accelerated cure. Pot life shortened for multi-component systems. |
| Above 100°F (38°C) | Risk of skinning before tooling. Solvent flash too rapid. Adhesion may suffer. |

### Adhesion Chemistry
- Cold substrates may have condensation preventing adhesion
- Hot substrates may cause premature skinning of sealant before wetting substrate
- Thermal cycling stresses adhesion bonds cyclically

### Degradation Chemistry
- Sustained heat accelerates oxidation rates
- Freeze-thaw cycling stresses polymer matrix and adhesion bonds
- UV intensity varies by latitude and altitude, affecting chain scission rates

## Humidity Effects on Chemistry

### Moisture-Cure Systems
- Require minimum ambient humidity (typically 40-60% RH)
- Excess humidity (>80% RH) can cause bubbling in some polyurethane systems
- Rain exposure before cure completion can damage surface quality

### Substrate Moisture
- Concrete moisture content affects adhesion (typically <5% moisture by ASTM D4263)
- Wood substrate moisture content affects adhesive performance
- Metal substrate condensation (dew point) prevents adhesion

### Degradation
- Sustained moisture drives hydrolysis in ester-based polymers
- Standing water accelerates biological degradation
- Humidity cycling causes dimensional stress in moisture-sensitive substrates

## UV Exposure Effects

| Polymer Family | UV Resistance |
|---|---|
| Silicone | Excellent — PDMS backbone resists UV |
| Aliphatic polyurethane | Good — no aromatic groups to absorb UV |
| Aromatic polyurethane | Poor — aromatic groups absorb UV, causing yellowing and chalking |
| EPDM | Excellent — saturated backbone |
| PVC | Moderate — requires UV stabilizers |
| Bituminous | Poor — requires surfacing protection |
| Acrylic | Good — UV stable backbone |
| Polysulfide | Poor — UV causes surface degradation |

## Data Representation

Climate context appears in chemistry records as:
- `cure_mechanism.min_temp_f` / `max_temp_f` — temperature limits
- `cure_mechanism.min_humidity_pct` / `max_humidity_pct` — humidity limits
- `degradation_mechanism.climate_context` — optional climate factors
- `degradation_mechanism.rate_factors` — conditions that accelerate degradation
