"""Kernel-owned graph node type schema.

Defines the canonical set of graph node types and their required fields.
Kernel owns typing — runtime owns projection and materialization.
"""

# Canonical graph node types for the Condition Graph.
GRAPH_NODE_TYPES = frozenset({
    "condition",
    "assembly",
    "interface",
    "detail",
    "issue",
    "blocker",
    "remediation",
    "artifact",
    "evidence",
    "pattern",
    "package",
    "revision",
    "owner",
})

# Required fields for every graph node regardless of type.
GRAPH_NODE_REQUIRED_FIELDS = frozenset({
    "graph_node_id",
    "node_type",
    "source_object_type",
    "source_object_id",
    "project_id",
    "label",
    "state_summary",
    "refs",
    "metadata",
    "lineage_ref",
    "node_version",
})
