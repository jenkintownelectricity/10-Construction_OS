"""
Ownership Classifier — Wave 4
Construction OS — Guaranteed Detail Engine

Classifies extracted geometry entities by ownership using Barrett semantic maps.

Classification priority:
  1. Entity type defaults (TEXT/MTEXT/MULTILEADER/DIMENSION → ANNOTATION always)
  2. Layer exact match against barrett_layer_semantic_map.json
  3. Layer regex fallback against layer_patterns
  4. Fallback: CONTEXT_ONLY with low confidence

Input:  extraction_result dict (matching extraction_result.schema.json)
Output: dict matching ownership_classification.schema.json
"""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Config paths (relative to repo root)
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

_ENTITY_TYPE_DEFAULTS_PATH = os.path.join(_REPO_ROOT, "config", "barrett_entity_type_defaults.json")
_LAYER_SEMANTIC_MAP_PATH = os.path.join(_REPO_ROOT, "config", "barrett_layer_semantic_map.json")
_OWNERSHIP_ROLE_MAP_PATH = os.path.join(_REPO_ROOT, "config", "barrett_ownership_role_map.json")

# Annotation entity types — hardcoded as fail-safe even if config is missing
_ANNOTATION_ENTITY_TYPES = frozenset(["TEXT", "MTEXT", "MULTILEADER", "DIMENSION"])


# ---------------------------------------------------------------------------
# Config loading (graceful fallback)
# ---------------------------------------------------------------------------

def _load_json(path: str) -> dict | None:
    """Load a JSON file, returning None on any failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def _load_entity_type_defaults() -> dict[str, dict]:
    """Load entity type defaults. Returns empty dict on failure."""
    data = _load_json(_ENTITY_TYPE_DEFAULTS_PATH)
    if data and "entity_type_defaults" in data:
        return data["entity_type_defaults"]
    return {}


def _load_layer_semantic_map() -> tuple[dict[str, dict], list[dict], dict]:
    """Load layer semantic map: (exact_layers, patterns, fallback)."""
    data = _load_json(_LAYER_SEMANTIC_MAP_PATH)
    if not data:
        return {}, [], {"ownership_role": "CONTEXT_ONLY", "confidence": 0.3}

    layers = data.get("layers", {})
    patterns = data.get("layer_patterns", [])
    fallback = data.get("fallback", {"ownership_role": "CONTEXT_ONLY", "confidence": 0.5})
    return layers, patterns, fallback


# ---------------------------------------------------------------------------
# Classification logic
# ---------------------------------------------------------------------------

def _classify_entity(
    entity: dict,
    entity_type_defaults: dict[str, dict],
    layer_map: dict[str, dict],
    layer_patterns: list[dict],
    fallback: dict,
) -> dict:
    """Classify a single entity by ownership.

    Returns a classified entity dict matching the schema items shape.
    """
    entity_id = entity.get("entity_id", str(uuid.uuid4()))
    entity_type = (entity.get("entity_type") or "").upper()
    layer = entity.get("layer", "")

    # --- Priority 1: Annotation entity types (always ANNOTATION) ---
    if entity_type in _ANNOTATION_ENTITY_TYPES:
        return {
            "entity_id": entity_id,
            "layer": layer,
            "entity_type": entity_type,
            "ownership_class": "ANNOTATION",
            "classification_basis": "entity_type_default",
            "confidence": 1.0,
        }

    # Check entity_type_defaults for non-annotation fixed roles
    et_default = entity_type_defaults.get(entity_type, {})
    if et_default.get("ownership_role") and et_default["ownership_role"] != "CLASSIFY_BY_LAYER":
        return {
            "entity_id": entity_id,
            "layer": layer,
            "entity_type": entity_type,
            "ownership_class": et_default["ownership_role"],
            "classification_basis": "entity_type_default",
            "confidence": 1.0,
        }

    # --- Priority 2: Layer exact match ---
    layer_info = layer_map.get(layer)
    if layer_info:
        return {
            "entity_id": entity_id,
            "layer": layer,
            "entity_type": entity_type,
            "ownership_class": layer_info.get("ownership_role", "CONTEXT_ONLY"),
            "classification_basis": "layer_exact_match",
            "confidence": layer_info.get("confidence", 0.9),
        }

    # --- Priority 3: Layer regex fallback ---
    layer_lower = layer.lower()
    for pat in layer_patterns:
        pattern = pat.get("pattern", "")
        try:
            if re.search(pattern, layer_lower, re.IGNORECASE):
                return {
                    "entity_id": entity_id,
                    "layer": layer,
                    "entity_type": entity_type,
                    "ownership_class": pat.get("ownership_role", "CONTEXT_ONLY"),
                    "classification_basis": "layer_regex_match",
                    "confidence": pat.get("confidence", 0.7),
                }
        except re.error:
            continue

    # --- Priority 4: Fallback ---
    return {
        "entity_id": entity_id,
        "layer": layer,
        "entity_type": entity_type,
        "ownership_class": fallback.get("ownership_role", "CONTEXT_ONLY"),
        "classification_basis": "fallback_default",
        "confidence": fallback.get("confidence", 0.3),
    }


def classify_entities(extraction_result: dict) -> dict:
    """Classify all entities from an extraction result by ownership.

    Args:
        extraction_result: dict matching extraction_result.schema.json

    Returns:
        dict matching ownership_classification.schema.json
    """
    extraction_id = extraction_result.get("extraction_id", str(uuid.uuid4()))
    entities = extraction_result.get("entities", [])

    # Load configs (graceful fallback)
    entity_type_defaults = _load_entity_type_defaults()
    layer_map, layer_patterns, fallback = _load_layer_semantic_map()

    classified = []
    counts = {"system_owned": 0, "context_only": 0, "annotation": 0, "unknown": 0}

    for entity in entities:
        result = _classify_entity(
            entity, entity_type_defaults, layer_map, layer_patterns, fallback
        )
        classified.append(result)

        oc = result["ownership_class"]
        if oc == "SYSTEM_OWNED":
            counts["system_owned"] += 1
        elif oc == "CONTEXT_ONLY":
            counts["context_only"] += 1
        elif oc == "ANNOTATION":
            counts["annotation"] += 1
        else:
            counts["unknown"] += 1

    return {
        "classification_id": f"OWN-{uuid.uuid4().hex[:12].upper()}",
        "extraction_id": extraction_id,
        "classified_entities": classified,
        "summary": {
            "total": len(classified),
            "system_owned": counts["system_owned"],
            "context_only": counts["context_only"],
            "annotation": counts["annotation"],
            "unknown": counts["unknown"],
        },
        "classified_at_utc": datetime.now(timezone.utc).isoformat(),
    }
