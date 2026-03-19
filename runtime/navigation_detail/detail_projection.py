"""DetailProjection — projects comprehensive detail for a single graph node.

Read-only. Composes QueryEngine, ReadinessRouter, and ImpactAnalyzer results.
No traversal logic duplication.
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
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


def _edge_summary(edge) -> dict:
    return {
        "edge_id": edge.graph_edge_id,
        "edge_type": edge.edge_type,
        "from_node_id": edge.from_node_id,
        "to_node_id": edge.to_node_id,
        "is_enrichment_derived": edge.is_enrichment_derived,
        "source_basis": edge.source_basis,
    }


class DetailProjection:
    """Projects comprehensive detail for a single node by composing all engines."""

    def __init__(self) -> None:
        pass

    def project_full_detail(self, graph: ConditionGraph, node_id: str) -> dict:
        """Project comprehensive detail for a single node.

        Includes: node summary, readiness state, blockers, dependencies,
        remediation path, owner info, evidence, artifacts, packages, revisions,
        upstream/downstream impacts, enrichment edges, and neighborhood.

        Returns a dict with "found": False if the node does not exist.
        """
        node = graph.get_node(node_id)
        if node is None:
            return {"node_id": node_id, "found": False}

        qe = QueryEngine(graph)
        rr = ReadinessRouter(graph)
        ia = ImpactAnalyzer(graph)

        # Readiness
        try:
            readiness = rr.get_readiness_chain(node_id)
            if readiness.get("ready"):
                readiness_state = "ready"
            elif readiness.get("blockers"):
                readiness_state = "blocked"
            elif not readiness.get("dependencies_met"):
                readiness_state = "pending"
            else:
                readiness_state = "pending"
            next_actions = readiness.get("next_actions", [])
        except KeyError:
            readiness_state = "unknown"
            next_actions = []

        # Query engine results
        blockers = [_node_summary(b) for b in qe.get_blockers(node_id)]
        dependencies = [_node_summary(d) for d in qe.get_dependencies(node_id)]
        remediation = [_node_summary(r) for r in qe.get_remediation_path(node_id)]
        enrichment_edges = [_edge_summary(e) for e in qe.get_enrichment_edges(node_id)]

        # Owner — explicit unknown handling
        owner_route = qe.get_owner_route(node_id)
        owner_info = {
            "owner_node": _node_summary(owner_route["owner_node"]) if owner_route["owner_node"] else None,
            "owner_state": owner_route["owner_state"],
        }

        # Readiness router results
        blocking_chain = [_node_summary(b) for b in rr.get_blocking_chain(node_id)]
        unblock_path = [_node_summary(n) for n in rr.get_unblock_path(node_id)]

        try:
            owner_responsibility = rr.get_owner_responsibility(node_id)
            responsibility_info = {
                "owner_node": _node_summary(owner_responsibility["owner_node"]) if owner_responsibility["owner_node"] else None,
                "owner_state": owner_responsibility["owner_state"],
                "owned_conditions": owner_responsibility["owned_conditions"],
            }
        except KeyError:
            responsibility_info = {
                "owner_node": None,
                "owner_state": "unknown",
                "owned_conditions": [],
            }

        # Impact analysis
        downstream = [_node_summary(n) for n in ia.get_downstream_impacts(node_id)]
        upstream = [_node_summary(n) for n in ia.get_upstream_dependencies(node_id)]
        artifacts = [_node_summary(a) for a in ia.get_artifact_impacts(node_id)]
        packages = [_node_summary(p) for p in ia.get_package_impacts(node_id)]
        revisions = [_node_summary(r) for r in ia.get_revision_impacts(node_id)]

        # Evidence via supported_by edges
        evidence: list[dict] = []
        for edge in graph.get_edges_from(node_id):
            if edge.edge_type == "supported_by":
                ev_node = graph.get_node(edge.to_node_id)
                if ev_node is not None:
                    ev_summary = _node_summary(ev_node)
                    ev_summary["edge_is_enrichment_derived"] = edge.is_enrichment_derived
                    evidence.append(ev_summary)

        # Neighborhood
        neighborhood = qe.get_condition_neighborhood(node_id, depth=1)
        neighbors = [_node_summary(n) for n in neighborhood.get("neighbors", [])]
        neighbor_edges = [_edge_summary(e) for e in neighborhood.get("edges", [])]

        # Outbound and inbound edges
        outbound_edges = [_edge_summary(e) for e in graph.get_edges_from(node_id)]
        inbound_edges = [_edge_summary(e) for e in graph.get_edges_to(node_id)]

        return {
            "node_id": node_id,
            "found": True,
            "node": _node_summary(node),
            "readiness_state": readiness_state,
            "next_actions": next_actions,
            "blockers": blockers,
            "blocking_chain": blocking_chain,
            "unblock_path": unblock_path,
            "dependencies": dependencies,
            "remediation_path": remediation,
            "owner": owner_info,
            "owner_responsibility": responsibility_info,
            "evidence": evidence,
            "artifacts": artifacts,
            "packages": packages,
            "revisions": revisions,
            "downstream_impacts": downstream,
            "upstream_dependencies": upstream,
            "enrichment_edges": enrichment_edges,
            "neighbors": neighbors,
            "neighbor_edges": neighbor_edges,
            "outbound_edges": outbound_edges,
            "inbound_edges": inbound_edges,
        }
