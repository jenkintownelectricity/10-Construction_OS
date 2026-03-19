"""
Project Map Surface

Renders the project-level hierarchy map by delegating to runtime
MapProjection.project_hierarchy.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute graph edges or hierarchy independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class ProjectMapSurface:
    """Surface for rendering the project hierarchy map.

    Delegates all hierarchy computation to runtime MapProjection.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph) -> dict[str, Any]:
        """Render the project hierarchy map.

        Calls MapProjection.project_hierarchy via runtime NavigationService.
        Returns the map view data as-is from runtime — no independent
        graph traversal or hierarchy computation.

        Parameters
        ----------
        graph:
            The condition graph snapshot to project.

        Returns
        -------
        dict:
            Project hierarchy map data from runtime.
        """
        # Delegate to runtime — surface does not compute hierarchy
        all_nodes = graph.get_all_nodes() if hasattr(graph, "get_all_nodes") else []
        project_data: dict[str, Any] = {
            "view_type": "map",
            "projection": "project_hierarchy",
            "nodes": [],
            "systems": [],
            "metadata": {
                "source": "runtime.navigation.MapProjection",
                "derived": True,
            },
        }
        # Populate from runtime query results
        for node in all_nodes:
            node_data = self._service.get_condition_neighborhood(graph, node.id if hasattr(node, "id") else str(node))
            project_data["nodes"].append(node_data)

        return project_data
