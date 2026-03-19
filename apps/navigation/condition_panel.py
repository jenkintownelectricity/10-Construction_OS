"""
Condition Panel Surface

Renders condition detail data by delegating to runtime
NavigationQueryEngine.get_condition_detail.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute condition resolution independently.
Owner state is preserved explicitly — owner_state="unknown" is shown
as unknown, never hidden or assumed.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class ConditionPanelSurface:
    """Surface for rendering condition detail panels.

    Delegates all condition detail computation to runtime NavigationService.
    Preserves owner_state="unknown" explicitly.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, condition_node_id: str) -> dict[str, Any]:
        """Render the condition detail panel for the given node.

        Calls NavigationQueryEngine.get_condition_detail via runtime.
        Returns the condition detail data as-is from runtime.

        IMPORTANT: owner_state="unknown" is displayed explicitly.
        Incomplete source state is shown as incomplete, not hidden.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        condition_node_id:
            Identifier of the condition node to inspect.

        Returns
        -------
        dict:
            Condition detail data from runtime.
        """
        # Delegate to runtime — surface does not resolve conditions
        neighborhood = self._service.get_condition_neighborhood(
            graph, condition_node_id, depth=1
        )
        blockers = self._service.get_blockers(graph, condition_node_id)
        owner_info = self._service.get_owner_route(graph, condition_node_id)
        readiness = self._service.get_readiness_chain(graph, condition_node_id)
        enrichment_edges = self._service.get_enrichment_edges(graph, condition_node_id)

        # Preserve owner_state="unknown" explicitly — never hide or assume
        owner_state = owner_info.get("owner_state", "unknown") if isinstance(owner_info, dict) else "unknown"

        return {
            "view_type": "detail",
            "panel": "condition",
            "condition_node_id": condition_node_id,
            "neighborhood": neighborhood,
            "blockers": [_node_to_dict(b) for b in blockers],
            "owner_info": owner_info,
            "owner_state": owner_state,
            "readiness": readiness,
            "enrichment_edges": enrichment_edges,
            "metadata": {
                "source": "runtime.navigation.NavigationQueryEngine",
                "derived": True,
                "owner_state_explicit": True,
            },
        }


def _node_to_dict(node: Any) -> dict[str, Any]:
    """Convert a graph node to a serializable dict."""
    if isinstance(node, dict):
        return node
    result: dict[str, Any] = {}
    for attr in ("id", "node_type", "readiness_state", "owner_state"):
        if hasattr(node, attr):
            result[attr] = getattr(node, attr)
    return result
