"""
Impact Overlay Surface

Renders the impact overlay by delegating to runtime
OverlayEngine.get_impact_overlay.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute impact sets independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class ImpactOverlaySurface:
    """Surface for rendering the impact overlay for a specific node.

    Delegates all impact computation to runtime NavigationService.
    Does not compute impact sets independently.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, node_id: str) -> dict[str, Any]:
        """Render the impact overlay for the given node.

        Calls OverlayEngine.get_impact_overlay via runtime.
        Returns all downstream impacts as computed by runtime.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to analyze for downstream impact.

        Returns
        -------
        dict:
            Impact overlay data with downstream impacted nodes.
        """
        # Delegate to runtime — surface does not compute impact sets
        downstream = self._service.get_downstream_impacts(graph, node_id)
        artifact_impacts = self._service.get_artifact_impacts(graph, node_id)
        package_impacts = self._service.get_package_impacts(graph, node_id)
        revision_impacts = self._service.get_revision_impacts(graph, node_id)

        return {
            "view_type": "overlay",
            "overlay": "impact",
            "node_id": node_id,
            "downstream_impacts": [_node_to_dict(n) for n in downstream],
            "artifact_impacts": [_node_to_dict(n) for n in artifact_impacts],
            "package_impacts": [_node_to_dict(n) for n in package_impacts],
            "revision_impacts": [_node_to_dict(n) for n in revision_impacts],
            "metadata": {
                "source": "runtime.navigation.OverlayEngine",
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
