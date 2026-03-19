"""Standalone function — get_upstream_dependencies for a node in a ConditionGraph."""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.impact_analysis.analyzer import ImpactAnalyzer


def get_upstream_dependencies(
    graph: ConditionGraph, node_id: str, max_depth: int = -1
) -> list[ConditionGraphNode]:
    """Return all nodes upstream of *node_id* in *graph*.

    Deterministic for identical graph input.
    """
    analyzer = ImpactAnalyzer(graph)
    return analyzer.get_upstream_dependencies(node_id, max_depth=max_depth)
