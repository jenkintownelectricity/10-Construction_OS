"""
Edge Registry — Wave 17A Construction Reference Graph.

Registers and manages typed edges between reference graph nodes.
All edges are validated for type compatibility, uniqueness, and partition rules.
"""

import hashlib
from datetime import datetime, timezone
from typing import Any

from runtime.reference_graph.node_registry import NodeRegistry, VALID_STATUSES


# === Relationship type categories ===

IDENTITY_RELATION_TYPES = frozenset([
    "instance_of", "belongs_to_project", "references_canonical", "scoped_under",
])

LINEAGE_RELATION_TYPES = frozenset([
    "derived_from", "produced_by", "rendered_from", "supersedes",
    "revision_of", "generated_from",
])

ARTIFACT_RELATION_TYPES = frozenset([
    "appears_in", "annotates", "region_of", "page_of", "attached_to",
])

OBSERVATION_RELATION_TYPES = frozenset([
    "observed_in", "documents", "verifies", "flags", "supports", "invalidates",
])

NAVIGATION_RELATION_TYPES = frozenset([
    "related_to", "installed_before", "installed_after",
    "alternative_to", "prerequisite_for",
])

ALL_RELATION_TYPES = (
    IDENTITY_RELATION_TYPES
    | LINEAGE_RELATION_TYPES
    | ARTIFACT_RELATION_TYPES
    | OBSERVATION_RELATION_TYPES
    | NAVIGATION_RELATION_TYPES
)

# Deterministic relation types that cannot be overwritten by advisory edges
DETERMINISTIC_RELATION_TYPES = (
    IDENTITY_RELATION_TYPES | LINEAGE_RELATION_TYPES | ARTIFACT_RELATION_TYPES
)

# Advisory relation types
ADVISORY_RELATION_TYPES = NAVIGATION_RELATION_TYPES

# Valid (from_type, to_type) pairs for select relation types
RELATION_TYPE_RULES: dict[str, dict[str, list[str]]] = {
    "instance_of": {
        "valid_from": ["VARIANT", "MANIFEST", "RENDER_JOB", "DRAWING", "PDF", "DXF", "SVG"],
        "valid_to": ["DETAIL", "INSTRUCTION_SET"],
    },
    "belongs_to_project": {
        "valid_from": ["CONDITION", "MANIFEST", "RENDER_JOB", "OBSERVATION", "MARKUP"],
        "valid_to": ["PROJECT"],
    },
    "derived_from": {
        "valid_from": ["VARIANT"],
        "valid_to": ["DETAIL"],
    },
    "produced_by": {
        "valid_from": ["MANIFEST", "DRAWING", "PDF", "DXF", "SVG"],
        "valid_to": ["RENDER_JOB", "INSTRUCTION_SET", "MANIFEST"],
    },
    "rendered_from": {
        "valid_from": ["DRAWING", "PDF", "DXF", "SVG"],
        "valid_to": ["RENDER_JOB"],
    },
    "region_of": {
        "valid_from": ["ARTIFACT_REGION"],
        "valid_to": ["DRAWING", "PDF", "DXF", "SVG", "ARTIFACT"],
    },
    "page_of": {
        "valid_from": ["PAGE_REFERENCE"],
        "valid_to": ["PDF", "DRAWING"],
    },
    "annotates": {
        "valid_from": ["MARKUP", "ANNOTATION"],
        "valid_to": ["DRAWING", "PDF", "DXF", "SVG", "ARTIFACT", "ARTIFACT_REGION"],
    },
    "observed_in": {
        "valid_from": ["OBSERVATION"],
        "valid_to": ["PROJECT", "CONDITION", "ARTIFACT"],
    },
}


class EdgeRegistrationError(Exception):
    """Raised when edge registration fails. Fail closed."""


