# Field Condition Scanner Specification — Wave 14

## Registry Entry
- **Subsystem:** field_condition_scanner
- **Owner:** Construction_Runtime
- **Path:** runtime/field_scan/
- **Contract Version:** 14.5.0
- **Lifecycle:** active

## Purpose
Processes field condition inputs (image, lidar, manual entry) to produce
advisory-only detected conditions. Scanner output may NEVER automatically
become kernel truth.

## Output Artifacts
- `detected_condition.json`

## Input Types
- Image references
- Lidar data references
- Manual condition entries

## Dependencies
- Construction_Kernel (condition types — frozen, read-only)

## Governance
- Advisory only — all outputs flagged `advisory_only: true`
- May not write to Construction_Kernel
- May not create canonical detail families
- Uncertain detections return UNKNOWN
