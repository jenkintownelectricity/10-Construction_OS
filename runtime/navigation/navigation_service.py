"""Main NavigationService — composes QueryEngine, ReadinessRouter, and ImpactAnalyzer.

This is a stateless facade. Each call receives a ConditionGraph and delegates
to the underlying Wave 11A engines. No graph mutation. No duplication of
traversal logic.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph_queries.query_engine import QueryEngine
from runtime.readiness_routing.router import ReadinessRouter
from runtime.impact_analysis.analyzer import ImpactAnalyzer


class NavigationService:
    """Facade that composes all Wave 11A engines for navigation-ready output.

    Every public method is read-only and stateless — the graph is passed in
    and internal engines are instantiated per call (or can be cached externally).
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        """NavigationService is stateless; engines are built per-graph."""

    def _engines(self, graph: ConditionGraph) -> tuple[QueryEngine, ReadinessRouter, ImpactAnalyzer]:
        """Instantiate all three engines for a given graph snapshot."""
        return (
            QueryEngine(graph),
            ReadinessRouter(graph),
            ImpactAnalyzer(graph),
        )

    # ------------------------------------------------------------------
    # Neighborhood / structure queries
    # ------------------------------------------------------------------

    def get_condition_neighborhood(
        self, graph: ConditionGraph, condition_node_id: str, depth: int = 1
    ) -> dict:
        """Return the neighborhood of a condition node."""
        qe, _, _ = self._engines(graph)
        return qe.get_condition_neighborhood(condition_node_id, depth)

    def get_blockers(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return immediate blocker nodes."""
        qe, _, _ = self._engines(graph)
        return qe.get_blockers(node_id)

    def get_dependencies(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return immediate dependency nodes."""
        qe, _, _ = self._engines(graph)
        return qe.get_dependencies(node_id)

    def get_remediation_path(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return remediation nodes linked to *node_id*."""
        qe, _, _ = self._engines(graph)
        return qe.get_remediation_path(node_id)

    def get_owner_route(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return owner information with explicit unknown handling."""
        qe, _, _ = self._engines(graph)
        return qe.get_owner_route(node_id)

    def get_enrichment_edges(self, graph: ConditionGraph, node_id: str) -> list:
        """Return enrichment-derived edges for a node."""
        qe, _, _ = self._engines(graph)
        return qe.get_enrichment_edges(node_id)

    # ------------------------------------------------------------------
    # Readiness routing queries
    # ------------------------------------------------------------------

    def get_blocking_chain(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return the full recursive blocking chain."""
        _, rr, _ = self._engines(graph)
        return rr.get_blocking_chain(node_id)

    def get_next_actions(self, graph: ConditionGraph, node_id: str) -> list[dict]:
        """Return suggested next actions to unblock a node."""
        _, rr, _ = self._engines(graph)
        return rr.get_next_actions(node_id)

    def get_unblock_path(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return topologically sorted unblock path."""
        _, rr, _ = self._engines(graph)
        return rr.get_unblock_path(node_id)

    def get_readiness_chain(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return full readiness assessment for a node."""
        _, rr, _ = self._engines(graph)
        return rr.get_readiness_chain(node_id)

    def get_owner_responsibility(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return owner responsibility info with explicit unknown state."""
        _, rr, _ = self._engines(graph)
        return rr.get_owner_responsibility(node_id)

    # ------------------------------------------------------------------
    # Impact analysis queries
    # ------------------------------------------------------------------

    def get_downstream_impacts(
        self, graph: ConditionGraph, node_id: str, max_depth: int = -1
    ) -> list[ConditionGraphNode]:
        """Return all downstream impacted nodes."""
        _, _, ia = self._engines(graph)
        return ia.get_downstream_impacts(node_id, max_depth)

    def get_upstream_dependencies(
        self, graph: ConditionGraph, node_id: str, max_depth: int = -1
    ) -> list[ConditionGraphNode]:
        """Return all upstream dependency nodes."""
        _, _, ia = self._engines(graph)
        return ia.get_upstream_dependencies(node_id, max_depth)

    def get_artifact_impacts(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return artifact nodes impacted by changes at *node_id*."""
        _, _, ia = self._engines(graph)
        return ia.get_artifact_impacts(node_id)

    def get_package_impacts(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return package nodes impacted by changes at *node_id*."""
        _, _, ia = self._engines(graph)
        return ia.get_package_impacts(node_id)

    def get_revision_impacts(self, graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
        """Return revision nodes impacted by changes at *node_id*."""
        _, _, ia = self._engines(graph)
        return ia.get_revision_impacts(node_id)
