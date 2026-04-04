"""
Condition Bridge — Wave 5
Construction OS — Guaranteed Detail Engine

Bridges ownership-classified geometry to condition detection.

Flow:
  1. Filter classified entities to SYSTEM_OWNED and CONTEXT_ONLY (exclude ANNOTATION)
  2. Call detect_condition_geometry.detect_conditions() with filtered entities
  3. Map results to condition_result.schema.json shape
  4. Add support_state honesty flag
  5. Return best (highest confidence) supported condition result

Fail-closed: unknown states → NO_SOURCE.
"""

from __future__ import annotations

import os
import sys
import uuid
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Import detect_condition_geometry from tools/
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_TOOLS_DIR = os.path.join(_REPO_ROOT, "tools")

if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from detect_condition_geometry import detect_conditions  # noqa: E402

# ---------------------------------------------------------------------------
# Supported conditions — must match pipeline contract
# ---------------------------------------------------------------------------

SUPPORTED_CONDITIONS = frozenset([
    "parapet", "drain", "penetration", "corner", "expansion_joint",
])


# ---------------------------------------------------------------------------
# Bridge logic
# ---------------------------------------------------------------------------

def _filter_for_detection(classified_entities: list[dict]) -> list[dict]:
    """Filter classified entities to those relevant for condition detection.

    Include SYSTEM_OWNED and CONTEXT_ONLY. Exclude ANNOTATION and UNKNOWN.
    """
    return [
        e for e in classified_entities
        if e.get("ownership_class") in ("SYSTEM_OWNED", "CONTEXT_ONLY")
    ]


def _map_to_condition_result(
    detection: dict,
    extraction_id: str,
    source_entity_count: int,
) -> dict:
    """Map a detect_conditions() result to condition_result.schema.json shape."""
    condition = detection.get("condition", "")
    confidence = detection.get("confidence", 0.0)
    features = detection.get("features", [])

    if condition in SUPPORTED_CONDITIONS:
        support_state = "SUPPORTED"
    else:
        support_state = "UNSUPPORTED_CONDITION"

    return {
        "condition_id": f"COND-{uuid.uuid4().hex[:12].upper()}",
        "extraction_id": extraction_id,
        "condition_type": condition,
        "support_state": support_state,
        "confidence": confidence,
        "features": features,
        "source_entity_count": source_entity_count,
        "detected_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def bridge_to_condition(
    ownership_classification: dict,
    extraction_id: str | None = None,
) -> dict:
    """Bridge ownership-classified entities to condition detection.

    Args:
        ownership_classification: dict matching ownership_classification.schema.json
        extraction_id: Optional override; defaults to extraction_id from classification

    Returns:
        dict matching condition_result.schema.json — best supported condition,
        or a NO_SOURCE result if nothing detected.
    """
    if extraction_id is None:
        extraction_id = ownership_classification.get("extraction_id", str(uuid.uuid4()))

    classified_entities = ownership_classification.get("classified_entities", [])
    filtered = _filter_for_detection(classified_entities)

    if not filtered:
        # No entities to analyze
        return {
            "condition_id": f"COND-{uuid.uuid4().hex[:12].upper()}",
            "extraction_id": extraction_id,
            "condition_type": "",
            "support_state": "NO_SOURCE",
            "confidence": 0.0,
            "features": [],
            "source_entity_count": 0,
            "detected_at_utc": datetime.now(timezone.utc).isoformat(),
        }

    # Build geometry dict for the detector
    geometry_json = {"entities": filtered}
    raw_detections = detect_conditions(geometry_json)

    if not raw_detections:
        return {
            "condition_id": f"COND-{uuid.uuid4().hex[:12].upper()}",
            "extraction_id": extraction_id,
            "condition_type": "",
            "support_state": "NO_SOURCE",
            "confidence": 0.0,
            "features": [],
            "source_entity_count": len(filtered),
            "detected_at_utc": datetime.now(timezone.utc).isoformat(),
        }

    # Map all detections, then pick best supported
    mapped = [
        _map_to_condition_result(d, extraction_id, len(filtered))
        for d in raw_detections
    ]

    # Prefer SUPPORTED conditions; among those, pick highest confidence
    supported = [m for m in mapped if m["support_state"] == "SUPPORTED"]
    if supported:
        best = max(supported, key=lambda m: m["confidence"])
    else:
        # All unsupported — return highest confidence unsupported
        best = max(mapped, key=lambda m: m["confidence"])

    return best
