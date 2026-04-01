"""Runtime Adapter — Bounded seam between Construction_Runtime and ALEXANDER Engine.

Accepts ConditionSignature from runtime consumers, invokes ALEXANDER
resolution pipeline, validates output, and returns governed advisory
ResolutionResult.

Boundary rules:
- ALEXANDER Engine is advisory only (Ring 2)
- Runtime adapter does not mutate kernels
- Runtime adapter does not own execution
- Fail-closed on any validation failure
"""

__version__ = "1.0.0"
