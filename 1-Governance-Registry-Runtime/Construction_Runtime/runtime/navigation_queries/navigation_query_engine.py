"""NavigationQueryEngine — high-level navigation queries that compose Wave 11A engines.

All methods are read-only and stateless. They consume QueryEngine, ReadinessRouter,
and ImpactAnalyzer — never duplicating their traversal logic. Results are
navigation-ready data structures (plain dicts/lists).
"""

from __future__ import annotations

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_index import GraphIndex
from runtime.graph_queries.query_engine import QueryEngine
from runtime.readiness_routing.router import ReadinessRouter
from runtime.impact_analysis.analyzer import ImpactAnalyzer


def _node_summary(node) -> dict:
    """Return a compact summary dict for a graph node."""
    return {
        "node_id": node.graph_node_id,
        "node_type": node.node_type,
        "label": node.label,
        "state_summary": dict(node.state_summary),
        "is_enrichment_derived": node.metadata.get("is_enrichment_derived", False),
    }


def _readiness_state_from_chain(readiness_chain: dict) -> str:
    """Derive a readiness state string from a ReadinessRouter.get_readiness_chain result."""
    if readiness_chain.get("ready"):
        return "ready"
    if readiness_chain.get("blockers"):
        return "blocked"
    if not readiness_chain.get("dependencies_met"):
        return "pending"
    return "pending"


