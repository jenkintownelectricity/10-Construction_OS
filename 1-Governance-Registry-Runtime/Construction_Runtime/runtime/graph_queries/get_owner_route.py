"""Standalone function — owner route query."""

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph_queries.query_engine import QueryEngine


def get_owner_route(graph: ConditionGraph, node_id: str) -> dict:
    """Follow owned_by edges from *node_id* and return owner information.

    Standalone wrapper that constructs a QueryEngine internally.

    Returns {"owner_node": node_or_None, "owner_state": state}.
    Explicitly returns owner_state="unknown" when no owner is found.
    """
    engine = QueryEngine(graph)
    return engine.get_owner_route(node_id)
