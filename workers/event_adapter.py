"""Core adapter for submitting event envelopes to the Cognitive Bus.

Calls the bus admission gate directly (local function call, no network).
"""

import sys

# Ensure the sibling Cognitive Bus repo is importable.
_BUS_REPO = "/home/user/Construction_Cognitive_Bus"
if _BUS_REPO not in sys.path:
    sys.path.insert(0, _BUS_REPO)

from bus.admission_gate import receive_event  # noqa: E402


class EventAdapter:
    """Submits a fully-built event envelope to the Cognitive Bus."""

    @staticmethod
    def submit(event: dict) -> dict:
        """Submit an event envelope to the bus admission gate.

        Args:
            event: A complete event envelope dict (built by schema_builder).

        Returns:
            The admission result dict from the bus.
        """
        return receive_event(event)
