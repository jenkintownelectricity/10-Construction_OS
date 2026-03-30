"""Wave 11A graph query engine — read-only queries over a ConditionGraph.

The query engine consumes a ConditionGraph without modifying it.
All queries are deterministic for identical graph state.
"""

from collections import deque
from typing import Optional

from runtime.graph.condition_graph import ConditionGraph
from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.graph_edge import ConditionGraphEdge
from runtime.graph.graph_index import GraphIndex


class QueryEngine:
    """Read-only query engine over a materialized ConditionGraph.

    Builds a GraphIndex internally for fast lookups. Never mutates the
    underlying graph.
    """

    def __init__(self, graph: ConditionGraph) -> None:
        self._graph = graph
        self._index = GraphIndex(graph)

    def get_condition_neighborhood(
        self, condition_node_id: str, depth: int = 1
    ) -> dict:
        """Return the neighborhood of a node within *depth* hops.

        Returns {"center": node, "neighbors": [nodes], "edges": [edges]}.
        """
        center = self._graph.get_node(condition_node_id)
        if center is None:
            return {"center": None, "neighbors": [], "edges": []}

        visited_nodes: dict[str, ConditionGraphNode] = {condition_node_id: center}
        collected_edges: dict[str, ConditionGraphEdge] = {}
        frontier: deque[tuple[str, int]] = deque([(condition_node_id, 0)])

        while frontier:
            current_id, current_depth = frontier.popleft()
            if current_depth >= depth:
                continue

            # Outbound edges
            for edge_id in self._index.adjacency_out.get(current_id, []):
                edge = self._graph.get_edge(edge_id)
                if edge is None:
                    continue
                collected_edges[edge_id] = edge
                neighbor_id = edge.to_node_id
                if neighbor_id not in visited_nodes:
                    neighbor = self._graph.get_node(neighbor_id)
                    if neighbor is not None:
                        visited_nodes[neighbor_id] = neighbor
                        frontier.append((neighbor_id, current_depth + 1))

            # Inbound edges
            for edge_id in self._index.adjacency_in.get(current_id, []):
                edge = self._graph.get_edge(edge_id)
                if edge is None:
                    continue
                collected_edges[edge_id] = edge
                neighbor_id = edge.from_node_id
                if neighbor_id not in visited_nodes:
                    neighbor = self._graph.get_node(neighbor_id)
                    if neighbor is not None:
                        visited_nodes[neighbor_id] = neighbor
                        frontier.append((neighbor_id, current_depth + 1))

        neighbors = [
            n for nid, n in visited_nodes.items() if nid != condition_node_id
        ]

        return {
            "center": center,
            "neighbors": neighbors,
            "edges": list(collected_edges.values()),
        }

    def get_blockers(self, node_id: str) -> list[ConditionGraphNode]:
        """Follow blocked_by edges from *node_id* and return the blocker nodes."""
        blockers: list[ConditionGraphNode] = []
        for edge_id in self._index.adjacency_out.get(node_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.edge_type == "blocked_by":
                blocker = self._graph.get_node(edge.to_node_id)
                if blocker is not None:
                    blockers.append(blocker)
        return blockers

    def get_dependencies(self, node_id: str) -> list[ConditionGraphNode]:
        """Follow depends_on edges from *node_id* and return dependency nodes."""
        deps: list[ConditionGraphNode] = []
        for edge_id in self._index.adjacency_out.get(node_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.edge_type == "depends_on":
                dep = self._graph.get_node(edge.to_node_id)
                if dep is not None:
                    deps.append(dep)
        return deps

    def get_remediation_path(self, node_id: str) -> list[ConditionGraphNode]:
        """Follow resolved_by edges from *node_id* and return remediation nodes."""
        remediations: list[ConditionGraphNode] = []
        for edge_id in self._index.adjacency_out.get(node_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.edge_type == "resolved_by":
                rem = self._graph.get_node(edge.to_node_id)
                if rem is not None:
                    remediations.append(rem)
        return remediations

    def get_owner_route(self, node_id: str) -> dict:
        """Follow owned_by edges from *node_id* and return owner information.

        Returns {"owner_node": node_or_None, "owner_state": state}.
        Explicitly preserves "unknown" when no owner is found.
        """
        for edge_id in self._index.adjacency_out.get(node_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.edge_type == "owned_by":
                owner = self._graph.get_node(edge.to_node_id)
                if owner is not None:
                    owner_state = owner.state_summary.get("owner_state", "unknown")
                    return {"owner_node": owner, "owner_state": owner_state}
        return {"owner_node": None, "owner_state": "unknown"}

    def get_node_by_source(
        self, source_object_type: str, source_object_id: str
    ) -> Optional[ConditionGraphNode]:
        """Look up a node by its source triple via the index."""
        source_key = f"{source_object_type}:{source_object_id}"
        node_id = self._index.source_to_node.get(source_key)
        if node_id is None:
            return None
        return self._graph.get_node(node_id)

    def get_edges_between(
        self, node_a_id: str, node_b_id: str
    ) -> list[ConditionGraphEdge]:
        """Return all edges connecting two nodes in either direction."""
        result: list[ConditionGraphEdge] = []
        for edge_id in self._index.adjacency_out.get(node_a_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.to_node_id == node_b_id:
                result.append(edge)
        for edge_id in self._index.adjacency_out.get(node_b_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.to_node_id == node_a_id:
                result.append(edge)
        return result

    def get_enrichment_edges(self, node_id: str) -> list[ConditionGraphEdge]:
        """Return edges where is_enrichment_derived=True connected to this node."""
        enrichment: list[ConditionGraphEdge] = []
        for edge_id in self._index.adjacency_out.get(node_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.is_enrichment_derived:
                enrichment.append(edge)
        for edge_id in self._index.adjacency_in.get(node_id, []):
            edge = self._graph.get_edge(edge_id)
            if edge is not None and edge.is_enrichment_derived:
                enrichment.append(edge)
        return enrichment
