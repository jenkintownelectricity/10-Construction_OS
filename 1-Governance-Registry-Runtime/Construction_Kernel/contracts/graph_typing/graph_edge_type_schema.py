"""Kernel-owned graph edge type schema.

Defines the canonical set of graph edge types and their required fields.
Kernel owns typing — runtime owns projection and materialization.
"""

# Canonical graph edge types for the Condition Graph.
GRAPH_EDGE_TYPES = frozenset({
    "depends_on",
    "blocked_by",
    "interfaces_with",
    "implemented_by",
    "resolved_by",
    "derived_from",
    "classified_as",
    "included_in",
    "revised_by",
    "owned_by",
    "supported_by",
})

# Required fields for every graph edge regardless of type.
GRAPH_EDGE_REQUIRED_FIELDS = frozenset({
    "graph_edge_id",
    "edge_type",
    "from_node_id",
    "to_node_id",
    "project_id",
    "source_basis",
    "lineage_ref",
})

# Edge types that are derived from enrichment (non-authoritative).
ENRICHMENT_EDGE_TYPES = frozenset({
    "classified_as",
})
