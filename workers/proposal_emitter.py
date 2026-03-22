"""Convenience wrapper for emitting Proposal events."""

from workers.event_adapter import EventAdapter
from workers.schema_builder import build_event


class ProposalEmitter:
    """Builds and submits Proposal events to the Cognitive Bus."""

    @staticmethod
    def emit(event_type: str, payload: dict) -> dict:
        """Build a Proposal envelope and submit it.

        Args:
            event_type: Specific type descriptor for this proposal.
            payload: Event payload as a dict.

        Returns:
            The admission result dict from the bus.
        """
        event = build_event("Proposal", event_type, payload)
        return EventAdapter.submit(event)
