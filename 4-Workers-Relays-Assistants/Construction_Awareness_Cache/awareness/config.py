"""
Construction Awareness Cache v0.1 — Configuration constants.

Local configuration only. No external config sources.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(BASE_DIR, "state")
EVENTS_DIR = os.path.join(STATE_DIR, "events")
SNAPSHOTS_DIR = os.path.join(STATE_DIR, "snapshots")

SCHEMA_VERSION = "0.1"

ALLOWED_EVENT_CLASSES = frozenset({
    "Observation",
    "Proposal",
    "ExternallyValidatedEvent",
})

REQUIRED_EVENT_FIELDS = (
    "event_id",
    "event_class",
    "event_type",
    "schema_version",
    "source_component",
    "source_repo",
    "timestamp",
    "payload",
)

MAX_PAYLOAD_BYTES = 65536  # 64 KiB