class NavigationQueryEngine:
    """High-level navigation queries composed from Wave 11A engines.

    Stateless — engines are built per graph. All methods take a ConditionGraph
    as input and return plain data structures.
    """

    def __init__(self) -> None:
        pass

    def _build_engines(self, graph: ConditionGraph):
        """Build all three engines for a graph snapshot."""
        qe = QueryEngine(graph)
        rr = ReadinessRouter(graph)
        ia = ImpactAnalyzer(graph)
        index = GraphIndex(graph)
        return qe, rr, ia, index

    # ------------------------------------------------------------------
    # Map-level queries
    # ------------------------------------------------------------------

    def get_project_map(self, graph: ConditionGraph) -> dict:
        """Return a project-level map: systems grouped by readiness state.

        Returns::
            {
                "project_id": str,
                "systems": {
                    "<readiness_state>": [{"node_id": ..., "label": ..., ...}, ...]
                },
                "total_systems": int,
            }
        """
        _, rr, _, index = self._build_engines(graph)

        systems_by_state: dict[str, list[dict]] = {}
        system_node_ids = index.nodes_by_type.get("assembly", [])

        for nid in system_node_ids:
            node = graph.get_node(nid)
            if node is None:
                continue
            # Check if this is a top-level system (no parent assembly)
            # Use state_summary to determine if it's a system-level assembly
            try:
                chain = rr.get_readiness_chain(nid)
                state = _readiness_state_from_chain(chain)
            except KeyError:
                state = "unknown"

            summary = _node_summary(node)
            summary["readiness_state"] = state
            systems_by_state.setdefault(state, []).append(summary)

        return {
            "project_id": graph.project_id,
            "systems": systems_by_state,
            "total_systems": len(system_node_ids),
        }

    def get_system_map(self, graph: ConditionGraph, system_id: str) -> dict:
        """Return a system-level map: assemblies and their readiness states.

        Returns::
            {
                "system_id": str,
                "system_node": dict,
                "assemblies": [{"node_id": ..., "readiness_state": ..., ...}, ...],
            }
        """
        qe, rr, _, index = self._build_engines(graph)

        system_node = graph.get_node(system_id)
        if system_node is None:
            return {"system_id": system_id, "system_node": None, "assemblies": []}

        # Find assemblies linked to this system via edges
        assemblies: list[dict] = []
        for edge in graph.get_edges_from(system_id):
            child = graph.get_node(edge.to_node_id)
            if child is not None and child.node_type in ("assembly", "condition"):
                try:
                    chain = rr.get_readiness_chain(child.graph_node_id)
                    state = _readiness_state_from_chain(chain)
                except KeyError:
                    state = "unknown"
                summary = _node_summary(child)
                summary["readiness_state"] = state
                assemblies.append(summary)

        # Also find assemblies linked TO this system
        for edge in graph.get_edges_to(system_id):
            child = graph.get_node(edge.from_node_id)
            if child is not None and child.node_type in ("assembly", "condition"):
                if any(a["node_id"] == child.graph_node_id for a in assemblies):
                    continue
                try:
                    chain = rr.get_readiness_chain(child.graph_node_id)
                    state = _readiness_state_from_chain(chain)
                except KeyError:
                    state = "unknown"
                summary = _node_summary(child)
                summary["readiness_state"] = state
                assemblies.append(summary)

        return {
            "system_id": system_id,
            "system_node": _node_summary(system_node),
            "assemblies": assemblies,
        }

    def get_assembly_map(self, graph: ConditionGraph, assembly_id: str) -> dict:
        """Return an assembly-level map: conditions, blockers, deps, artifacts.

        Returns::
            {
                "assembly_id": str,
                "assembly_node": dict,
                "conditions": [dict, ...],
                "blockers": [dict, ...],
                "dependencies": [dict, ...],
                "artifacts": [dict, ...],
            }
        """
        qe, rr, ia, index = self._build_engines(graph)

        assembly_node = graph.get_node(assembly_id)
        if assembly_node is None:
            return {
                "assembly_id": assembly_id,
                "assembly_node": None,
                "conditions": [],
                "blockers": [],
                "dependencies": [],
                "artifacts": [],
            }

        # Collect conditions linked from this assembly
        conditions: list[dict] = []
        for edge in graph.get_edges_from(assembly_id):
            child = graph.get_node(edge.to_node_id)
            if child is not None and child.node_type == "condition":
                conditions.append(_node_summary(child))

        # Also conditions linked TO this assembly
        for edge in graph.get_edges_to(assembly_id):
            child = graph.get_node(edge.from_node_id)
            if child is not None and child.node_type == "condition":
                if not any(c["node_id"] == child.graph_node_id for c in conditions):
                    conditions.append(_node_summary(child))

        # Blockers and dependencies via QueryEngine
        blockers = [_node_summary(b) for b in qe.get_blockers(assembly_id)]
        dependencies = [_node_summary(d) for d in qe.get_dependencies(assembly_id)]

        # Artifacts via ImpactAnalyzer
        artifacts = [_node_summary(a) for a in ia.get_artifact_impacts(assembly_id)]

        return {
            "assembly_id": assembly_id,
            "assembly_node": _node_summary(assembly_node),
            "conditions": conditions,
            "blockers": blockers,
            "dependencies": dependencies,
            "artifacts": artifacts,
        }

    # ------------------------------------------------------------------
    # Detail-level queries
    # ------------------------------------------------------------------

    def get_condition_detail(self, graph: ConditionGraph, condition_node_id: str) -> dict:
        """Return full condition detail including neighborhood, readiness, and impacts.

        Returns a comprehensive dict with all available information about a condition node.
        """
        qe, rr, ia, index = self._build_engines(graph)

        node = graph.get_node(condition_node_id)
        if node is None:
            return {"node_id": condition_node_id, "found": False}

        neighborhood = qe.get_condition_neighborhood(condition_node_id, depth=1)
        blockers = [_node_summary(b) for b in qe.get_blockers(condition_node_id)]
        dependencies = [_node_summary(d) for d in qe.get_dependencies(condition_node_id)]
        remediation = [_node_summary(r) for r in qe.get_remediation_path(condition_node_id)]
        owner_route = qe.get_owner_route(condition_node_id)
        enrichment_edges = qe.get_enrichment_edges(condition_node_id)

        try:
            readiness = rr.get_readiness_chain(condition_node_id)
            readiness_state = _readiness_state_from_chain(readiness)
            next_actions = readiness.get("next_actions", [])
        except KeyError:
            readiness_state = "unknown"
            next_actions = []

        downstream = [_node_summary(n) for n in ia.get_downstream_impacts(condition_node_id)]
        upstream = [_node_summary(n) for n in ia.get_upstream_dependencies(condition_node_id)]

        owner_info = {
            "owner_node": _node_summary(owner_route["owner_node"]) if owner_route["owner_node"] else None,
            "owner_state": owner_route["owner_state"],
        }

        return {
            "node_id": condition_node_id,
            "found": True,
            "node": _node_summary(node),
            "readiness_state": readiness_state,
            "blockers": blockers,
            "dependencies": dependencies,
            "remediation_path": remediation,
            "owner": owner_info,
            "next_actions": next_actions,
            "downstream_impacts": downstream,
            "upstream_dependencies": upstream,
            "neighbors": [_node_summary(n) for n in neighborhood.get("neighbors", [])],
            "enrichment_edges": [
                {
                    "edge_id": e.graph_edge_id,
                    "edge_type": e.edge_type,
                    "from_node_id": e.from_node_id,
                    "to_node_id": e.to_node_id,
                    "is_enrichment_derived": e.is_enrichment_derived,
                }
                for e in enrichment_edges
            ],
        }

    # ------------------------------------------------------------------
    # Panel queries
    # ------------------------------------------------------------------

    def get_blocker_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return blocker chain and immediate blockers for a node.

        Returns::
            {
                "node_id": str,
                "immediate_blockers": [dict, ...],
                "blocking_chain": [dict, ...],
            }
        """
        qe, rr, _, _ = self._build_engines(graph)
        immediate = [_node_summary(b) for b in qe.get_blockers(node_id)]
        chain = [_node_summary(b) for b in rr.get_blocking_chain(node_id)]
        return {
            "node_id": node_id,
            "immediate_blockers": immediate,
            "blocking_chain": chain,
        }

    def get_dependency_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return dependency list for a node."""
        qe, _, _, _ = self._build_engines(graph)
        deps = [_node_summary(d) for d in qe.get_dependencies(node_id)]
        return {"node_id": node_id, "dependencies": deps}

    def get_owner_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return owner info with explicit unknown handling.

        owner_state is always present and is one of: "assigned", "unassigned", "unknown".
        """
        _, rr, _, _ = self._build_engines(graph)
        responsibility = rr.get_owner_responsibility(node_id)
        owner_node = responsibility["owner_node"]
        return {
            "node_id": node_id,
            "owner_node": _node_summary(owner_node) if owner_node else None,
            "owner_state": responsibility["owner_state"],
            "owned_conditions": responsibility["owned_conditions"],
        }

    def get_remediation_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return remediation path for a node."""
        qe, _, _, _ = self._build_engines(graph)
        path = [_node_summary(r) for r in qe.get_remediation_path(node_id)]
        return {"node_id": node_id, "remediation_path": path}

    def get_evidence_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return linked evidence for a node.

        Evidence is linked via supported_by edges.
        """
        evidence_nodes: list[dict] = []
        for edge in graph.get_edges_from(node_id):
            if edge.edge_type == "supported_by":
                ev_node = graph.get_node(edge.to_node_id)
                if ev_node is not None and ev_node.node_type == "evidence":
                    summary = _node_summary(ev_node)
                    summary["is_enrichment_derived"] = edge.is_enrichment_derived
                    evidence_nodes.append(summary)
        return {"node_id": node_id, "evidence": evidence_nodes}

    def get_artifact_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return linked artifacts for a node."""
        _, _, ia, _ = self._build_engines(graph)
        artifacts = [_node_summary(a) for a in ia.get_artifact_impacts(node_id)]
        return {"node_id": node_id, "artifacts": artifacts}

    def get_package_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return linked packages for a node."""
        _, _, ia, _ = self._build_engines(graph)
        packages = [_node_summary(p) for p in ia.get_package_impacts(node_id)]
        return {"node_id": node_id, "packages": packages}

    def get_revision_panel(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return linked revisions for a node."""
        _, _, ia, _ = self._build_engines(graph)
        revisions = [_node_summary(r) for r in ia.get_revision_impacts(node_id)]
        return {"node_id": node_id, "revisions": revisions}

    # ------------------------------------------------------------------
    # Overlay queries
    # ------------------------------------------------------------------

    def get_readiness_overlay(self, graph: ConditionGraph) -> dict:
        """Return all nodes annotated with readiness states.

        Returns::
            {
                "nodes": [{"node_id": ..., "readiness_state": ..., ...}, ...]
            }
        """
        _, rr, _, _ = self._build_engines(graph)

        annotated: list[dict] = []
        for node_id, node in graph.nodes.items():
            try:
                chain = rr.get_readiness_chain(node_id)
                state = _readiness_state_from_chain(chain)
            except KeyError:
                state = "unknown"
            summary = _node_summary(node)
            summary["readiness_state"] = state
            annotated.append(summary)

        return {"nodes": annotated}

    def get_impact_overlay(self, graph: ConditionGraph, node_id: str) -> dict:
        """Return upstream and downstream impacts for a node.

        Returns::
            {
                "node_id": str,
                "upstream": [dict, ...],
                "downstream": [dict, ...],
            }
        """
        _, _, ia, _ = self._build_engines(graph)
        upstream = [_node_summary(n) for n in ia.get_upstream_dependencies(node_id)]
        downstream = [_node_summary(n) for n in ia.get_downstream_impacts(node_id)]
        return {
            "node_id": node_id,
            "upstream": upstream,
            "downstream": downstream,
        }
