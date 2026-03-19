"""Standalone function — get_downstream_impacts for a node in a ConditionGraph."""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.impact_analysis.analyzer import ImpactAnalyzer


def get_downstream_impacts(
    graph: ConditionGraph, node_id: str, max_depth: int = -1
) -> list[ConditionGraphNode]:
    """Return all nodes downstream of *node_id* in *graph*.

    Deterministic for identical graph input.
    """
    analyzer = ImpactAnalyzer(graph)
    return analyzer.get_downstream_impacts(node_id, max_depth=max_depth)
