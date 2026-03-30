# Chemistry Kernel Interpretation Limitations

## Scope of Interpretation

The Construction Chemistry Kernel records published chemical behavior data from verified sources. It provides structured access to that data. It does not interpret beyond what the source data states.

## Specific Limitations

### 1. No Novel Reaction Prediction
This kernel records known chemical interactions. If two chemistries have not been tested together and no published data exists, this kernel returns `untested` — not a prediction. The absence of an incompatibility record does not imply compatibility.

### 2. No Extrapolation Beyond Tested Conditions
Cure mechanism records include tested temperature and humidity ranges. This kernel does not extrapolate behavior outside those ranges. A moisture-cure urethane tested at 40-100°F cannot be assumed to perform at 20°F based on this kernel's data.

### 3. No Cross-Chemistry Analogies
Behavior documented for one polymer family is not applied to another. Silicone adhesion data does not inform polysulfide adhesion assumptions, even when substrates are identical.

### 4. Source Hierarchy
Data quality depends on source type. This kernel records the source but does not upgrade data confidence:
- **Tier 1:** Peer-reviewed research, ASTM/ISO test reports
- **Tier 2:** Manufacturer SDS and technical data sheets
- **Tier 3:** Industry technical bulletins (NRCA, SMACNA)
- **Tier 4:** Documented field observations (flagged as lower confidence)

### 5. No Time-Based Degradation Rate Calculation
Degradation mechanisms are recorded qualitatively (oxidation, UV chain scission, hydrolysis). Rate calculations require project-specific exposure modeling that is outside this kernel's scope.

### 6. No Climate-Specific Predictions
Climate context records describe how temperature and humidity affect chemistry (e.g., cure slows below 40°F). This kernel does not predict performance in a specific climate zone. Climate-specific analysis is a reference intelligence function.

### 7. No Interaction Effect Modeling
When three or more chemistries are present, pairwise incompatibility rules may not capture emergent effects. This kernel records pairwise rules only. Multi-chemistry interaction analysis requires intelligence-layer synthesis.

### 8. Manufacturer-Specific Variations
Two products in the same chemistry family may behave differently due to proprietary formulation. This kernel records family-level behavior. Product-specific deviations require manufacturer-specific evidence records.

## Fail-Closed Implication

When interpretation reaches a limitation boundary, the kernel defaults to the most conservative position: untested, unverified, or not recommended. This is the fail-closed doctrine in practice.
