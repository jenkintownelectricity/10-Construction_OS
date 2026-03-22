"""Typed payload models for each required runtime event.

All payloads are strictly factual. No inferences. No cognitive interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class ConditionDetectedPayload:
    """Payload for ConditionDetected event — pipeline entry checkpoint."""

    condition_signature_id: str
    node_type: str
    pipeline_stage: str
    project_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v != ""}


@dataclass(frozen=True)
class DetailResolvedPayload:
    """Payload for DetailResolved event — resolution success checkpoint."""

    condition_signature_id: str
    resolved_detail_id: str
    resolution_source: str
    pipeline_stage: str
    pattern_id: str = ""
    variant_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v != ""}


@dataclass(frozen=True)
class ArtifactRenderedPayload:
    """Payload for ArtifactRendered event — artifact success checkpoint."""

    artifact_id: str
    artifact_type: str
    renderer_name: str
    pipeline_stage: str
    instruction_set_id: str = ""
    lineage_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v != ""}


@dataclass(frozen=True)
class ValidationFailedPayload:
    """Payload for ValidationFailed event — validation failure checkpoint."""

    validation_stage: str
    error_code: str
    failure_reason: str
    pipeline_stage: str
    object_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v != ""}


@dataclass(frozen=True)
class RuntimeErrorPayload:
    """Payload for RuntimeError event — unexpected runtime failure checkpoint."""

    exception_type: str
    failure_reason: str
    pipeline_stage: str
    error_code: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v != ""}


PAYLOAD_TYPES = {
    "ConditionDetected": ConditionDetectedPayload,
    "DetailResolved": DetailResolvedPayload,
    "ArtifactRendered": ArtifactRenderedPayload,
    "ValidationFailed": ValidationFailedPayload,
    "RuntimeError": RuntimeErrorPayload,
}
