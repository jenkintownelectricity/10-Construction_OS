"""Standalone function — get_next_actions for a node in a ConditionGraph."""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.readiness_routing.router import ReadinessRouter


def get_next_actions(graph: ConditionGraph, node_id: str) -> list[dict]:
    """Return a list of actions that would unblock *node_id*.

    Each action is a dict with keys ``action``, ``target_node_id``, and ``reason``.
    Deterministic for identical graph input.
    """
    router = ReadinessRouter(graph)
    return router.get_next_actions(node_id)
