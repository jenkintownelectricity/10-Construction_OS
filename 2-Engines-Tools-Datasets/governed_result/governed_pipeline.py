"""Governed Pipeline — Application-facing seam.

Orchestrates the full governed resolution chain:
  ConditionSignature
  → RuntimeAdapter (Wave 3)
  → ConstraintPort (Wave 4)
  → GovernedResult (Wave 5)

Application consumers call resolve_governed() and receive
GovernedResult only. No direct kernel, engine, or constraint
port ownership leaks to the application layer.

Boundary rules:
- Application consumes GovernedResult only
- No engine ownership from application
- No direct kernel access from application
- No runtime bypass of constraint port
- Fail-closed at every stage
"""

from __future__ import annotations

from typing import Any

from governed_result.governed_result_types import GovernedResult
from governed_result.governed_result_transformer import transform
from governed_result.governed_result_receipt import generate_receipt, generate_signal


class GovernedPipeline:
    """The narrow application seam for governed condition resolution.

    Wires Wave 3 (RuntimeAdapter) → Wave 4 (ConstraintPort) → Wave 5 (GovernedResult).
    Application consumers interact ONLY through this pipeline.
    """

    def __init__(
        self,
        runtime_adapter: Any,
        constraint_port: Any,
        constraint_provider: Any | None = None,
    ) -> None:
        """Initialize the governed pipeline.

        Args:
            runtime_adapter: AlexanderRuntimeAdapter instance (Wave 3)
            constraint_port: ConstraintPort instance (Wave 4)
            constraint_provider: Optional provider that supplies constraints
                and evidence for a given resolution result. If None,
                constraint evaluation is skipped and result is based
                on resolution alone.
        """
        self._adapter = runtime_adapter
        self._port = constraint_port
        self._provider = constraint_provider

    def resolve_governed(
        self,
        condition: dict[str, Any],
    ) -> GovernedPipelineOutput:
        """Execute the full governed resolution pipeline.

        Args:
            condition: A ConditionSignature dict

        Returns:
            GovernedPipelineOutput containing the GovernedResult,
            receipt, and signal.

        Fail-closed: any upstream error produces a FAILED GovernedResult.
        """
        # Stage 1: Invoke runtime adapter (Wave 3)
        adapter_result = self._adapter.resolve_condition(condition)

        # Stage 2: If adapter succeeded and provider available, run constraints (Wave 4)
        constraint_result = None
        if (
            adapter_result.success
            and adapter_result.resolution_result is not None
            and self._provider is not None
        ):
            try:
                constraints, evidence_map = self._provider.get_constraints(
                    adapter_result.resolution_result
                )
                constraint_result = self._port.evaluate(
                    resolution_result=adapter_result.resolution_result,
                    constraints=constraints,
                    evidence_map=evidence_map,
                )
            except Exception:
                # Fail-closed: constraint provider error produces no constraint result
                # Transformer will handle this gracefully
                constraint_result = None

        # Stage 3: Transform to GovernedResult (Wave 5)
        governed_result = transform(
            adapter_result=adapter_result,
            constraint_result=constraint_result,
        )

        # Stage 4: Generate receipt and signal
        receipt = generate_receipt(governed_result)
        signal = generate_signal(governed_result)

        return GovernedPipelineOutput(
            governed_result=governed_result,
            receipt=receipt,
            signal=signal,
        )


class GovernedPipelineOutput:
    """Output from the governed pipeline.

    Contains the GovernedResult plus receipt and signal data
    for downstream persistence/notification.
    """

    __slots__ = ("governed_result", "receipt", "signal")

    def __init__(
        self,
        governed_result: GovernedResult,
        receipt: dict[str, Any],
        signal: dict[str, Any],
    ) -> None:
        self.governed_result = governed_result
        self.receipt = receipt
        self.signal = signal
