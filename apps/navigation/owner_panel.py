"""
Owner Panel Surface

Renders owner information by delegating to runtime
NavigationQueryEngine.get_owner_panel.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not resolve owner assignments independently.

CRITICAL: owner_state="unknown" MUST be preserved explicitly.
The surface never hides, assumes, or overrides unknown owner state.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class OwnerPanelSurface:
    """Surface for rendering owner panels.

    Delegates all owner resolution to runtime NavigationService.
    MUST preserve owner_state="unknown" explicitly — never hidden or assumed.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, node_id: str) -> dict[str, Any]:
        """Render the owner panel for the given node.

        Calls NavigationQueryEngine.get_owner_panel via runtime.
        Returns owner data as-is from runtime.

        CRITICAL: owner_state="unknown" is preserved explicitly.
        The surface never hides, assumes, or overrides unknown owner state.
        Incomplete source state is shown as incomplete, not hidden.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to inspect for owner information.

        Returns
        -------
        dict:
            Owner panel data with explicit owner_state field.
        """
        # Delegate to runtime — surface does not resolve owners
        owner_info = self._service.get_owner_route(graph, node_id)
        owner_responsibility = self._service.get_owner_responsibility(graph, node_id)

        # CRITICAL: Preserve owner_state="unknown" explicitly
        owner_state = "unknown"
        if isinstance(owner_info, dict):
            owner_state = owner_info.get("owner_state", "unknown")
        elif isinstance(owner_responsibility, dict):
            owner_state = owner_responsibility.get("owner_state", "unknown")

        return {
            "view_type": "detail",
            "panel": "owner",
            "node_id": node_id,
            "owner_info": owner_info,
            "owner_responsibility": owner_responsibility,
            "owner_state": owner_state,
            "owner_state_explicit": True,
            "metadata": {
                "source": "runtime.navigation.NavigationQueryEngine",
                "derived": True,
                "owner_state_preserved": True,
                "owner_state_value": owner_state,
            },
        }
