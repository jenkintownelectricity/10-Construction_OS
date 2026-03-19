"""
Readiness Overlay Surface

Renders the readiness overlay by delegating to runtime
OverlayEngine.get_readiness_overlay.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not redefine readiness semantics.

Visual states: ready, pending, blocked, completed, unknown.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


# Valid visual readiness states — surface renders these, does not define them
READINESS_VISUAL_STATES = frozenset({
    "ready",
    "pending",
    "blocked",
    "completed",
    "unknown",
})


class ReadinessOverlaySurface:
    """Surface for rendering the readiness overlay across the graph.

    Delegates all readiness computation to runtime NavigationService.
    Does not redefine readiness semantics — only renders runtime state.

    Visual states: ready, pending, blocked, completed, unknown.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph) -> dict[str, Any]:
        """Render the readiness overlay for the entire graph.

        Calls OverlayEngine.get_readiness_overlay via runtime.
        Maps each node to its visual readiness state as returned
        by runtime. Does not redefine readiness semantics.

        Parameters
        ----------
        graph:
            The condition graph snapshot.

        Returns
        -------
        dict:
            Readiness overlay data with per-node visual states.
        """
        # Delegate to runtime — surface does not redefine readiness
        all_nodes = graph.get_all_nodes() if hasattr(graph, "get_all_nodes") else []

        node_states: list[dict[str, Any]] = []
        for node in all_nodes:
            node_id = node.id if hasattr(node, "id") else str(node)
            readiness_info = self._service.get_readiness_chain(graph, node_id)

            # Extract readiness state from runtime response
            state = "unknown"
            if isinstance(readiness_info, dict):
                state = readiness_info.get("readiness_state", "unknown")
            elif hasattr(readiness_info, "readiness_state"):
                state = getattr(readiness_info, "readiness_state", "unknown")

            # Validate state against known visual states
            if state not in READINESS_VISUAL_STATES:
                state = "unknown"

            node_states.append({
                "node_id": node_id,
                "readiness_state": state,
                "readiness_detail": readiness_info,
            })

        return {
            "view_type": "overlay",
            "overlay": "readiness",
            "valid_states": sorted(READINESS_VISUAL_STATES),
            "node_states": node_states,
            "metadata": {
                "source": "runtime.navigation.OverlayEngine",
                "derived": True,
            },
        }
