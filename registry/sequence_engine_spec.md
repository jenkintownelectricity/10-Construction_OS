# Installation Sequence Engine Specification — Wave 14

## Registry Entry
- **Subsystem:** installation_sequence_engine
- **Owner:** Construction_Runtime
- **Path:** runtime/installation_sequence/
- **Contract Version:** 14.6.0
- **Lifecycle:** active

## Purpose
Generates derived installation sequencing from resolved details and route
relationships. Every step is traceable to detail and relationship context.

## Output Artifacts
- `installation_sequence_manifest.json`

## Dependencies
- Detail Resolver Engine (resolved detail IDs)
- Construction_Kernel (route graph — frozen, read-only)

## Governance
- Runtime-derived, recomputable
- May not create circular dependencies
- May not write to Construction_Kernel
- Deterministic output required
