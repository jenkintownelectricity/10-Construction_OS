"""Governed runtime event envelope builder.

Builds event envelopes compatible with Construction_Cognitive_Bus admission.
Runtime emits only the fields it owns — bus-derived metadata (admission_decision,
admission_timestamp, content_hash, routing) is never produced by runtime.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from runtime.events.event_types import EVENT_TYPES

# Schema version matching Construction_Cognitive_Bus v0.1 contract
SCHEMA_VERSION = "0.1"

# Source identity constants
SOURCE_COMPONENT = "Construction_Runtime"
SOURCE_REPO = "Construction_Runtime"

# Event class — runtime emits observations only
EVENT_CLASS = "Observation"


class EventBuildError(Exception):
    """Raised when event envelope construction fails deterministically."""


def build_event_envelope(
    event_type: str,
    pipeline_stage: str,
    payload: dict[str, Any],
    condition_signature_id: str = "",
    artifact_id: str = "",
) -> dict[str, Any]:
    """Build a governed event envelope for Cognitive Bus submission.

    Args:
        event_type: One of the five required event types.
        pipeline_stage: The pipeline stage at which this event was produced.
        payload: The typed event payload as a dict.
        condition_signature_id: Optional condition signature ID.
        artifact_id: Optional artifact ID.

    Returns:
        A complete event envelope dict ready for bus submission.

    Raises:
        EventBuildError: If any required field is missing or invalid.
    """
    # Validate event_type
    if event_type not in EVENT_TYPES:
        raise EventBuildError(
            f"Invalid event_type: {event_type!r}. "
            f"Must be one of: {sorted(EVENT_TYPES)}"
        )

    # Validate pipeline_stage
    if not pipeline_stage or not isinstance(pipeline_stage, str):
        raise EventBuildError("pipeline_stage must be a non-empty string")

    # Validate payload
    if not isinstance(payload, dict):
        raise EventBuildError(
            f"payload must be a dict, got {type(payload).__name__}"
        )

    # Build envelope — only runtime-owned fields
    envelope: dict[str, Any] = {
        "event_id": f"rt-{uuid.uuid4().hex}",
        "event_class": EVENT_CLASS,
        "event_type": event_type,
        "schema_version": SCHEMA_VERSION,
        "source_component": SOURCE_COMPONENT,
        "source_repo": SOURCE_REPO,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pipeline_stage": pipeline_stage,
        "payload": payload,
    }

    # Add optional fields when applicable
    if condition_signature_id:
        envelope["condition_signature_id"] = condition_signature_id
    if artifact_id:
        envelope["artifact_id"] = artifact_id

    return envelope
