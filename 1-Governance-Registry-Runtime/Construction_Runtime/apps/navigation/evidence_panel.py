"""
Evidence Panel Surface

Renders evidence information by delegating to runtime
NavigationQueryEngine.get_evidence_panel.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not evaluate evidence independently.
Incomplete source state is shown as incomplete, not hidden.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class EvidencePanelSurface:
    """Surface for rendering evidence panels.

    Delegates all evidence retrieval to runtime NavigationService.
    Shows incomplete evidence state as incomplete, not hidden.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, node_id: str) -> dict[str, Any]:
        """Render the evidence panel for the given node.

        Calls NavigationQueryEngine.get_evidence_panel via runtime.
        Returns evidence data as-is from runtime — no independent
        evidence evaluation.

        Incomplete source state is shown as incomplete, not hidden.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to inspect for evidence.

        Returns
        -------
        dict:
            Evidence panel data from runtime.
        """
        # Delegate to runtime — surface does not evaluate evidence
        neighborhood = self._service.get_condition_neighborhood(graph, node_id, depth=1)
        enrichment_edges = self._service.get_enrichment_edges(graph, node_id)

        return {
            "view_type": "detail",
            "panel": "evidence",
            "node_id": node_id,
            "neighborhood": neighborhood,
            "enrichment_edges": enrichment_edges,
            "metadata": {
                "source": "runtime.navigation.NavigationQueryEngine",
                "derived": True,
                "incomplete_state_visible": True,
            },
        }
