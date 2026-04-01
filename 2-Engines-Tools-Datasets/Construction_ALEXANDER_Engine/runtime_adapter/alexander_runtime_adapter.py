"""Alexander Runtime Adapter.

Bounded runtime adapter that accepts ConditionSignature from runtime consumers,
invokes the ALEXANDER resolution pipeline, validates the output, and returns
a governed advisory RuntimeAdapterResult.

Flow: accept → validate input → invoke engine → validate output → return result

Boundary rules:
- ALEXANDER Engine is advisory only (Ring 2)
- Adapter does not mutate kernels
- Adapter does not own execution
- Fail-closed on any validation or engine error
- All outputs are validated before returning to consumer
"""

from __future__ import annotations

from typing import Any, Protocol

from runtime_adapter.runtime_resolution_types import (
    RuntimeAdapterError,
    RuntimeAdapterResult,
)
from runtime_adapter.runtime_resolution_validator import (
    validate_condition_signature,
    validate_resolution_result,
)


class ResolutionEngine(Protocol):
    """Protocol for the ALEXANDER resolution pipeline.

    The adapter depends on this interface, not on the concrete engine.
    This allows the adapter to be tested independently of the full engine.
    """

    def resolve(self, condition: dict[str, Any], kernel: Any) -> dict[str, Any]:
        """Execute the resolution pipeline and return a ResolutionResult dict."""
        ...


class AlexanderRuntimeAdapter:
    """Bounded runtime adapter for the ALEXANDER resolution pipeline.

    Accepts ConditionSignature inputs, validates them, invokes the engine,
    validates the output, and returns a RuntimeAdapterResult.

    This adapter is the ONLY sanctioned seam between Construction_Runtime
    consumers and the ALEXANDER Engine.
    """

    def __init__(self, engine: ResolutionEngine, kernel: Any) -> None:
        """Initialize the adapter.

        Args:
            engine: The resolution engine (must implement ResolutionEngine protocol)
            kernel: The PatternKernelConsumer instance for truth lookup
        """
        self._engine = engine
        self._kernel = kernel

    def resolve_condition(self, condition: dict[str, Any]) -> RuntimeAdapterResult:
        """Resolve a ConditionSignature through the governed adapter seam.

        Flow:
        1. Validate input ConditionSignature
        2. Invoke ALEXANDER resolution pipeline
        3. Validate output ResolutionResult
        4. Return governed RuntimeAdapterResult

        Fail-closed: any error at any stage returns a failed result
        with structured error information.
        """
        # ── Stage 1: Validate input ──
        input_errors = validate_condition_signature(condition)
        if input_errors:
            return RuntimeAdapterResult(
                success=False,
                resolution_result=None,
                adapter_errors=input_errors,
            )

        # ── Stage 2: Invoke engine (fail-closed on exception) ──
        try:
            resolution_result = self._engine.resolve(condition, self._kernel)
        except Exception as exc:
            return RuntimeAdapterResult(
                success=False,
                resolution_result=None,
                adapter_errors=[RuntimeAdapterError(
                    code="ENGINE_INVOCATION_FAILED",
                    message=f"ALEXANDER engine raised an exception: {exc}",
                    stage="engine_invocation",
                    details={"exception_type": type(exc).__name__},
                )],
            )

        # ── Stage 3: Validate output ──
        output_errors = validate_resolution_result(resolution_result)
        if output_errors:
            return RuntimeAdapterResult(
                success=False,
                resolution_result=None,
                adapter_errors=output_errors,
            )

        # ── Stage 4: Return governed result ──
        return RuntimeAdapterResult(
            success=True,
            resolution_result=resolution_result,
            adapter_errors=[],
        )
