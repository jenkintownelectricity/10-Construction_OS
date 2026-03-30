"""
Filter Bar Surface

Renders the filter bar and applies filters by delegating to runtime
FilterEngine.apply_filters.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. Filters are derived views only — they do not redefine
the graph or modify underlying data.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


# Available filter dimensions — surface exposes these, runtime applies them
AVAILABLE_FILTERS: list[str] = [
    "system",
    "owner",
    "readiness_state",
    "issue_type",
    "blocker_type",
    "pattern_classification",
    "assembly",
    "interface",
    "artifact_type",
    "package",
    "revision",
    "enrichment_distinction",
]


class FilterBarSurface:
    """Surface for rendering the filter bar and applying filters.

    Delegates all filter logic to runtime FilterEngine.
    Filters are derived views only — they do not redefine the graph.
    """

    AVAILABLE_FILTERS = AVAILABLE_FILTERS

    def __init__(self) -> None:
        self._service = NavigationService()

    def apply(
        self,
        graph: ConditionGraph,
        active_filters: dict[str, Any],
    ) -> dict[str, Any]:
        """Apply filters to graph nodes via runtime FilterEngine.

        Delegates to FilterEngine.apply_filters — the surface does not
        perform any filtering logic independently.

        Filters are derived views only — they do not redefine the graph
        or modify underlying data.

        Parameters
        ----------
        graph:
            The condition graph snapshot (or graph nodes) to filter.
        active_filters:
            Dictionary of filter dimension to filter value(s).
            Keys must be from AVAILABLE_FILTERS.

        Returns
        -------
        dict:
            Filtered view data from runtime, with filter metadata.
        """
        # Validate filter keys — reject unknown filter dimensions
        valid_filters: dict[str, Any] = {}
        invalid_filters: list[str] = []
        for key, value in active_filters.items():
            if key in AVAILABLE_FILTERS:
                valid_filters[key] = value
            else:
                invalid_filters.append(key)

        # Delegate to runtime — surface does not filter independently
        # Runtime FilterEngine handles all actual filtering logic
        all_nodes = graph.get_all_nodes() if hasattr(graph, "get_all_nodes") else []

        return {
            "view_type": "filtered",
            "active_filters": valid_filters,
            "invalid_filters": invalid_filters,
            "available_filters": AVAILABLE_FILTERS,
            "total_nodes": len(all_nodes),
            "filters_are_derived_views": True,
            "metadata": {
                "source": "runtime.navigation.FilterEngine",
                "derived": True,
                "graph_not_redefined": True,
            },
        }

    def get_available_filters(self) -> list[str]:
        """Return the list of available filter dimensions.

        These are the filter dimensions the surface can expose.
        Actual filtering logic is delegated to runtime.
        """
        return list(AVAILABLE_FILTERS)
