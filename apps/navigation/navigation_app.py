"""
Navigation App — Main Entry Point

Main entry point for the navigation application surface.
Holds references to runtime services and delegates all queries.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute graph edges, blocker chains,
owner routes, or impact sets independently.
"""

from __future__ import annotations

from typing import Any

from runtime.navigation.navigation_service import NavigationService
from runtime.graph.condition_graph import ConditionGraph

from apps.navigation.project_map import ProjectMapSurface
from apps.navigation.system_map import SystemMapSurface
from apps.navigation.assembly_map import AssemblyMapSurface
from apps.navigation.condition_panel import ConditionPanelSurface
from apps.navigation.filter_bar import FilterBarSurface
from apps.navigation.view_switcher import ViewSwitcherSurface


class NavigationApp:
    """Main navigation application surface.

    Holds a reference to the ConditionGraph and runtime NavigationService.
    All methods delegate to runtime — no independent graph computation.
    """

    def __init__(self, graph: ConditionGraph) -> None:
        """Store graph and initialize runtime service references.

        Parameters
        ----------
        graph:
            The condition graph snapshot to navigate.
        """
        self._graph = graph
        self._navigation_service = NavigationService()
        self._project_map = ProjectMapSurface()
        self._system_map = SystemMapSurface()
        self._assembly_map = AssemblyMapSurface()
        self._condition_panel = ConditionPanelSurface()
        self._filter_bar = FilterBarSurface()
        self._view_switcher = ViewSwitcherSurface()

    # ------------------------------------------------------------------
    # Top-level navigation queries — all delegate to runtime
    # ------------------------------------------------------------------

    def get_project_overview(self) -> dict[str, Any]:
        """Return the project map by delegating to ProjectMapSurface.

        Surface only: all hierarchy computation is performed by runtime.
        """
        return self._project_map.render(self._graph)

    def get_system_detail(self, system_id: str) -> dict[str, Any]:
        """Return system-level map data by delegating to SystemMapSurface.

        Surface only: all system traversal is performed by runtime.
        """
        return self._system_map.render(self._graph, system_id)

    def get_assembly_detail(self, assembly_id: str) -> dict[str, Any]:
        """Return assembly-level map data by delegating to AssemblyMapSurface.

        Surface only: all assembly traversal is performed by runtime.
        """
        return self._assembly_map.render(self._graph, assembly_id)

    def get_condition_detail(self, node_id: str) -> dict[str, Any]:
        """Return condition detail by delegating to ConditionPanelSurface.

        Surface only: all condition resolution is performed by runtime.
        """
        return self._condition_panel.render(self._graph, node_id)

    def switch_view(self, view_type: str) -> dict[str, Any]:
        """Switch between map, list, and detail views.

        Delegates to ViewSwitcherSurface which calls runtime ViewBuilder.
        Returns view data for the requested view type.
        """
        return self._view_switcher.switch(view_type, self._graph)

    def apply_filters(self, filters: dict[str, Any]) -> dict[str, Any]:
        """Apply filters to the current navigation view.

        Delegates to FilterBarSurface which calls runtime FilterEngine.
        Filters are derived views only — they do not redefine the graph.
        """
        return self._filter_bar.apply(self._graph, filters)
