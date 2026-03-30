"""
Condition Graph Serializer — Wave 14 Subsystem 1.

Serializes and deserializes condition graphs to/from JSON.
Deterministic output guaranteed.
"""

import hashlib
import json
from typing import Any


class ConditionGraphSerializationError(Exception):
    """Raised when serialization or deserialization fails."""


def serialize_graph(graph: dict[str, Any]) -> str:
    """Serialize a condition graph to a deterministic JSON string."""
    required_keys = {"graph_id", "source_refs", "build_timestamp", "contract_version", "nodes", "edges", "checksum"}
    missing = required_keys - set(graph.keys())
    if missing:
        raise ConditionGraphSerializationError(
            f"Cannot serialize: missing required keys: {sorted(missing)}"
        )
    return json.dumps(graph, indent=2, sort_keys=False, ensure_ascii=True)


def deserialize_graph(json_string: str) -> dict[str, Any]:
    """Deserialize a condition graph from a JSON string."""
    try:
        graph = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ConditionGraphSerializationError(
            f"Invalid JSON: {e}"
        ) from e

    if not isinstance(graph, dict):
        raise ConditionGraphSerializationError("Graph must be a JSON object.")

    required_keys = {"graph_id", "nodes", "edges"}
    missing = required_keys - set(graph.keys())
    if missing:
        raise ConditionGraphSerializationError(
            f"Missing required keys: {sorted(missing)}"
        )
    return graph


def compute_checksum(graph: dict[str, Any]) -> str:
    """Compute deterministic checksum for graph content (nodes + edges only)."""
    content = json.dumps(
        {"nodes": graph.get("nodes", []), "edges": graph.get("edges", [])},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def verify_checksum(graph: dict[str, Any]) -> bool:
    """Verify the checksum of a serialized graph matches its content."""
    stored = graph.get("checksum")
    if not stored:
        return False
    return compute_checksum(graph) == stored
