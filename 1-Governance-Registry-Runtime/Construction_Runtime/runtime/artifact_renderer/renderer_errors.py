"""Renderer error taxonomy for artifact rendering pipeline.

All renderer errors are classified, fail-closed, and surfaced
with structured metadata. No silent failures permitted.
"""


class RendererError(Exception):
    """Base error for all renderer failures."""

    def __init__(self, code: str, message: str, context: dict | None = None):
        self.code = code
        self.message = message
        self.context = context or {}
        super().__init__(f"[{code}] {message}")

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "context": self.context,
        }


class UnsupportedPrimitiveError(RendererError):
    """Raised when a geometry primitive type is not supported."""

    def __init__(self, primitive_type: str):
        super().__init__(
            code="RENDER_UNSUPPORTED_PRIMITIVE",
            message=f"Unsupported geometry primitive: '{primitive_type}'.",
            context={"primitive_type": primitive_type},
        )


class MissingLayerError(RendererError):
    """Raised when a required layer is missing from the instruction set."""

    def __init__(self, layer: str):
        super().__init__(
            code="RENDER_MISSING_LAYER",
            message=f"Required layer missing from instruction set: '{layer}'.",
            context={"layer": layer},
        )


class InvalidInstructionSetError(RendererError):
    """Raised when an instruction set fails validation."""

    def __init__(self, reason: str, errors: list | None = None):
        super().__init__(
            code="RENDER_INVALID_INSTRUCTION_SET",
            message=f"Instruction set validation failed: {reason}",
            context={"reason": reason, "errors": errors or []},
        )


class RendererNotFoundError(RendererError):
    """Raised when a requested renderer format is not registered."""

    def __init__(self, format_name: str):
        super().__init__(
            code="RENDER_RENDERER_NOT_FOUND",
            message=f"No renderer registered for format: '{format_name}'.",
            context={"format_name": format_name},
        )


class ManifestError(RendererError):
    """Raised when the rendering manifest is invalid or incomplete."""

    def __init__(self, reason: str):
        super().__init__(
            code="RENDER_MANIFEST_ERROR",
            message=f"Manifest error: {reason}",
            context={"reason": reason},
        )


class LineageError(RendererError):
    """Raised when artifact lineage tracking fails."""

    def __init__(self, reason: str):
        super().__init__(
            code="RENDER_LINEAGE_ERROR",
            message=f"Lineage tracking error: {reason}",
            context={"reason": reason},
        )


class PipelineError(RendererError):
    """Raised when the rendering pipeline encounters a fatal error."""

    def __init__(self, stage: str, reason: str, cause: Exception | None = None):
        super().__init__(
            code="RENDER_PIPELINE_ERROR",
            message=f"Pipeline failed at stage '{stage}': {reason}",
            context={"stage": stage, "reason": reason, "cause": str(cause) if cause else None},
        )


class DeterminismError(RendererError):
    """Raised when renderer output fails determinism check."""

    def __init__(self, format_name: str, expected_hash: str, actual_hash: str):
        super().__init__(
            code="RENDER_DETERMINISM_FAILURE",
            message=f"Non-deterministic output from '{format_name}' renderer.",
            context={
                "format_name": format_name,
                "expected_hash": expected_hash,
                "actual_hash": actual_hash,
            },
        )
