"""Governed Result Surface.

Final governed output contract for application-facing consumers.
Wires the complete chain:
  ConditionSignature → ResolutionResult → ConstraintDecision → GovernedResult

Boundary rules:
- Application consumes GovernedResult only
- No direct kernel or engine ownership
- No UI ownership in this layer
- Fail-closed: invalid upstream outputs produce failed GovernedResult
"""

__version__ = "1.0.0"
