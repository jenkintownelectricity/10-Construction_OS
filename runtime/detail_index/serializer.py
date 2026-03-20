"""
Detail Index Serializer — Wave 15.

Deterministic JSON serialization for detail index artifacts.
"""

import json
from typing import Any


def serialize_detail_index(index_artifact: dict[str, Any]) -> str:
    """Serialize a detail index artifact to deterministic JSON."""
    return json.dumps(index_artifact, sort_keys=True, indent=2, ensure_ascii=False)


def deserialize_detail_index(json_str: str) -> dict[str, Any]:
    """Deserialize a detail index artifact from JSON."""
    return json.loads(json_str)
