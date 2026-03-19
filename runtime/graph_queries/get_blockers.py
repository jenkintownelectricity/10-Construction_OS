"""Standalone function — blockers query."""

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph_queries.query_engine import QueryEngine


def get_blockers(graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
    """Follow blocked_by edges from *node_id* and return the blocker nodes.

    Standalone wrapper that constructs a QueryEngine internally.
    """
    engine = QueryEngine(graph)
    return engine.get_blockers(node_id)
