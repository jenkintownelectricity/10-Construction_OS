"""
Construction Cognitive Bus v0.1 — Configuration constants.

Local configuration for the governed cognitive event/admission layer.
No external config sources. All values are deterministic defaults.
"""

import os

# --- Storage paths (relative to repository root) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENTS_DIR = os.path.join(BASE_DIR, "state", "events")
REJECTIONS_DIR = os.path.join(BASE_DIR, "state", "rejections")

# --- Schema ---
SCHEMA_VERSION = "0.1"
SCHEMA_PATH = os.path.join(
    BASE_DIR, "schemas", "event-envelope.schema.json"
)

# --- Payload size limit (bytes) ---
MAX_PAYLOAD_BYTES = 65536  # 64 KiB

# --- Allowed emitters (source_component values) ---
ALLOWED_EMITTERS = frozenset({
    "Construction_Intelligence_Workers",
    "Construction_Reference_Intelligence",
    "Construction_Runtime",
})

# --- Allowed event classes ---
ALLOWED_EVENT_CLASSES = frozenset({
    "Observation",
    "Proposal",
    "ExternallyValidatedEvent",
})

# --- Explicitly denied emitters ---
DENIED_EMITTERS = frozenset({
    "Construction_Assistant",
})
