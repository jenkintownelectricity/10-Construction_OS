"""Wave 11A condition graph container — materialized graph with query accessors."""

from dataclasses import dataclass, field
from typing import Optional

from runtime.graph.graph_node import ConditionGraphNode
from runtime.graph.graph_edge import ConditionGraphEdge


@dataclass
class ConditionGraph:
    """Container for the materialized condition graph.

    Holds all projected nodes and edges for a single project, keyed by their
    deterministic identifiers. Enforces uniqueness constraints per L6.
    """

    project_id: str = ""
    nodes: dict[str, ConditionGraphNode] = field(default_factory=dict)
    edges: dict[str, ConditionGraphEdge] = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    build_version: str = ""

    def add_node(self, node: ConditionGraphNode) -> None:
        """Add a node to the graph. Raises ValueError if a node with the same id already exists."""
        if node.graph_node_id in self.nodes:
            raise ValueError(
                f"Duplicate node id: {node.graph_node_id} "
                f"(type={node.node_type}, source={node.source_object_type}:{node.source_object_id})"
            )
        self.nodes[node.graph_node_id] = node

    def add_edge(self, edge: ConditionGraphEdge) -> None:
        """Add an edge to the graph. Raises ValueError if a duplicate edge id exists (L6 constraint)."""
        if edge.graph_edge_id in self.edges:
            raise ValueError(
                f"Duplicate edge id: {edge.graph_edge_id} "
                f"(type={edge.edge_type}, {edge.from_node_id} -> {edge.to_node_id})"
            )
        self.edges[edge.graph_edge_id] = edge

    def get_node(self, graph_node_id: str) -> Optional[ConditionGraphNode]:
        """Return a node by id, or None if not found."""
        return self.nodes.get(graph_node_id)

    def get_edge(self, graph_edge_id: str) -> Optional[ConditionGraphEdge]:
        """Return an edge by id, or None if not found."""
        return self.edges.get(graph_edge_id)

    def get_nodes_by_type(self, node_type: str) -> list[ConditionGraphNode]:
        """Return all nodes matching the given node_type."""
        return [n for n in self.nodes.values() if n.node_type == node_type]

    def get_edges_by_type(self, edge_type: str) -> list[ConditionGraphEdge]:
        """Return all edges matching the given edge_type."""
        return [e for e in self.edges.values() if e.edge_type == edge_type]

    def get_edges_from(self, node_id: str) -> list[ConditionGraphEdge]:
        """Return all edges originating from the given node_id."""
        return [e for e in self.edges.values() if e.from_node_id == node_id]

    def get_edges_to(self, node_id: str) -> list[ConditionGraphEdge]:
        """Return all edges targeting the given node_id."""
        return [e for e in self.edges.values() if e.to_node_id == node_id]

    def node_count(self) -> int:
        """Return the number of nodes in the graph."""
        return len(self.nodes)

    def edge_count(self) -> int:
        """Return the number of edges in the graph."""
        return len(self.edges)
