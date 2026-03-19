"""
Remediation Panel Surface

Renders remediation information by delegating to runtime
NavigationQueryEngine.get_remediation_panel.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not compute remediation paths independently.

Must distinguish runtime-backed remediation data from
enrichment-derived remediation data explicitly.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


class RemediationPanelSurface:
    """Surface for rendering remediation panels.

    Delegates all remediation computation to runtime NavigationService.
    Distinguishes runtime-backed vs enrichment-derived data explicitly.
    """

    def __init__(self) -> None:
        self._service = NavigationService()

    def render(self, graph: ConditionGraph, node_id: str) -> dict[str, Any]:
        """Render the remediation panel for the given node.

        Calls NavigationQueryEngine.get_remediation_panel via runtime.
        Returns remediation data with explicit labeling of whether each
        remediation step is runtime-backed or enrichment-derived.

        Parameters
        ----------
        graph:
            The condition graph snapshot.
        node_id:
            Identifier of the node to inspect for remediation paths.

        Returns
        -------
        dict:
            Remediation panel data with enrichment distinction labels.
        """
        # Delegate to runtime — surface does not compute remediation paths
        remediation_path = self._service.get_remediation_path(graph, node_id)
        enrichment_edges = self._service.get_enrichment_edges(graph, node_id)
        next_actions = self._service.get_next_actions(graph, node_id)

        # Build enrichment node ID set for labeling
        enrichment_node_ids: set[str] = set()
        for edge in enrichment_edges:
            if isinstance(edge, dict):
                for key in ("target_id", "source_id", "target", "source"):
                    if key in edge:
                        enrichment_node_ids.add(str(edge[key]))
            elif hasattr(edge, "target_id"):
                enrichment_node_ids.add(str(edge.target_id))

        # Label each remediation step with its data source
        labeled_steps = []
        for step in remediation_path:
            step_dict = _node_to_dict(step)
            step_id = step_dict.get("id", "")
            step_dict["enrichment_derived"] = step_id in enrichment_node_ids
            step_dict["data_source"] = (
                "enrichment" if step_id in enrichment_node_ids else "runtime"
            )
            labeled_steps.append(step_dict)

        return {
            "view_type": "detail",
            "panel": "remediation",
            "node_id": node_id,
            "remediation_path": labeled_steps,
            "next_actions": next_actions,
            "enrichment_distinction": True,
            "metadata": {
                "source": "runtime.navigation.NavigationQueryEngine",
                "derived": True,
                "enrichment_labeled": True,
            },
        }


def _node_to_dict(node: Any) -> dict[str, Any]:
    """Convert a graph node to a serializable dict."""
    if isinstance(node, dict):
        return node
    result: dict[str, Any] = {}
    for attr in ("id", "node_type", "readiness_state", "owner_state"):
        if hasattr(node, attr):
            result[attr] = getattr(node, attr)
    return result
