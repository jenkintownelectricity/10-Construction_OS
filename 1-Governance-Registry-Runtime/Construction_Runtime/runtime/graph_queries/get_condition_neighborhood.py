"""Standalone function — condition neighborhood query."""

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph_queries.query_engine import QueryEngine


def get_condition_neighborhood(
    graph: ConditionGraph, node_id: str, depth: int = 1
) -> dict:
    """Return the neighborhood of *node_id* within *depth* hops.

    Standalone wrapper that constructs a QueryEngine internally.

    Returns {"center": node, "neighbors": [nodes], "edges": [edges]}.
    """
    engine = QueryEngine(graph)
    return engine.get_condition_neighborhood(node_id, depth=depth)
