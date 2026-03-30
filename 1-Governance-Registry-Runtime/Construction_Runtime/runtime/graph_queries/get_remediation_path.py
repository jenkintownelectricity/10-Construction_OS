"""Standalone function — remediation path query."""

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph_queries.query_engine import QueryEngine


def get_remediation_path(
    graph: ConditionGraph, node_id: str
) -> list[ConditionGraphNode]:
    """Follow resolved_by edges from *node_id* and return remediation nodes.

    Standalone wrapper that constructs a QueryEngine internally.
    """
    engine = QueryEngine(graph)
    return engine.get_remediation_path(node_id)
