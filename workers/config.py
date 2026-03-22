"""Worker identity constants and schema configuration."""

SOURCE_COMPONENT = "Construction_Intelligence_Workers"
SOURCE_REPO = "Construction_Intelligence_Workers"
SCHEMA_VERSION = "0.1"

# Event classes workers are allowed to emit.
ALLOWED_WORKER_EVENT_CLASSES = frozenset({"Observation", "Proposal"})

# Event classes workers must never emit.
DENIED_WORKER_EVENT_CLASSES = frozenset({"ExternallyValidatedEvent"})
