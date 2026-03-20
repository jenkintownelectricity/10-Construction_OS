# Installation Sequence Contract — Wave 14

## Contract Version
14.6.0

## Purpose
Generates derived installation sequencing from resolved details and route relationships.
Every step is traceable to detail and relationship context.

## Authority
- Construction_Runtime (derived, runtime-only)
- Construction_Kernel provides canonical detail families (frozen, read-only)

## Inputs
- Resolved detail IDs from detail_resolver
- Route relationships from detail_route_index

## Outputs
- installation_sequence_manifest.json

## Contract Object: InstallationSequence
```json
{
  "sequence_id": "string",
  "detail_ref": "canonical_detail_id",
  "steps": [
    {
      "step_number": 1,
      "action": "description of installation action",
      "detail_context": "context reference",
      "dependencies": [step_numbers]
    }
  ],
  "status": "RESOLVED | UNRESOLVED | UNSUPPORTED"
}
```

## Rules
1. Sequence must reference valid canonical detail IDs.
2. Sequence must not create circular dependencies.
3. Every step must be traceable to detail and relationship context.
4. Unsupported sequences must emit UNRESOLVED.
5. Output must be deterministic.

## Governance
- This subsystem may NOT create new detail families.
- This subsystem may NOT write to Construction_Kernel.
- All outputs are runtime-derived and recomputable.
