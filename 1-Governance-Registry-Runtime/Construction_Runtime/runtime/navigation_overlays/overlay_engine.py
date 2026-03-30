"""OverlayEngine — projects overlay annotations onto graph nodes.

Read-only. Composes QueryEngine, ReadinessRouter, and ImpactAnalyzer results.
No graph mutation. No traversal logic duplication.

Each overlay method returns a list of annotated node dicts or a structured
overlay result. Enrichment-derived data is explicitly flagged.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_index import GraphIndex
from runtime.graph_queries.query_engine import QueryEngine
from runtime.readiness_routing.router import ReadinessRouter
from runtime.impact_analysis.analyzer import ImpactAnalyzer


def _node_summary(node) -> dict:
    return {
        "node_id": node.graph_node_id,
        "node_type": node.node_type,
        "label": node.label,
        "state_summary": dict(node.state_summary),
        "is_enrichment_derived": node.metadata.get("is_enrichment_derived", False),
    }


def _readiness_state(rr: ReadinessRouter, node_id: str) -> str:
    try:
        chain = rr.get_readiness_chain(node_id)
        if chain.get("ready"):
            return "ready"
        if chain.get("blockers"):
            return "blocked"
        if not chain.get("dependencies_met"):
            return "pending"
        return "pending"
    except KeyError:
        return "unknown"


class OverlayEngine:
    """Projects overlay annotations onto condition graph nodes.

    Each overlay method annotates nodes with a specific dimension (readiness,
    blockers, ownership, etc.) and returns the annotated set.
    """

    def __init__(self) -> None:
        pass

    def _build_engines(self, graph: ConditionGraph):
        qe = QueryEngine(graph)
        rr = ReadinessRouter(graph)
        ia = ImpactAnalyzer(graph)
        index = GraphIndex(graph)
        return qe, rr, ia, index

    # ------------------------------------------------------------------
    # Overlays
    # ------------------------------------------------------------------

    def get_readiness_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate all nodes with their visual readiness state.

        Returns a list of node summary dicts, each with an added
        "readiness_state" key.
        """
        _, rr, _, _ = self._build_engines(graph)

        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            summary = _node_summary(node)
            summary["readiness_state"] = _readiness_state(rr, node_id)
            result.append(summary)

        return result

    def get_blocker_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate nodes with blocker information.

        Returns a list of node summary dicts, each with added keys:
        - "has_blockers": bool
        - "blocker_count": int
        - "immediate_blocker_ids": [str, ...]
        """
        qe, _, _, _ = self._build_engines(graph)

        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            blockers = qe.get_blockers(node_id)
            summary = _node_summary(node)
            summary["has_blockers"] = len(blockers) > 0
            summary["blocker_count"] = len(blockers)
            summary["immediate_blocker_ids"] = [b.graph_node_id for b in blockers]
            result.append(summary)

        return result

    def get_dependency_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate nodes with dependency information.

        Returns a list of node summary dicts, each with added keys:
        - "dependency_count": int
        - "dependency_ids": [str, ...]
        """
        qe, _, _, _ = self._build_engines(graph)

        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            deps = qe.get_dependencies(node_id)
            summary = _node_summary(node)
            summary["dependency_count"] = len(deps)
            summary["dependency_ids"] = [d.graph_node_id for d in deps]
            result.append(summary)

        return result

    def get_ownership_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate nodes with ownership information.

        Explicit unknown handling: owner_state is always present and is one of
        "assigned", "unassigned", or "unknown". Unknown is never smoothed away.

        Returns a list of node summary dicts, each with added keys:
        - "owner_state": str  ("assigned" | "unassigned" | "unknown")
        - "owner_node_id": str | None
        """
        _, rr, _, _ = self._build_engines(graph)

        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            try:
                responsibility = rr.get_owner_responsibility(node_id)
                owner_state = responsibility["owner_state"]
                owner_node = responsibility["owner_node"]
                owner_node_id = owner_node.graph_node_id if owner_node else None
            except KeyError:
                owner_state = "unknown"
                owner_node_id = None

            summary = _node_summary(node)
            summary["owner_state"] = owner_state
            summary["owner_node_id"] = owner_node_id
            result.append(summary)

        return result

    def get_remediation_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate nodes with remediation path information.

        Returns a list of node summary dicts, each with added keys:
        - "has_remediation": bool
        - "remediation_node_ids": [str, ...]
        """
        qe, _, _, _ = self._build_engines(graph)

        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            remediations = qe.get_remediation_path(node_id)
            summary = _node_summary(node)
            summary["has_remediation"] = len(remediations) > 0
            summary["remediation_node_ids"] = [r.graph_node_id for r in remediations]
            result.append(summary)

        return result

    def get_impact_overlay(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return the impact set for a given node.

        Returns::
            {
                "node_id": str,
                "downstream": [dict, ...],
                "upstream": [dict, ...],
                "impacted_artifacts": [dict, ...],
                "impacted_packages": [dict, ...],
            }
        """
        _, _, ia, _ = self._build_engines(graph)

        downstream = [_node_summary(n) for n in ia.get_downstream_impacts(node_id)]
        upstream = [_node_summary(n) for n in ia.get_upstream_dependencies(node_id)]
        artifacts = [_node_summary(n) for n in ia.get_artifact_impacts(node_id)]
        packages = [_node_summary(n) for n in ia.get_package_impacts(node_id)]

        return {
            "node_id": node_id,
            "downstream": downstream,
            "upstream": upstream,
            "impacted_artifacts": artifacts,
            "impacted_packages": packages,
        }

    def get_evidence_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate nodes with evidence linkage information.

        Returns a list of node summary dicts, each with added keys:
        - "has_evidence": bool
        - "evidence_count": int
        - "evidence_node_ids": [str, ...]
        """
        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            evidence_ids: list[str] = []
            for edge in graph.get_edges_from(node_id):
                if edge.edge_type == "supported_by":
                    ev_node = graph.get_node(edge.to_node_id)
                    if ev_node is not None and ev_node.node_type == "evidence":
                        evidence_ids.append(ev_node.graph_node_id)

            summary = _node_summary(node)
            summary["has_evidence"] = len(evidence_ids) > 0
            summary["evidence_count"] = len(evidence_ids)
            summary["evidence_node_ids"] = evidence_ids
            result.append(summary)

        return result

    def get_artifact_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate nodes with artifact linkage information.

        Returns a list of node summary dicts, each with added keys:
        - "has_artifacts": bool
        - "artifact_count": int
        """
        _, _, ia, _ = self._build_engines(graph)

        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            try:
                artifacts = ia.get_artifact_impacts(node_id)
            except KeyError:
                artifacts = []
            summary = _node_summary(node)
            summary["has_artifacts"] = len(artifacts) > 0
            summary["artifact_count"] = len(artifacts)
            result.append(summary)

        return result

    def get_pattern_overlay(self, graph: ConditionGraph) -> list[dict]:
        """Annotate nodes with pattern classification information.

        Pattern classifications are enrichment-derived and are explicitly marked
        with is_enrichment_derived=True.

        Returns a list of node summary dicts, each with added keys:
        - "has_pattern_classification": bool
        - "pattern_classifications": [{"edge_id": ..., "target_node_id": ..., "is_enrichment_derived": True}, ...]
        """
        qe, _, _, _ = self._build_engines(graph)

        result: list[dict] = []
        for node_id, node in graph.nodes.items():
            enrichment_edges = qe.get_enrichment_edges(node_id)
            classifications: list[dict] = []
            for edge in enrichment_edges:
                if edge.edge_type == "classified_as":
                    target_id = edge.to_node_id if edge.from_node_id == node_id else edge.from_node_id
                    classifications.append({
                        "edge_id": edge.graph_edge_id,
                        "target_node_id": target_id,
                        "is_enrichment_derived": True,
                        "source_basis": edge.source_basis,
                    })

            summary = _node_summary(node)
            summary["has_pattern_classification"] = len(classifications) > 0
            summary["pattern_classifications"] = classifications
            result.append(summary)

        return result
