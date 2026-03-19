"""Standalone function — dependencies query."""

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph_queries.query_engine import QueryEngine


def get_dependencies(
    graph: ConditionGraph, node_id: str
) -> list[ConditionGraphNode]:
    """Follow depends_on edges from *node_id* and return dependency nodes.

    Standalone wrapper that constructs a QueryEngine internally.
    """
    engine = QueryEngine(graph)
    return engine.get_dependencies(node_id)
