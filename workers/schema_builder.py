"""Builds valid Cognitive Bus event envelope dicts.

Workers may only build Observation and Proposal envelopes.
ExternallyValidatedEvent is explicitly refused.
"""

import json
import uuid
from datetime import datetime, timezone

from workers.config import (
    ALLOWED_WORKER_EVENT_CLASSES,
    DENIED_WORKER_EVENT_CLASSES,
    SCHEMA_VERSION,
    SOURCE_COMPONENT,
    SOURCE_REPO,
)

# Mirror the bus payload size limit (64 KiB).
MAX_PAYLOAD_BYTES = 65536


def build_event(event_class: str, event_type: str, payload: dict) -> dict:
    """Build a complete event envelope dict.

    Args:
        event_class: Must be 'Observation' or 'Proposal'.
        event_type: Specific type descriptor within the event class.
        payload: Event payload as a dict.

    Returns:
        A dict matching the Cognitive Bus event envelope schema.

    Raises:
        ValueError: If event_class is denied or unsupported, payload is
            not a dict, or payload exceeds the size limit.
    """
    # --- Guard: denied event classes ---
    if event_class in DENIED_WORKER_EVENT_CLASSES:
        raise ValueError(
            f"Workers must not emit {event_class}. "
            "Only Observation and Proposal are permitted."
        )

    # --- Guard: allowed event classes ---
    if event_class not in ALLOWED_WORKER_EVENT_CLASSES:
        raise ValueError(
            f"Unsupported event_class: {event_class}. "
            f"Allowed: {sorted(ALLOWED_WORKER_EVENT_CLASSES)}"
        )

    # --- Guard: event_type ---
    if not isinstance(event_type, str) or not event_type.strip():
        raise ValueError("event_type must be a non-empty string.")

    # --- Guard: payload type ---
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict.")

    # --- Guard: payload size ---
    payload_bytes = len(json.dumps(payload, sort_keys=True).encode("utf-8"))
    if payload_bytes > MAX_PAYLOAD_BYTES:
        raise ValueError(
            f"payload exceeds size limit: {payload_bytes} bytes > "
            f"{MAX_PAYLOAD_BYTES} bytes"
        )

    return {
        "event_id": str(uuid.uuid4()),
        "event_class": event_class,
        "event_type": event_type,
        "schema_version": SCHEMA_VERSION,
        "source_component": SOURCE_COMPONENT,
        "source_repo": SOURCE_REPO,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
