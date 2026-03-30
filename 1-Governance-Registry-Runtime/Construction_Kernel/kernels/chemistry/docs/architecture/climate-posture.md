# Chemistry Kernel Climate Posture

## Purpose

Defines how the Chemistry Kernel addresses climate and weather effects on chemical behavior without owning climate data or making climate-specific predictions.

## Climate Effects on Chemistry

### Temperature Effects
- **Cure rate:** Most cure mechanisms slow or stop below minimum temperatures. Moisture-cure urethanes typically require >40°F. Epoxies require >50°F for proper crosslinking.
- **Viscosity:** Sealant and adhesive viscosity increases in cold, decreasing workability. Hot-applied systems require sustained application temperature.
- **Adhesion:** Cold substrates may have condensation affecting adhesion. Thermal shock can stress adhesive bonds.
- **Degradation:** Thermal cycling accelerates fatigue in polymer chains. Sustained heat accelerates oxidation.

### Humidity Effects
- **Moisture cure:** Requires minimum humidity (typically >40% RH) for moisture-cure systems. Excess humidity can cause bubbling in some polyurethanes.
- **Adhesion:** Substrate moisture content affects adhesion. Concrete substrate moisture must be within limits for adhesive systems.
- **Degradation:** Sustained moisture exposure drives hydrolysis in susceptible chemistries (certain esters, polyurethanes).

### UV Exposure
- **Chain scission:** UV radiation breaks polymer chains in non-UV-stabilized systems. Aromatic polyurethanes yellow and chalk. Aliphatic polyurethanes and silicones resist UV.
- **Surface degradation:** UV affects exposed surfaces first. Depth of degradation depends on pigmentation and UV stabilizer content.

## What This Kernel Records

- Temperature ranges in cure mechanism records (min_temp_f, max_temp_f)
- Humidity ranges in cure mechanism records (min_humidity_pct, max_humidity_pct)
- UV degradation as a degradation mechanism type
- Climate context as optional fields on degradation records

## What This Kernel Does NOT Do

- Predict performance in specific climate zones (ASHRAE zones, Koppen classifications)
- Calculate degree-day accumulation for cure estimation
- Model seasonal UV exposure patterns
- Recommend climate-specific product selections

Climate-specific analysis is a Reference Intelligence function that consumes chemistry facts from this kernel combined with project location data.
