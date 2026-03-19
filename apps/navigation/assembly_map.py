"""
Assembly Map Surface

Renders assembly-level map data by delegating to runtime
NavigationQueryEngine.get_assembly_map.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute graph edges or assembly structure independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class AssemblyMapSurface:
    """Surface for rendering assembly-level navigation maps.

    Delegates all assembly map computation to runtime NavigationService.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, assembly_id: str) -> dict[str, Any]:
        """Render the assembly-level map for the given assembly.

        Calls NavigationQueryEngine.get_assembly_map via runtime.
        Returns the assembly map data as-is from runtime — no independent
        graph traversal or assembly structure computation.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        assembly_id:
            Identifier of the assembly to render.

        Returns
        -------
        dict:
            Assembly map data from runtime.
        """
        # Delegate to runtime — surface does not traverse assembly edges
        neighborhood = self._service.get_condition_neighborhood(graph, assembly_id, depth=2)
        return {
            "view_type": "map",
            "projection": "assembly_map",
            "assembly_id": assembly_id,
            "neighborhood": neighborhood,
            "metadata": {
                "source": "runtime.navigation.NavigationQueryEngine",
                "derived": True,
            },
        }
