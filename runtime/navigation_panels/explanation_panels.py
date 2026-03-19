"""ExplanationPanelBuilder — builds structured explanation panels from graph queries.

Composes QueryEngine, ReadinessRouter, and ImpactAnalyzer results into
explanation-oriented data structures. Read-only, stateless, no graph mutation.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph_queries.query_engine import QueryEngine
from runtime.readiness_routing.router import ReadinessRouter
from runtime.impact_analysis.analyzer import ImpactAnalyzer


def _node_summary(node) -> dict:
    """Compact summary dict for a graph node."""
    return {
        "node_id": node.graph_node_id,
        "node_type": node.node_type,
        "label": node.label,
        "state_summary": dict(node.state_summary),
        "is_enrichment_derived": node.metadata.get("is_enrichment_derived", False),
    }


class ExplanationPanelBuilder:
    """Builds explanation panels by composing Wave 11A engine results.

    Each panel method returns a plain dict ready for presentation.
    All methods are read-only and take a ConditionGraph as input.
    """

    def __init__(self) -> None:
        pass

    def _build_engines(self, graph: ConditionGraph):
        qe = QueryEngine(graph)
        rr = ReadinessRouter(graph)
        ia = ImpactAnalyzer(graph)
        return qe, rr, ia

    # ------------------------------------------------------------------
    # Explanation panels
    # ------------------------------------------------------------------

    def build_why_blocked(self, graph: ConditionGraph, node_id: str) -> dict:
        """Explain why a node is blocked.

        Returns::
            {
                "node_id": str,
                "immediate_blockers": [dict, ...],
                "upstream_blockers": [dict, ...],
                "owner_route": {"owner_node": dict | None, "owner_state": str},
                "remediation_path": [dict, ...],
            }
        """
        qe, rr, _ = self._build_engines(graph)

        immediate = qe.get_blockers(node_id)
        chain = rr.get_blocking_chain(node_id)
        owner_route = qe.get_owner_route(node_id)
        remediation = qe.get_remediation_path(node_id)

        # Upstream blockers are chain members that are NOT immediate blockers
        immediate_ids = {b.graph_node_id for b in immediate}
        upstream = [n for n in chain if n.graph_node_id not in immediate_ids]

        return {
            "node_id": node_id,
            "immediate_blockers": [_node_summary(b) for b in immediate],
            "upstream_blockers": [_node_summary(b) for b in upstream],
            "owner_route": {
                "owner_node": _node_summary(owner_route["owner_node"]) if owner_route["owner_node"] else None,
                "owner_state": owner_route["owner_state"],
            },
            "remediation_path": [_node_summary(r) for r in remediation],
        }

    def build_what_depends(self, graph: ConditionGraph, node_id: str) -> dict:
        """Explain what depends on this node.

        Returns::
            {
                "node_id": str,
                "downstream_conditions": [dict, ...],
                "downstream_artifacts": [dict, ...],
                "package_implications": [dict, ...],
            }
        """
        _, _, ia = self._build_engines(graph)

        downstream = ia.get_downstream_impacts(node_id)
        downstream_conditions = [
            _node_summary(n) for n in downstream if n.node_type == "condition"
        ]
        downstream_artifacts = [
            _node_summary(n) for n in downstream if n.node_type == "artifact"
        ]

        packages = ia.get_package_impacts(node_id)

        return {
            "node_id": node_id,
            "downstream_conditions": downstream_conditions,
            "downstream_artifacts": downstream_artifacts,
            "package_implications": [_node_summary(p) for p in packages],
        }

    def build_what_changed(self, graph: ConditionGraph, node_id: str) -> dict:
        """Explain what changed relative to this node.

        Returns::
            {
                "node_id": str,
                "revision_changes": [dict, ...],
                "impacted_artifacts": [dict, ...],
                "changed_dependencies": [dict, ...],
            }
        """
        qe, _, ia = self._build_engines(graph)

        revisions = ia.get_revision_impacts(node_id)
        artifacts = ia.get_artifact_impacts(node_id)
        dependencies = qe.get_dependencies(node_id)

        return {
            "node_id": node_id,
            "revision_changes": [_node_summary(r) for r in revisions],
            "impacted_artifacts": [_node_summary(a) for a in artifacts],
            "changed_dependencies": [_node_summary(d) for d in dependencies],
        }

    def build_evidence_support(self, graph: ConditionGraph, node_id: str) -> dict:
        """Explain the evidence supporting this node's state.

        Returns::
            {
                "node_id": str,
                "evidence_refs": [dict, ...],
                "source_provenance": [dict, ...],
            }

        Evidence is linked via supported_by edges. Source provenance comes from
        enrichment edges and is explicitly marked.
        """
        qe, _, _ = self._build_engines(graph)

        # Evidence via supported_by edges
        evidence_nodes: list[dict] = []
        for edge in graph.get_edges_from(node_id):
            if edge.edge_type == "supported_by":
                ev_node = graph.get_node(edge.to_node_id)
                if ev_node is not None:
                    summary = _node_summary(ev_node)
                    summary["edge_is_enrichment_derived"] = edge.is_enrichment_derived
                    evidence_nodes.append(summary)

        # Enrichment edges as provenance
        enrichment_edges = qe.get_enrichment_edges(node_id)
        provenance: list[dict] = []
        for edge in enrichment_edges:
            linked_node = graph.get_node(edge.to_node_id)
            if linked_node is None:
                linked_node = graph.get_node(edge.from_node_id)
            provenance.append({
                "edge_id": edge.graph_edge_id,
                "edge_type": edge.edge_type,
                "is_enrichment_derived": edge.is_enrichment_derived,
                "linked_node": _node_summary(linked_node) if linked_node else None,
                "source_basis": edge.source_basis,
            })

        return {
            "node_id": node_id,
            "evidence_refs": evidence_nodes,
            "source_provenance": provenance,
        }
