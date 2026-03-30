"""
Construction Awareness Cache v0.1 — Validation gate.

Validates ingested records have required fields and valid event classes.
Fail closed: any malformed record is rejected.
"""

from . import config


class ValidationGate:
    """Validates ingested event records before compilation."""

    def validate(self, events: list[dict]) -> tuple[list[dict], list[dict]]:
        """Validate a list of event dicts.

        Returns (valid, rejected) where each is a list of event dicts.
        Rejected entries include a '_rejection_reason' key.
        """
        valid = []
        rejected = []
        for event in events:
            reason = self._check(event)
            if reason is None:
                valid.append(event)
            else:
                rejected.append({**event, "_rejection_reason": reason})
        return valid, rejected

    def _check(self, event: dict) -> str | None:
        """Return a rejection reason string, or None if valid."""
        if not isinstance(event, dict):
            return "not a dict"

        for field in config.REQUIRED_EVENT_FIELDS:
            if field not in event:
                return f"missing required field: {field}"

        event_class = event.get("event_class")
        if event_class not in config.ALLOWED_EVENT_CLASSES:
            return f"invalid event_class: {event_class}"

        if event.get("schema_version") != config.SCHEMA_VERSION:
            return f"unsupported schema_version: {event.get('schema_version')}"

        if not isinstance(event.get("payload"), dict):
            return "payload is not a dict"

        return None
