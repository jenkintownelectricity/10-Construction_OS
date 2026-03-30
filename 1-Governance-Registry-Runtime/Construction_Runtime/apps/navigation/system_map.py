"""
System Map Surface

Renders system-level map data by delegating to runtime
NavigationQueryEngine.get_system_map.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute graph edges or system structure independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class SystemMapSurface:
    """Surface for rendering system-level navigation maps.

    Delegates all system map computation to runtime NavigationService.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, system_id: str) -> dict[str, Any]:
        """Render the system-level map for the given system.

        Calls NavigationQueryEngine.get_system_map via runtime.
        Returns the system map data as-is from runtime — no independent
        graph traversal or system structure computation.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        system_id:
            Identifier of the building system to render.

        Returns
        -------
        dict:
            System map data from runtime.
        """
        # Delegate to runtime — surface does not traverse system edges
        neighborhood = self._service.get_condition_neighborhood(graph, system_id, depth=2)
        return {
            "view_type": "map",
            "projection": "system_map",
            "system_id": system_id,
            "neighborhood": neighborhood,
            "metadata": {
                "source": "runtime.navigation.NavigationQueryEngine",
                "derived": True,
            },
        }
