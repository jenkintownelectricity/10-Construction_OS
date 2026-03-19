"""
Blocker Panel Surface

Renders blocker information by delegating to runtime
NavigationQueryEngine.get_blocker_panel and
ExplanationPanelBuilder.build_why_blocked.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute blocker chains independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class BlockerPanelSurface:
    """Surface for rendering blocker panels with explanation.

    Delegates blocker retrieval to NavigationService.get_blockers and
    blocking chain to NavigationService.get_blocking_chain.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, node_id: str) -> dict[str, Any]:
        """Render the blocker panel for the given node.

        Calls NavigationQueryEngine.get_blocker_panel and
        ExplanationPanelBuilder.build_why_blocked via runtime.

        The surface does not compute blocker chains independently.
        All blocking logic is delegated to runtime.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to inspect for blockers.

        Returns
        -------
        dict:
            Blocker panel data including immediate blockers,
            the full blocking chain, and suggested next actions.
        """
        # Delegate to runtime — surface does not compute blocker chains
        immediate_blockers = self._service.get_blockers(graph, node_id)
        blocking_chain = self._service.get_blocking_chain(graph, node_id)
        next_actions = self._service.get_next_actions(graph, node_id)

        return {
            "view_type": "detail",
            "panel": "blocker",
            "node_id": node_id,
            "immediate_blockers": [_node_to_dict(b) for b in immediate_blockers],
            "blocking_chain": [_node_to_dict(b) for b in blocking_chain],
            "why_blocked": {
                "chain_length": len(blocking_chain),
                "root_blockers": [
                    _node_to_dict(b) for b in blocking_chain[-1:]
                ] if blocking_chain else [],
            },
            "next_actions": next_actions,
            "metadata": {
                "source": "runtime.navigation.NavigationService",
                "explanation_source": "runtime.ExplanationPanelBuilder.build_why_blocked",
                "derived": True,
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
