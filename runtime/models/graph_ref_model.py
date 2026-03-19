"""Graph reference model for addressable construction graph nodes and edges."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GraphNode:
    """A node in the construction graph.

    Nodes represent assemblies, interfaces, details, parameters, or other
    addressable elements within the project model.
    """

    node_id: str = ""
    node_type: str = ""  # assembly | interface | detail | parameter | condition
    label: str = ""
    attributes: dict = field(default_factory=dict)
    parent_ref: str = ""
    child_refs: list[str] = field(default_factory=list)


@dataclass
class GraphEdge:
    """An edge in the construction graph.

    Edges represent relationships between nodes such as containment,
    dependency, interface connection, or reference.
    """

    edge_id: str = ""
    edge_type: str = ""  # contains | depends_on | interfaces_with | references
    source_node_id: str = ""
    target_node_id: str = ""
    attributes: dict = field(default_factory=dict)
    weight: float = 1.0


@dataclass
class GraphRef:
    """A reference into the construction graph.

    Provides addressability for any element in the graph via a structured
    path or direct node/edge reference.
    """

    ref_id: str = ""
    path: str = ""  # e.g., "project/assembly-01/interface-03/detail-02"
    node_id: str = ""
    edge_id: str = ""
    ref_type: str = ""  # node | edge | subgraph
    resolved: bool = False
    resolution_target: str = ""
