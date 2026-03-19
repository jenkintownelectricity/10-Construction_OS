"""Wave 11A condition graph edge — deterministic identity, typed relationships."""

import hashlib
from dataclasses import dataclass, field


@dataclass
class ConditionGraphEdge:
    """An edge in the Wave 11A condition graph.

    Each edge represents a relationship between two graph nodes. Identity is
    deterministic via SHA-256 of (edge_type, from_node_id, to_node_id, project_id).
    """

    graph_edge_id: str = ""
    edge_type: str = ""  # depends_on | blocked_by | interfaces_with | implemented_by | resolved_by | derived_from | classified_as | included_in | revised_by | owned_by | supported_by
    from_node_id: str = ""
    to_node_id: str = ""
    project_id: str = ""
    source_basis: str = ""  # describes what runtime fact generated this edge
    lineage_ref: str = ""
    is_enrichment_derived: bool = False  # True only for pattern-derived edges like classified_as
    metadata: dict = field(default_factory=dict)

    @staticmethod
    def compute_edge_id(edge_type: str, from_node_id: str, to_node_id: str, project_id: str) -> str:
        """Return a deterministic SHA-256 hex digest (first 16 chars) of the edge quad."""
        raw = f"{edge_type}:{from_node_id}:{to_node_id}:{project_id}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
