"""
Package Panel Surface

Renders package information by delegating to runtime
NavigationQueryEngine.get_package_panel.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute package relationships independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class PackagePanelSurface:
    """Surface for rendering package panels.

    Delegates all package retrieval to runtime NavigationService.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, node_id: str) -> dict[str, Any]:
        """Render the package panel for the given node.

        Calls NavigationQueryEngine.get_package_panel via runtime.
        Returns package data as-is from runtime — no independent
        package relationship computation.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to inspect for packages.

        Returns
        -------
        dict:
            Package panel data from runtime.
        """
        # Delegate to runtime — surface does not compute package relationships
        package_impacts = self._service.get_package_impacts(graph, node_id)
        neighborhood = self._service.get_condition_neighborhood(graph, node_id, depth=1)

        return {
            "view_type": "detail",
            "panel": "package",
            "node_id": node_id,
            "package_impacts": [_node_to_dict(p) for p in package_impacts],
            "neighborhood": neighborhood,
            "metadata": {
                "source": "runtime.navigation.NavigationQueryEngine",
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
