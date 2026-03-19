"""Kernel-owned graph relation typing rules.

Defines GRAPH_RELATION_RULES as a structural contract for edge relation
constraints. Runtime enforces these rules during materialization.

Kernel owns typing only — no projection, materialization, or query logic.
"""

from types import MappingProxyType


GRAPH_RELATION_RULES = MappingProxyType({
    "max_edges_per_pair": 1,
    "enrichment_edge_types": frozenset({"classified_as"}),
    "hard_edge_types": frozenset({
        "depends_on",
        "blocked_by",
        "interfaces_with",
        "implemented_by",
        "resolved_by",
        "derived_from",
        "included_in",
        "revised_by",
        "owned_by",
        "supported_by",
    }),
    "identity_fields": ("from_node_id", "to_node_id", "edge_type"),
})
