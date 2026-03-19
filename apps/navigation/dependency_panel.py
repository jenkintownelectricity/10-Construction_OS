"""
Dependency Panel Surface

Renders dependency information by delegating to runtime
NavigationQueryEngine.get_dependency_panel.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute dependency graphs independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class DependencyPanelSurface:
    """Surface for rendering dependency panels.

    Delegates all dependency computation to runtime NavigationService.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, node_id: str) -> dict[str, Any]:
        """Render the dependency panel for the given node.

        Calls NavigationQueryEngine.get_dependency_panel via runtime.
        Returns dependency data as-is from runtime — no independent
        dependency graph computation.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to inspect for dependencies.

        Returns
        -------
        dict:
            Dependency panel data including immediate dependencies
            and upstream dependency chain.
        """
        # Delegate to runtime — surface does not compute dependency graphs
        dependencies = self._service.get_dependencies(graph, node_id)
        upstream = self._service.get_upstream_dependencies(graph, node_id)

        return {
            "view_type": "detail",
            "panel": "dependency",
            "node_id": node_id,
            "immediate_dependencies": [_node_to_dict(d) for d in dependencies],
            "upstream_chain": [_node_to_dict(d) for d in upstream],
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
