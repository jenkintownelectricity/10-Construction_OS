"""Standalone function — get_revision_impacts for a node in a ConditionGraph."""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.impact_analysis.analyzer import ImpactAnalyzer


def get_revision_impacts(graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
    """Return all revision nodes in the subgraph reachable from *node_id*.

    Deterministic for identical graph input.
    """
    analyzer = ImpactAnalyzer(graph)
    return analyzer.get_revision_impacts(node_id)
