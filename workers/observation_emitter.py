"""Convenience wrapper for emitting Observation events."""

from workers.event_adapter import EventAdapter
from workers.schema_builder import build_event


class ObservationEmitter:
    """Builds and submits Observation events to the Cognitive Bus."""

    @staticmethod
    def emit(event_type: str, payload: dict) -> dict:
        """Build an Observation envelope and submit it.

        Args:
            event_type: Specific type descriptor for this observation.
            payload: Event payload as a dict.

        Returns:
            The admission result dict from the bus.
        """
        event = build_event("Observation", event_type, payload)
        return EventAdapter.submit(event)
