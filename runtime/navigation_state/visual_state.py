"""VisualStateMapper — maps runtime readiness outputs to visual state strings.

This module maps DIRECTLY from runtime readiness outputs. It does NOT redefine
readiness semantics. It explicitly distinguishes hard facts vs enrichment vs
unknown vs incomplete.
"""

from __future__ import annotations


class VisualStateMapper:
    """Maps readiness chain outputs to a finite set of visual states.

    Visual states are a presentation-layer concept: they tell the UI what
    colour/icon to use without reinterpreting the underlying readiness logic.
    """

    VISUAL_STATES: set[str] = {"ready", "pending", "blocked", "completed", "unknown"}

    # Map from runtime state_summary status values to visual states.
    _STATUS_TO_VISUAL: dict[str, str] = {
        "ready": "ready",
        "pending": "pending",
        "blocked": "blocked",
        "completed": "completed",
        "resolved": "completed",
        "in_progress": "pending",
    }

    def __init__(self) -> None:
        pass

    def map_readiness_to_visual(self, readiness_state: str | None) -> str:
        """Map a readiness state string to a visual state.

        Parameters
        ----------
        readiness_state:
            The readiness state from runtime outputs (e.g. from
            ReadinessRouter.get_readiness_chain or a node's state_summary["status"]).
            May be None or empty if the source state is incomplete.

        Returns
        -------
        str
            One of the VISUAL_STATES values. Returns "unknown" for any
            unrecognised or missing input — incomplete source state is never hidden.
        """
        if readiness_state is None or readiness_state == "":
            return "unknown"

        return self._STATUS_TO_VISUAL.get(readiness_state, "unknown")

    def map_readiness_chain_to_visual(self, readiness_chain: dict) -> str:
        """Map a full readiness chain dict (from ReadinessRouter) to a visual state.

        This uses the structured output of ReadinessRouter.get_readiness_chain
        to determine visual state from hard-fact readiness logic.

        Parameters
        ----------
        readiness_chain:
            Dict with keys "ready" (bool), "blockers" (list), "dependencies_met" (bool).

        Returns
        -------
        str
            Visual state string.
        """
        if not isinstance(readiness_chain, dict):
            return "unknown"

        if readiness_chain.get("ready") is True:
            return "ready"

        if readiness_chain.get("blockers"):
            return "blocked"

        if readiness_chain.get("dependencies_met") is False:
            return "pending"

        # If we cannot determine state from the chain, be explicit.
        return "unknown"

    def map_node_to_visual(self, node_summary: dict) -> str:
        """Map a node summary dict to a visual state.

        Uses state_summary["status"] if present. Explicitly marks enrichment-
        derived nodes and preserves unknown state for incomplete data.

        Parameters
        ----------
        node_summary:
            A node summary dict with "state_summary" and optionally
            "is_enrichment_derived".

        Returns
        -------
        str
            Visual state string.
        """
        state_summary = node_summary.get("state_summary", {})
        status = state_summary.get("status")
        return self.map_readiness_to_visual(status)

    def annotate_with_visual_state(self, node_summary: dict) -> dict:
        """Return a copy of node_summary with a "visual_state" key added.

        Also adds "visual_state_source" to indicate whether the state came
        from hard facts or enrichment.
        """
        result = dict(node_summary)
        result["visual_state"] = self.map_node_to_visual(node_summary)

        if node_summary.get("is_enrichment_derived", False):
            result["visual_state_source"] = "enrichment"
        else:
            result["visual_state_source"] = "hard_fact"

        return result
