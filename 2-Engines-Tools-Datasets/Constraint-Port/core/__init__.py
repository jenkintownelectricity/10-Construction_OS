"""Constraint Port Core — Deterministic constraint evaluation engine.

Sits between resolution output and execution, evaluating constraints
and halting invalid outcomes before runtime proceeds.

Boundary rules:
- Deterministic validation only
- No probabilistic authority
- No truth mutation
- No UI ownership
- Fail-closed: unknown constraints BLOCK by default
"""

__version__ = "1.0.0"
