# Runtime Resolution Contract

This contract defines the runtime-facing advisory seam for Construction_ALEXANDER_Engine.

Advisory seam objects:
- `resolution_result.schema.json`
- `condition_signature.schema.json`

Purpose:
- Define runtime-facing contract for advisory resolution results only.

Boundary rules:
- Construction_Runtime is consumer only.
- Construction_ALEXANDER_Engine does not execute runtime.
- Construction_ALEXANDER_Engine does not mutate kernels.
- Construction_ALEXANDER_Engine emits advisory outputs only.