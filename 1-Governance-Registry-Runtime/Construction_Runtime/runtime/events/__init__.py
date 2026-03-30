"""Runtime event emission layer.

Deterministic runtime observer events emitted at governed pipeline checkpoints.
Runtime emits facts only — no reasoning, no cognitive interpretation.
All events are published through the Construction_Cognitive_Bus contract.
"""

from runtime.events.event_types import (
    ConditionDetected,
    DetailResolved,
    ArtifactRendered,
    ValidationFailed,
    RuntimeError as RuntimeErrorEvent,
    EVENT_TYPES,
    PIPELINE_STAGES,
)
from runtime.events.event_models import (
    ConditionDetectedPayload,
    DetailResolvedPayload,
    ArtifactRenderedPayload,
    ValidationFailedPayload,
    RuntimeErrorPayload,
)
from runtime.events.event_builder import build_event_envelope
from runtime.events.event_emitter import RuntimeEventEmitter
from runtime.events.bus_adapter import CognitiveBusAdapter

__all__ = [
    "ConditionDetected",
    "DetailResolved",
    "ArtifactRendered",
    "ValidationFailed",
    "RuntimeErrorEvent",
    "EVENT_TYPES",
    "PIPELINE_STAGES",
    "ConditionDetectedPayload",
    "DetailResolvedPayload",
    "ArtifactRenderedPayload",
    "ValidationFailedPayload",
    "RuntimeErrorPayload",
    "build_event_envelope",
    "RuntimeEventEmitter",
    "CognitiveBusAdapter",
]
