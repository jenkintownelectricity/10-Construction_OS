"""Standalone function — get_unblock_path for a node in a ConditionGraph."""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.readiness_routing.router import ReadinessRouter


def get_unblock_path(graph: ConditionGraph, node_id: str) -> list[ConditionGraphNode]:
    """Return an ordered list of nodes that must be resolved to unblock *node_id*.

    The list is topologically sorted so that resolving nodes in order progressively
    unblocks the target.  Deterministic for identical graph input.
    """
    router = ReadinessRouter(graph)
    return router.get_unblock_path(node_id)
