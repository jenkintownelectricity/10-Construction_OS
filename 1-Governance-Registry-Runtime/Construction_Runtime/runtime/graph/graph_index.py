"""Graph index — fast lookup structures over a materialized ConditionGraph."""

from collections import defaultdict

from runtime.graph.condition_graph import ConditionGraph


class GraphIndex:
    """Builds and holds lookup indexes on a ConditionGraph.

    Indexes are built once at construction time. If the graph mutates,
    create a new GraphIndex.
    """

    def __init__(self, graph: ConditionGraph) -> None:
        self.graph = graph

        # node_type -> list of graph_node_ids
        self.nodes_by_type: dict[str, list[str]] = defaultdict(list)
        # edge_type -> list of graph_edge_ids
        self.edges_by_type: dict[str, list[str]] = defaultdict(list)
        # from_node_id -> list of graph_edge_ids
        self.adjacency_out: dict[str, list[str]] = defaultdict(list)
        # to_node_id -> list of graph_edge_ids
        self.adjacency_in: dict[str, list[str]] = defaultdict(list)
        # "source_object_type:source_object_id" -> graph_node_id
        self.source_to_node: dict[str, str] = {}

        self._build(graph)

    def _build(self, graph: ConditionGraph) -> None:
        """Populate all indexes from the graph."""
        for node_id, node in graph.nodes.items():
            self.nodes_by_type[node.node_type].append(node_id)
            source_key = f"{node.source_object_type}:{node.source_object_id}"
            self.source_to_node[source_key] = node_id

        for edge_id, edge in graph.edges.items():
            self.edges_by_type[edge.edge_type].append(edge_id)
            self.adjacency_out[edge.from_node_id].append(edge_id)
            self.adjacency_in[edge.to_node_id].append(edge_id)
