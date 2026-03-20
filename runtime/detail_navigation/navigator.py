"""
Detail Navigator — Wave 15.

Provides cross-detail traversal operations using the detail graph.
All outputs are deterministic and explainable from source truth.
"""

from typing import Any

from runtime.detail_graph.graph_builder import DetailGraph
from runtime.detail_navigation.contract import (
    UPSTREAM_RELATIONSHIP_TYPES,
    DOWNSTREAM_RELATIONSHIP_TYPES,
    TRANSITION_RELATIONSHIP_TYPES,
    ADJACENCY_RELATIONSHIP_TYPES,
)


class DetailNavigator:
    """Stateless navigation engine over a DetailGraph."""

    def __init__(self, graph: DetailGraph):
        self._graph = graph

    def find_related_details(self, detail_id: str) -> list[dict[str, Any]]:
        """Find all details related to the given detail, with relationship metadata."""
        if detail_id not in self._graph.nodes:
            return []

        related: list[dict[str, Any]] = []
        seen = set()
        for edge in self._graph.edges:
            if edge["source_detail_id"] == detail_id:
                target = edge["target_detail_id"]
                if target not in seen:
                    seen.add(target)
                    related.append({
                        "detail_id": target,
                        "relationship_type": edge["relationship_type"],
                        "directionality": edge.get("directionality", "directional"),
                        "criticality": edge.get("criticality", "required"),
                        "direction": "outbound",
                        "node": self._graph.nodes.get(target),
                    })
            elif edge["target_detail_id"] == detail_id:
                source = edge["source_detail_id"]
                if source not in seen:
                    seen.add(source)
                    related.append({
                        "detail_id": source,
                        "relationship_type": edge["relationship_type"],
                        "directionality": edge.get("directionality", "directional"),
                        "criticality": edge.get("criticality", "required"),
                        "direction": "inbound",
                        "node": self._graph.nodes.get(source),
                    })

        return sorted(related, key=lambda r: r["detail_id"])

    def resolve_neighbors(self, detail_id: str) -> list[dict[str, Any]]:
        """Resolve immediate neighbors of a detail."""
        if detail_id not in self._graph.nodes:
            return []

        neighbor_ids = self._graph.neighbor_lookup(detail_id)
        result = []
        for nid in neighbor_ids:
            edges = [
                e for e in self._graph.edges
                if (e["source_detail_id"] == detail_id and e["target_detail_id"] == nid)
                or (e["source_detail_id"] == nid and e["target_detail_id"] == detail_id)
            ]
            result.append({
                "detail_id": nid,
                "node": self._graph.nodes.get(nid),
                "edges": edges,
            })
        return result

    def resolve_upstream_dependencies(self, detail_id: str) -> list[dict[str, Any]]:
        """Resolve upstream dependencies for a detail (things this detail depends on)."""
        if detail_id not in self._graph.nodes:
            return []

        upstream = []
        for edge in self._graph.edges:
            if (edge["source_detail_id"] == detail_id
                    and edge["relationship_type"] in UPSTREAM_RELATIONSHIP_TYPES):
                upstream.append({
                    "detail_id": edge["target_detail_id"],
                    "relationship_type": edge["relationship_type"],
                    "criticality": edge.get("criticality", "required"),
                    "node": self._graph.nodes.get(edge["target_detail_id"]),
                })
            elif (edge["target_detail_id"] == detail_id
                    and edge["relationship_type"] in ("blocks",)):
                upstream.append({
                    "detail_id": edge["source_detail_id"],
                    "relationship_type": edge["relationship_type"],
                    "criticality": edge.get("criticality", "required"),
                    "node": self._graph.nodes.get(edge["source_detail_id"]),
                })
        return sorted(upstream, key=lambda u: u["detail_id"])

    def resolve_downstream_paths(self, detail_id: str) -> list[dict[str, Any]]:
        """Resolve downstream details (things that depend on this detail)."""
        if detail_id not in self._graph.nodes:
            return []

        downstream = []
        for edge in self._graph.edges:
            if (edge["target_detail_id"] == detail_id
                    and edge["relationship_type"] in UPSTREAM_RELATIONSHIP_TYPES):
                downstream.append({
                    "detail_id": edge["source_detail_id"],
                    "relationship_type": edge["relationship_type"],
                    "criticality": edge.get("criticality", "required"),
                    "node": self._graph.nodes.get(edge["source_detail_id"]),
                })
            elif (edge["source_detail_id"] == detail_id
                    and edge["relationship_type"] in DOWNSTREAM_RELATIONSHIP_TYPES):
                downstream.append({
                    "detail_id": edge["target_detail_id"],
                    "relationship_type": edge["relationship_type"],
                    "criticality": edge.get("criticality", "required"),
                    "node": self._graph.nodes.get(edge["target_detail_id"]),
                })
        return sorted(downstream, key=lambda d: d["detail_id"])

    def resolve_installation_transitions(self, detail_id: str) -> list[dict[str, Any]]:
        """Resolve installation transition details (terminates_into, precedes, follows)."""
        if detail_id not in self._graph.nodes:
            return []

        transitions = []
        for edge in self._graph.edges:
            if (edge["source_detail_id"] == detail_id
                    and edge["relationship_type"] in TRANSITION_RELATIONSHIP_TYPES):
                transitions.append({
                    "detail_id": edge["target_detail_id"],
                    "relationship_type": edge["relationship_type"],
                    "direction": "outbound",
                    "criticality": edge.get("criticality", "required"),
                    "node": self._graph.nodes.get(edge["target_detail_id"]),
                })
            elif (edge["target_detail_id"] == detail_id
                    and edge["relationship_type"] in TRANSITION_RELATIONSHIP_TYPES):
                transitions.append({
                    "detail_id": edge["source_detail_id"],
                    "relationship_type": edge["relationship_type"],
                    "direction": "inbound",
                    "criticality": edge.get("criticality", "required"),
                    "node": self._graph.nodes.get(edge["source_detail_id"]),
                })
        return sorted(transitions, key=lambda t: t["detail_id"])

    def resolve_navigation_path(
        self, detail_a: str, detail_b: str
    ) -> dict[str, Any]:
        """
        Resolve the navigation path between two details.

        Returns a dict with path steps and relationship chain.
        """
        if detail_a not in self._graph.nodes or detail_b not in self._graph.nodes:
            return {
                "source": detail_a,
                "target": detail_b,
                "path_exists": False,
                "steps": [],
                "relationship_chain": [],
            }

        path = self._graph.shortest_path(detail_a, detail_b)
        if path is None:
            return {
                "source": detail_a,
                "target": detail_b,
                "path_exists": False,
                "steps": [],
                "relationship_chain": [],
            }

        steps = []
        relationship_chain = []
        for i in range(len(path)):
            step_node = self._graph.nodes.get(path[i])
            steps.append({
                "step": i,
                "detail_id": path[i],
                "node": step_node,
            })
            if i > 0:
                edges_between = _find_edges_between(
                    self._graph.edges, path[i - 1], path[i]
                )
                for edge in edges_between:
                    relationship_chain.append({
                        "from": path[i - 1],
                        "to": path[i],
                        "relationship_type": edge["relationship_type"],
                        "criticality": edge.get("criticality", "required"),
                    })

        return {
            "source": detail_a,
            "target": detail_b,
            "path_exists": True,
            "path_length": len(path) - 1,
            "steps": steps,
            "relationship_chain": relationship_chain,
        }


def _find_edges_between(
    edges: list[dict[str, Any]], id_a: str, id_b: str
) -> list[dict[str, Any]]:
    """Find all edges between two detail IDs in either direction."""
    result = []
    for e in edges:
        if ((e["source_detail_id"] == id_a and e["target_detail_id"] == id_b)
                or (e["source_detail_id"] == id_b and e["target_detail_id"] == id_a)):
            result.append(e)
    return result
