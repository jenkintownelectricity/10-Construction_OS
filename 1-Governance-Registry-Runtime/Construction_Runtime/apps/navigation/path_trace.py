"""
Path Trace Surface

Renders path traces (unblock paths, owner routes, impact paths,
dependency chains) by delegating to runtime services.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute paths, routes, or chains independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class PathTraceSurface:
    """Surface for rendering path traces through the condition graph.

    Delegates all path computation to runtime NavigationService.
    Does not compute graph edges, blocker chains, owner routes,
    or impact sets independently.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render_unblock_path(
        self, graph: ConditionGraph, node_id: str
    ) -> dict[str, Any]:
        """Render the unblock path for the given node.

        Calls ReadinessRouter.get_unblock_path via runtime.
        Returns the topologically sorted unblock path as-is from runtime.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the blocked node to trace unblock path for.

        Returns
        -------
        dict:
            Unblock path data from runtime.
        """
        # Delegate to runtime — surface does not compute unblock paths
        unblock_path = self._service.get_unblock_path(graph, node_id)
        return {
            "trace_type": "unblock_path",
            "node_id": node_id,
            "path": [_node_to_dict(n) for n in unblock_path],
            "path_length": len(unblock_path),
            "metadata": {
                "source": "runtime.readiness_routing.ReadinessRouter",
                "derived": True,
            },
        }

    def render_owner_route(
        self, graph: ConditionGraph, node_id: str
    ) -> dict[str, Any]:
        """Render the owner responsibility route for the given node.

        Calls ReadinessRouter.get_owner_responsibility via runtime.
        Preserves owner_state="unknown" explicitly.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to trace owner responsibility for.

        Returns
        -------
        dict:
            Owner route data from runtime with explicit owner_state.
        """
        # Delegate to runtime — surface does not resolve owner routes
        owner_responsibility = self._service.get_owner_responsibility(graph, node_id)

        # Preserve owner_state="unknown" explicitly
        owner_state = "unknown"
        if isinstance(owner_responsibility, dict):
            owner_state = owner_responsibility.get("owner_state", "unknown")

        return {
            "trace_type": "owner_route",
            "node_id": node_id,
            "owner_responsibility": owner_responsibility,
            "owner_state": owner_state,
            "owner_state_explicit": True,
            "metadata": {
                "source": "runtime.readiness_routing.ReadinessRouter",
                "derived": True,
                "owner_state_preserved": True,
            },
        }

    def render_impact_path(
        self, graph: ConditionGraph, node_id: str
    ) -> dict[str, Any]:
        """Render the downstream impact path for the given node.

        Calls ImpactAnalyzer.get_downstream_impacts via runtime.
        Returns all downstream impacted nodes as computed by runtime.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to trace downstream impacts for.

        Returns
        -------
        dict:
            Impact path data from runtime.
        """
        # Delegate to runtime — surface does not compute impact sets
        downstream = self._service.get_downstream_impacts(graph, node_id)
        return {
            "trace_type": "impact_path",
            "node_id": node_id,
            "downstream_impacts": [_node_to_dict(n) for n in downstream],
            "impact_count": len(downstream),
            "metadata": {
                "source": "runtime.impact_analysis.ImpactAnalyzer",
                "derived": True,
            },
        }

    def render_dependency_chain(
        self, graph: ConditionGraph, node_id: str
    ) -> dict[str, Any]:
        """Render the dependency chain for the given node.

        Calls QueryEngine.get_dependencies via runtime.
        Returns the full upstream dependency chain.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to trace dependencies for.

        Returns
        -------
        dict:
            Dependency chain data from runtime.
        """
        # Delegate to runtime — surface does not compute dependency chains
        dependencies = self._service.get_dependencies(graph, node_id)
        upstream = self._service.get_upstream_dependencies(graph, node_id)
        return {
            "trace_type": "dependency_chain",
            "node_id": node_id,
            "immediate_dependencies": [_node_to_dict(n) for n in dependencies],
            "upstream_chain": [_node_to_dict(n) for n in upstream],
            "chain_length": len(upstream),
            "metadata": {
                "source": "runtime.graph_queries.QueryEngine",
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
