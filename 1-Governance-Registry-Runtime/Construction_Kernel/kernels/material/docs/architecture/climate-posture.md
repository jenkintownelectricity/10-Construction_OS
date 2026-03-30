# Climate Posture — Construction Material Kernel

## Climate Context for Materials

Climate affects material selection, performance expectations, and degradation rates. This kernel records climate-relevant material properties and climate context metadata. It does not perform climate analysis or climate zone classification.

## Climate Factors Affecting Material Properties

| Climate Factor | Material Impact | Kernel Coverage |
|---|---|---|
| Temperature extremes | Thermal expansion, brittleness, softening | Records thermal range properties |
| UV radiation intensity | Polymer degradation, color change, embrittlement | Records UV weathering behavior |
| Moisture exposure | Absorption, permeance change, biological growth | Records hygrothermal properties |
| Freeze-thaw cycling | Dimensional change, cracking, adhesion loss | Records freeze-thaw weathering behavior |
| Wind exposure | Mechanical stress on membranes and flashings | Records tensile and tear strength |
| Salt spray (coastal) | Corrosion, chemical degradation | Records chemical weathering behavior |
| High humidity (sustained) | Moisture absorption, vapor drive | Records permeance and absorption |

## Climate Context in Material Records

Material performance and weathering records include an optional `climate_context` field that may specify:

- ASHRAE climate zone applicability (e.g., Zone 4A — Mixed Humid)
- IECC climate zone reference
- Exposure severity classification (mild, moderate, severe)
- Specific climate stressors relevant to the test data

## What This Kernel Does

- Records material properties tested under climate-relevant conditions
- Records weathering behavior data with climate context metadata
- Records hygrothermal properties at stated temperature and humidity
- Tags material records with climate zone applicability when published data supports it

## What This Kernel Does Not Do

- Does not classify projects by climate zone (project scope concern)
- Does not recommend materials for specific climate zones (specification concern)
- Does not model heat transfer through assemblies (assembly concern)
- Does not predict material performance in untested climate conditions
- Does not perform hygrothermal simulation (engineering analysis tool)

## Climate Data Sources

Climate context in material records traces to:
- Manufacturer TDS with climate zone recommendations
- ASTM weathering test results under climate-specific protocols
- Published field performance studies in identified climate zones
- Building science research with climate-stratified material data

## Shared Climate References

Climate zone definitions are maintained in the shared family artifacts. This kernel references climate zones by ID from the shared registry; it does not define climate zone boundaries.
