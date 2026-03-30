"""Standalone function — get_readiness_chain for a node in a ConditionGraph."""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.readiness_routing.router import ReadinessRouter


def get_readiness_chain(graph: ConditionGraph, node_id: str) -> dict:
    """Return a readiness assessment dict for *node_id*.

    Keys: ``node``, ``ready``, ``blockers``, ``dependencies_met``, ``next_actions``.
    Deterministic for identical graph input.
    """
    router = ReadinessRouter(graph)
    return router.get_readiness_chain(node_id)
