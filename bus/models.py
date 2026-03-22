"""
Construction Cognitive Bus v0.1 — Data models.

Immutable record types for events, admission results, and rejection records.
All models use plain dicts for serialization. No ORM. No framework types.
"""

import hashlib
import json
from datetime import datetime, timezone


def compute_content_hash(event: dict) -> str:
    """Compute a deterministic SHA-256 hash of the event content.

    Uses sorted-key JSON serialization to ensure determinism.
    """
    canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def make_admission_record(event: dict) -> dict:
    """Create an immutable admission record wrapping the original event."""
    return {
        "record_type": "admitted",
        "event": event,
        "content_hash": compute_content_hash(event),
        "admission_timestamp": datetime.now(timezone.utc).isoformat(),
        "admission_decision": "admitted",
    }


def make_rejection_record(event: dict | None, reason: str) -> dict:
    """Create an immutable rejection record.

    event may be None if the raw input was entirely unparseable.
    """
    return {
        "record_type": "rejected",
        "event": event,
        "rejection_timestamp": datetime.now(timezone.utc).isoformat(),
        "rejection_reason": reason,
    }


def make_routing_decision(event: dict, targets: list[str]) -> dict:
    """Create a routing decision (advisory only — no delivery)."""
    return {
        "event_id": event.get("event_id"),
        "event_class": event.get("event_class"),
        "targets": list(targets),
    }
