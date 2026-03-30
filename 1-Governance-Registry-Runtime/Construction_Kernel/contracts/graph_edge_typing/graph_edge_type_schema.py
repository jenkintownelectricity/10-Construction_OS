"""Kernel-owned graph edge type schema with per-type constraint contracts.

Defines GRAPH_EDGE_TYPES as an immutable mapping from edge type name
to its constraint schema including valid source/target node types.

Kernel owns typing only — no projection, materialization, or query logic.
"""

from types import MappingProxyType


def _edge_schema(
    edge_type: str,
    valid_from: frozenset,
    valid_to: frozenset,
    is_enrichment_derived: bool = False,
) -> dict:
    """Build an immutable edge type schema entry."""
    return MappingProxyType({
        "edge_type": edge_type,
        "valid_from_node_types": valid_from,
        "valid_to_node_types": valid_to,
        "is_enrichment_derived": is_enrichment_derived,
    })


GRAPH_EDGE_TYPES = MappingProxyType({
    "depends_on": _edge_schema(
        "depends_on",
        valid_from=frozenset({"condition"}),
        valid_to=frozenset({"condition"}),
    ),
    "blocked_by": _edge_schema(
        "blocked_by",
        valid_from=frozenset({"condition"}),
        valid_to=frozenset({"blocker", "issue"}),
    ),
    "interfaces_with": _edge_schema(
        "interfaces_with",
        valid_from=frozenset({"assembly", "condition"}),
        valid_to=frozenset({"assembly", "interface"}),
    ),
    "implemented_by": _edge_schema(
        "implemented_by",
        valid_from=frozenset({"detail"}),
        valid_to=frozenset({"assembly"}),
    ),
    "resolved_by": _edge_schema(
        "resolved_by",
        valid_from=frozenset({"blocker", "issue"}),
        valid_to=frozenset({"remediation"}),
    ),
    "derived_from": _edge_schema(
        "derived_from",
        valid_from=frozenset({"condition", "artifact"}),
        valid_to=frozenset({"evidence", "package"}),
    ),
    "classified_as": _edge_schema(
        "classified_as",
        valid_from=frozenset({"condition"}),
        valid_to=frozenset({"pattern"}),
        is_enrichment_derived=True,
    ),
    "included_in": _edge_schema(
        "included_in",
        valid_from=frozenset({"assembly", "artifact", "detail", "condition"}),
        valid_to=frozenset({"package", "assembly"}),
    ),
    "revised_by": _edge_schema(
        "revised_by",
        valid_from=frozenset({"condition", "assembly", "package", "artifact"}),
        valid_to=frozenset({"revision"}),
    ),
    "owned_by": _edge_schema(
        "owned_by",
        valid_from=frozenset({"condition", "assembly"}),
        valid_to=frozenset({"owner"}),
    ),
    "supported_by": _edge_schema(
        "supported_by",
        valid_from=frozenset({"evidence", "remediation"}),
        valid_to=frozenset({"artifact", "evidence"}),
    ),
})
