"""
Assembly Candidate Generator — Wave 6
Construction OS — Guaranteed Detail Engine

Generates an assembly candidate from a condition detection result + system context.

Flow:
  1. Load Barrett condition recipes from config/assembly_condition_recipes.barrett.json
  2. Match condition_type to a recipe
  3. Generate candidate matching assembly_candidate.schema.json
  4. Status: PASS if recipe found and confidence > 0.3,
            PARTIAL if confidence <= 0.3,
            HALT if no recipe found

Fail-closed: no recipe → HALT.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_RECIPES_PATH = os.path.join(_REPO_ROOT, "config", "assembly_condition_recipes.barrett.json")
_SYSTEMS_PATH = os.path.join(_REPO_ROOT, "assemblies", "barrett", "ramproof_gc_systems.json")

# Barrett defaults
_DEFAULT_MANUFACTURER_ID = "MFR-BARRETT-001"
_DEFAULT_SYSTEM_ID = "FAM-BARRETT-RAMPROOF-GC"

# Condition type aliases — map supported pipeline condition names to recipe condition_types
_CONDITION_ALIASES: dict[str, list[str]] = {
    "parapet": ["parapet_termination", "parapet"],
    "drain": ["roof_drain", "drain"],
    "penetration": ["pipe_penetration", "penetration"],
    "corner": ["corner", "inside_corner", "outside_corner"],
    "expansion_joint": ["expansion_joint"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_json(path: str) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def _load_recipes() -> list[dict]:
    """Load Barrett condition recipes. Returns empty list on failure."""
    data = _load_json(_RECIPES_PATH)
    if data and "recipes" in data:
        return data["recipes"]
    return []


def _load_system_info() -> dict:
    """Load Barrett system info for manufacturer/system IDs."""
    data = _load_json(_SYSTEMS_PATH)
    if data:
        return data
    return {}


def _find_recipe(condition_type: str, recipes: list[dict]) -> dict | None:
    """Find a matching recipe for the given condition_type.

    Tries exact match first, then alias lookup.
    """
    # Exact match on recipe condition_type
    for recipe in recipes:
        if recipe.get("condition_type") == condition_type:
            return recipe

    # Alias expansion
    aliases = _CONDITION_ALIASES.get(condition_type, [condition_type])
    for alias in aliases:
        for recipe in recipes:
            if recipe.get("condition_type") == alias:
                return recipe
            if recipe.get("recipe_family") == alias:
                return recipe

    return None


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_candidate(
    condition_result: dict,
    manufacturer_id: str | None = None,
    system_id: str | None = None,
) -> dict:
    """Generate an assembly candidate from a condition result.

    Args:
        condition_result: dict matching condition_result.schema.json
        manufacturer_id: Override manufacturer ID
        system_id: Override system ID

    Returns:
        dict matching assembly_candidate.schema.json
    """
    condition_type = condition_result.get("condition_type", "")
    confidence = condition_result.get("confidence", 0.0)
    support_state = condition_result.get("support_state", "NO_SOURCE")
    condition_id = condition_result.get("condition_id", "")
    extraction_id = condition_result.get("extraction_id", "")

    # Load system info for defaults
    system_info = _load_system_info()
    mfr_id = manufacturer_id or system_info.get("manufacturer_id", _DEFAULT_MANUFACTURER_ID)
    sys_id = system_id or system_info.get("family_id", _DEFAULT_SYSTEM_ID)

    candidate_id = f"CAND-{uuid.uuid4().hex[:12].upper()}"
    now_utc = datetime.now(timezone.utc).isoformat()

    # If support_state is NO_SOURCE, halt immediately
    if support_state == "NO_SOURCE":
        return {
            "candidate_id": candidate_id,
            "manufacturer_id": mfr_id,
            "system_id": sys_id,
            "condition_type": condition_type or "unknown",
            "source_evidence_id": condition_id,
            "extraction_id": extraction_id,
            "condition_result_id": condition_id,
            "geometry_reference": "",
            "confidence": 0.0,
            "status": "HALT",
            "halt_reason": "No condition source detected (NO_SOURCE support_state).",
            "created_at_utc": now_utc,
        }

    # If unsupported condition, halt
    if support_state == "UNSUPPORTED_CONDITION":
        return {
            "candidate_id": candidate_id,
            "manufacturer_id": mfr_id,
            "system_id": sys_id,
            "condition_type": condition_type,
            "source_evidence_id": condition_id,
            "extraction_id": extraction_id,
            "condition_result_id": condition_id,
            "geometry_reference": "",
            "confidence": confidence,
            "status": "HALT",
            "halt_reason": f"Unsupported condition type: {condition_type}.",
            "created_at_utc": now_utc,
        }

    # Load recipes and match
    recipes = _load_recipes()
    recipe = _find_recipe(condition_type, recipes)

    if recipe is None:
        return {
            "candidate_id": candidate_id,
            "manufacturer_id": mfr_id,
            "system_id": sys_id,
            "condition_type": condition_type,
            "source_evidence_id": condition_id,
            "extraction_id": extraction_id,
            "condition_result_id": condition_id,
            "geometry_reference": "",
            "confidence": confidence,
            "status": "HALT",
            "halt_reason": f"No recipe found for condition type '{condition_type}'.",
            "created_at_utc": now_utc,
        }

    # Recipe found — determine status by confidence threshold
    if confidence > 0.3:
        status = "PASS"
        halt_reason = ""
    else:
        status = "PARTIAL"
        halt_reason = f"Low confidence ({confidence:.2f} <= 0.3) for condition '{condition_type}'."

    return {
        "candidate_id": candidate_id,
        "manufacturer_id": mfr_id,
        "system_id": sys_id,
        "condition_type": condition_type,
        "source_evidence_id": condition_id,
        "extraction_id": extraction_id,
        "condition_result_id": condition_id,
        "geometry_reference": recipe.get("assembly_id", ""),
        "confidence": confidence,
        "status": status,
        "halt_reason": halt_reason if halt_reason else "",
        "created_at_utc": now_utc,
    }
