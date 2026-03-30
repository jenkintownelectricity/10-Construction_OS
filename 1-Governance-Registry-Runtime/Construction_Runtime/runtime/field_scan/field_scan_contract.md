# Field Condition Scanner Contract — Wave 14

## Contract Version
14.5.0

## Purpose
Processes field condition inputs (image, lidar, manual entry) to produce
advisory-only detected conditions. Scanner output may NEVER automatically
become kernel truth.

## Authority
- Construction_Runtime (derived, runtime-only, advisory)
- Construction_Kernel is the ONLY source of truth (scanner cannot write)

## Inputs
- Image references
- Lidar data references
- Manual condition entries

## Outputs
- detected_condition.json (advisory only)

## Contract Object: DetectedCondition
```json
{
  "detected_condition_type": "string — condition type or UNKNOWN",
  "detected_material_hints": ["string — material class hints"],
  "detected_geometry_hints": {"param": "value"},
  "confidence": "number 0–1",
  "evidence_refs": ["string — references to raw evidence"],
  "advisory_only": true
}
```

## Rules
1. Scanner output is advisory only.
2. No scanner output may automatically become kernel truth.
3. Uncertain detection must return UNKNOWN.
4. Confidence thresholds must be explicit.
5. Unsupported detection classes must fail closed.
6. Raw scan evidence refs must be preserved.
7. No silent correction of ambiguous detections.

## Governance
- This subsystem may NOT write to Construction_Kernel.
- This subsystem may NOT create canonical detail families.
- All outputs are advisory and must be explicitly flagged as such.