class EdgeRegistry:
    """Registry for typed edges in the reference graph."""

    def __init__(self, node_registry: NodeRegistry) -> None:
        self._node_registry = node_registry
        self._edges: dict[str, dict[str, Any]] = {}
        self._edge_fingerprints: set[str] = set()
        self._adjacency_out: dict[str, list[str]] = {}
        self._adjacency_in: dict[str, list[str]] = {}

    @staticmethod
    def compute_edge_id(
        relation_type: str, from_id: str, to_id: str,
    ) -> str:
        """Compute deterministic edge ID."""
        raw = f"{relation_type}:{from_id}:{to_id}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def compute_edge_fingerprint(
        relation_type: str, from_id: str, to_id: str,
    ) -> str:
        """Compute fingerprint for duplicate detection."""
        return f"{relation_type}:{from_id}:{to_id}"

    def register(
        self,
        relation_type: str,
        from_id: str,
        to_id: str,
        source_basis: str = "",
        is_advisory: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Register a typed edge.

        Raises:
            EdgeRegistrationError on validation failures.
        """
        if relation_type not in ALL_RELATION_TYPES:
            raise EdgeRegistrationError(
                f"Invalid relation_type '{relation_type}'."
            )

        from_node = self._node_registry.get(from_id)
        if not from_node:
            raise EdgeRegistrationError(
                f"Source node '{from_id}' not found in node registry."
            )
        to_node = self._node_registry.get(to_id)
        if not to_node:
            raise EdgeRegistrationError(
                f"Target node '{to_id}' not found in node registry."
            )

        self._validate_relation_type_rules(
            relation_type, from_node["object_type"], to_node["object_type"],
        )

        fingerprint = self.compute_edge_fingerprint(relation_type, from_id, to_id)
        if fingerprint in self._edge_fingerprints:
            edge_id = self.compute_edge_id(relation_type, from_id, to_id)
            existing = self._edges.get(edge_id)
            if existing:
                return existing
            raise EdgeRegistrationError(
                f"Duplicate edge: {relation_type} from {from_id} to {to_id}."
            )

        if is_advisory and relation_type in DETERMINISTIC_RELATION_TYPES:
            raise EdgeRegistrationError(
                f"Cannot mark deterministic relation '{relation_type}' as advisory."
            )

        existing_deterministic = self._find_deterministic_edge(from_id, to_id)
        if existing_deterministic and is_advisory:
            raise EdgeRegistrationError(
                f"Advisory edge cannot overwrite deterministic edge "
                f"between {from_id} and {to_id}."
            )

        edge_id = self.compute_edge_id(relation_type, from_id, to_id)

        edge: dict[str, Any] = {
            "edge_id": edge_id,
            "relation_type": relation_type,
            "from_id": from_id,
            "to_id": to_id,
            "from_type": from_node["object_type"],
            "to_type": to_node["object_type"],
            "source_basis": source_basis,
            "is_advisory": is_advisory,
            "created_timestamp": datetime.now(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "status": "active",
            "metadata": metadata or {},
        }

        self._edges[edge_id] = edge
        self._edge_fingerprints.add(fingerprint)

        self._adjacency_out.setdefault(from_id, []).append(to_id)
        self._adjacency_in.setdefault(to_id, []).append(from_id)

        return edge

    def get(self, edge_id: str) -> dict[str, Any] | None:
        return self._edges.get(edge_id)

    def get_edges_from(self, node_id: str) -> list[dict[str, Any]]:
        """Get all outgoing edges from a node."""
        return [
            e for e in self._edges.values()
            if e["from_id"] == node_id and e["status"] == "active"
        ]

    def get_edges_to(self, node_id: str) -> list[dict[str, Any]]:
        """Get all incoming edges to a node."""
        return [
            e for e in self._edges.values()
            if e["to_id"] == node_id and e["status"] == "active"
        ]

    def get_edges_by_type(self, relation_type: str) -> list[dict[str, Any]]:
        """Get all edges of a given type."""
        return [
            e for e in self._edges.values()
            if e["relation_type"] == relation_type
        ]

    def list_edges(
        self,
        relation_type: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        results = list(self._edges.values())
        if relation_type:
            results = [e for e in results if e["relation_type"] == relation_type]
        if status:
            results = [e for e in results if e["status"] == status]
        return sorted(results, key=lambda e: e["edge_id"])

    def update_status(self, edge_id: str, new_status: str) -> dict[str, Any]:
        if new_status not in VALID_STATUSES:
            raise EdgeRegistrationError(f"Invalid status '{new_status}'.")
        edge = self._edges.get(edge_id)
        if not edge:
            raise EdgeRegistrationError(f"Edge '{edge_id}' not found.")
        edge["status"] = new_status
        return edge

    @property
    def edge_count(self) -> int:
        return len(self._edges)

    @property
    def adjacency_out(self) -> dict[str, list[str]]:
        return dict(self._adjacency_out)

    @property
    def adjacency_in(self) -> dict[str, list[str]]:
        return dict(self._adjacency_in)

    def _validate_relation_type_rules(
        self, relation_type: str, from_type: str, to_type: str,
    ) -> None:
        """Validate that from/to types are valid for this relation type."""
        if relation_type in RELATION_TYPE_RULES:
            rules = RELATION_TYPE_RULES[relation_type]
            if from_type not in rules["valid_from"]:
                raise EdgeRegistrationError(
                    f"Relation '{relation_type}' does not support "
                    f"from_type '{from_type}'. Valid: {rules['valid_from']}"
                )
            if to_type not in rules["valid_to"]:
                raise EdgeRegistrationError(
                    f"Relation '{relation_type}' does not support "
                    f"to_type '{to_type}'. Valid: {rules['valid_to']}"
                )

    def _find_deterministic_edge(
        self, from_id: str, to_id: str,
    ) -> dict[str, Any] | None:
        """Find existing deterministic edge between two nodes."""
        for edge in self._edges.values():
            if (
                edge["from_id"] == from_id
                and edge["to_id"] == to_id
                and not edge["is_advisory"]
            ):
                return edge
        return None
