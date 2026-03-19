"""Kernel-owned graph node type schema with per-type field contracts.

Defines GRAPH_NODE_TYPES as an immutable mapping from node type name
to its required and optional source field schemas.

Kernel owns typing only — no projection, materialization, or query logic.
"""

from types import MappingProxyType


def _node_schema(node_type: str, required: frozenset, optional: frozenset = frozenset()) -> dict:
    """Build an immutable node type schema entry."""
    return MappingProxyType({
        "node_type": node_type,
        "required_source_fields": required,
        "optional_source_fields": optional,
    })


GRAPH_NODE_TYPES = MappingProxyType({
    "condition": _node_schema(
        "condition",
        required=frozenset({"condition_id", "label", "severity", "status", "location_ref"}),
        optional=frozenset({"description", "detected_date", "category"}),
    ),
    "assembly": _node_schema(
        "assembly",
        required=frozenset({"assembly_id", "label", "assembly_type", "location_ref"}),
        optional=frozenset({"description", "spec_section"}),
    ),
    "interface": _node_schema(
        "interface",
        required=frozenset({"interface_id", "label", "interface_type"}),
        optional=frozenset({"description", "assembly_refs"}),
    ),
    "detail": _node_schema(
        "detail",
        required=frozenset({"detail_id", "label", "detail_type", "sheet_ref"}),
        optional=frozenset({"description", "scale", "spec_section"}),
    ),
    "issue": _node_schema(
        "issue",
        required=frozenset({"issue_id", "label", "severity", "status"}),
        optional=frozenset({"description", "reported_date", "reporter"}),
    ),
    "blocker": _node_schema(
        "blocker",
        required=frozenset({"blocker_id", "label", "severity", "status"}),
        optional=frozenset({"description", "blocking_reason", "reported_date"}),
    ),
    "remediation": _node_schema(
        "remediation",
        required=frozenset({"remediation_id", "label", "remediation_type", "status"}),
        optional=frozenset({"description", "assigned_to", "due_date"}),
    ),
    "artifact": _node_schema(
        "artifact",
        required=frozenset({"artifact_id", "label", "artifact_type", "file_ref"}),
        optional=frozenset({"description", "version", "format"}),
    ),
    "evidence": _node_schema(
        "evidence",
        required=frozenset({"evidence_id", "label", "evidence_type", "source_ref"}),
        optional=frozenset({"description", "captured_date", "confidence"}),
    ),
    "pattern": _node_schema(
        "pattern",
        required=frozenset({"pattern_id", "label", "pattern_type"}),
        optional=frozenset({"description", "frequency", "known_cause"}),
    ),
    "package": _node_schema(
        "package",
        required=frozenset({"package_id", "label", "package_type"}),
        optional=frozenset({"description", "version", "scope"}),
    ),
    "revision": _node_schema(
        "revision",
        required=frozenset({"revision_id", "label", "revision_number", "effective_date"}),
        optional=frozenset({"description", "author", "change_summary"}),
    ),
    "owner": _node_schema(
        "owner",
        required=frozenset({"owner_id", "label", "owner_type"}),
        optional=frozenset({"description", "contact_ref", "organization"}),
    ),
})
