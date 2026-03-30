# Interpretation Limitations — Construction Material Kernel

## Foundational Rule

This kernel records published material properties from test data, manufacturer technical data sheets, and field performance observations. It does not interpret, predict, extrapolate, or editorialize beyond what the published data states. Every material property record is a faithful representation of a tested or published value.

## Published Data Fidelity

When a manufacturer TDS states "tensile strength: 200 psi per ASTM D751," this kernel records:

- The property name (tensile strength)
- The value (200 psi)
- The test method (ASTM D751)
- The evidence source (manufacturer TDS reference)

It does not infer that tensile strength will remain at 200 psi after 10 years of UV exposure. It does not calculate retained tensile strength from accelerated weathering data. Those are predictions that belong to engineering analysis.

## Test Condition Boundaries

Material properties are valid only under the conditions stated in the test method and evidence source. A vapor permeance value tested at 73 deg F and 50% RH is recorded with those conditions. The kernel does not extrapolate that value to different temperatures or humidity levels.

## Compatibility Judgment Limits

Compatibility records state whether two materials are compatible, incompatible, conditional, or untested based on published evidence. The kernel does not:

1. **Predict untested combinations** — if no evidence exists, the status is `untested`
2. **Explain mechanisms** — the reason for incompatibility (plasticizer migration, solvent attack) belongs to the chemistry kernel
3. **Override manufacturer guidance** — if a manufacturer states incompatibility, that fact is recorded regardless of theoretical chemistry arguments

## Weathering and Degradation Limits

Weathering behavior records capture published degradation rates from accelerated and natural weathering studies. The kernel does not:

1. **Extend beyond test duration** — a 10,000-hour xenon arc test result is not extrapolated to 20,000 hours
2. **Combine exposure effects** — synergistic degradation from simultaneous UV and moisture is recorded only if specifically tested
3. **Predict field life** — service life estimates are recorded as published claims, not kernel-generated predictions

## Hygrothermal Property Limits

Hygrothermal properties are recorded at stated temperature and relative humidity conditions. The kernel does not model moisture transport through assemblies, calculate dew point locations, or simulate hygrothermal behavior. Those functions belong to engineering analysis tools and the assembly kernel.

## Prohibited Interpretation Activities

The following activities are explicitly outside this kernel's scope:

1. **Performance prediction** — projecting behavior beyond tested conditions
2. **Material selection** — recommending one material over another
3. **Failure analysis** — determining root cause of material failures (forensic data is recorded as evidence, not interpreted)
4. **Equivalency judgments** — determining whether one material can substitute for another
5. **Standard summarization** — restating what a referenced test method measures
6. **Gap-filling** — inferring properties that have not been tested

## Human Resolution Path

When material data is ambiguous, contradictory, or insufficient, the `ambiguity_flag` is set. Ambiguity flags are surfaced to the intelligence layer for human review. When resolved, a new material record is created with updated evidence pointers. The original ambiguous record is superseded, never deleted.
