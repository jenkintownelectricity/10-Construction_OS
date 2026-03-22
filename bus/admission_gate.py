"""
Construction Cognitive Bus v0.1 — Admission gate.

The single entry point for all cognitive events. Validates schema,
emitter policy, event class, required fields, and payload size.
Appends to the appropriate log and returns a structured result.

Fail-closed: any uncertainty results in rejection.
"""

import json
import os

from bus.config import (
    ALLOWED_EVENT_CLASSES,
    MAX_PAYLOAD_BYTES,
    SCHEMA_VERSION,
)
from bus.emitter_policy import validate_emitter
from bus.event_log import append_event
from bus.models import make_admission_record, make_rejection_record
from bus.rejection_log import append_rejection
from bus.router import route

REQUIRED_FIELDS = (
    "event_id",
    "event_class",
    "event_type",
    "schema_version",
    "source_component",
    "source_repo",
    "timestamp",
    "payload",
)


def _reject(event, reason):
    """Record rejection and return structured result."""
    record = make_rejection_record(event, reason)
    path = append_rejection(record)
    return {
        "admitted": False,
        "reason": reason,
        "rejection_path": path,
    }


def receive_event(event: dict | None) -> dict:
    """Process an incoming event through the admission pipeline.

    Returns a structured result dict with keys:
        admitted: bool
        reason: str
        And either admission_path/routing or rejection_path.
    """
    # --- Null / non-dict guard ---
    if not isinstance(event, dict):
        return _reject(None, "event is not a dict or is None")

    # --- Required fields ---
    for field in REQUIRED_FIELDS:
        if field not in event or event[field] is None:
            return _reject(event, f"missing required field: {field}")
        if isinstance(event[field], str) and not event[field].strip():
            return _reject(event, f"empty required field: {field}")

    # --- Schema version ---
    if event["schema_version"] != SCHEMA_VERSION:
        return _reject(
            event,
            f"unsupported schema_version: {event['schema_version']} (expected {SCHEMA_VERSION})",
        )

    # --- Event class ---
    if event["event_class"] not in ALLOWED_EVENT_CLASSES:
        return _reject(event, f"invalid event_class: {event['event_class']}")

    # --- Emitter policy ---
    allowed, emitter_reason = validate_emitter(event["source_component"])
    if not allowed:
        return _reject(event, emitter_reason)

    # --- Payload type check ---
    if not isinstance(event["payload"], dict):
        return _reject(event, "payload must be a JSON object (dict)")

    # --- Payload size ---
    payload_bytes = len(json.dumps(event["payload"], sort_keys=True).encode("utf-8"))
    if payload_bytes > MAX_PAYLOAD_BYTES:
        return _reject(
            event,
            f"payload exceeds size limit: {payload_bytes} bytes > {MAX_PAYLOAD_BYTES} bytes",
        )

    # --- ExternallyValidatedEvent documentation check ---
    if event["event_class"] == "ExternallyValidatedEvent":
        if not event.get("authority_status"):
            return _reject(
                event,
                "ExternallyValidatedEvent requires authority_status identifying the upstream governed system",
            )

    # --- Admit ---
    record = make_admission_record(event)
    path = append_event(record)
    routing = route(event)

    return {
        "admitted": True,
        "reason": "admitted",
        "admission_path": path,
        "content_hash": record["content_hash"],
        "routing": routing,
    }
