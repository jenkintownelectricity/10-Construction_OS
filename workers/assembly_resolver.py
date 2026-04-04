"""
Assembly Resolver — Wave 7
Construction OS — Guaranteed Detail Engine

Resolves an assembly candidate to a concrete detail.

Flow:
  1. Load Barrett system details from config / demo seed data
  2. Match system_id + condition_type to a detail_id
  3. Return assembly_resolution_result.schema.json shape

source_mode:
  LIVE_EXTRACTED — extraction drove the resolution
  DEMO_SEED     — fallback to hardcoded seed data

resolution_status:
  RESOLVED  — match found
  NO_MATCH  — no detail for this system+condition
  HALTED    — candidate was HALT status

Fail-closed: unknown states → HALTED.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Config / seed data
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_RECIPES_PATH = os.path.join(_REPO_ROOT, "config", "assembly_condition_recipes.barrett.json")
_SYSTEMS_PATH = os.path.join(_REPO_ROOT, "assemblies", "barrett", "ramproof_gc_systems.json")

# Demo seed detail map — hardcoded to match Supabase seed data.
# Maps (system_id_prefix, condition_alias) → (detail_id, detail_label)
_DEMO_SEED_DETAILS: dict[tuple[str, str], tuple[str, str]] = {
    ("BARRETT", "parapet"): (
        "DTL-BARRETT-RP-PARAPET-001",
        "RamProof GC Parapet Termination Detail",
    ),
    ("BARRETT", "drain"): (
        "DTL-BARRETT-RP-DRAIN-001",
        "RamProof GC Roof Drain Detail",
    ),
    ("BARRETT", "penetration"): (
        "DTL-BARRETT-RP-PENE-001",
        "RamProof GC Pipe Penetration Detail",
    ),
    ("BARRETT", "corner"): (
        "DTL-BARRETT-RP-CORNER-001",
        "RamProof GC Corner Detail",
    ),
    ("BARRETT", "expansion_joint"): (
        "DTL-BARRETT-RP-EXPJT-001",
        "RamProof GC Expansion Joint Detail",
    ),
}

# Condition type aliases (same as candidate generator)
_CONDITION_NORMALIZE: dict[str, str] = {
    "parapet_termination": "parapet",
    "roof_drain": "drain",
    "pipe_penetration": "penetration",
    "inside_corner": "corner",
    "outside_corner": "corner",
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
    data = _load_json(_RECIPES_PATH)
    if data and "recipes" in data:
        return data["recipes"]
    return []


def _normalize_condition(condition_type: str) -> str:
    """Normalize condition type to canonical form."""
    return _CONDITION_NORMALIZE.get(condition_type, condition_type)


def _manufacturer_prefix(manufacturer_id: str) -> str:
    """Extract manufacturer prefix for seed lookup."""
    mid = (manufacturer_id or "").upper()
    if "BARRETT" in mid:
        return "BARRETT"
    return mid


def _resolve_from_recipes(
    system_id: str, condition_type: str, recipes: list[dict]
) -> tuple[str, str] | None:
    """Try to resolve detail from recipes. Returns (detail_id, label) or None."""
    normalized = _normalize_condition(condition_type)
    for recipe in recipes:
        rc = _normalize_condition(recipe.get("condition_type", ""))
        if rc == normalized:
            assembly_id = recipe.get("assembly_id", "")
            label = recipe.get("description", f"{system_id} {condition_type} detail")
            return assembly_id, label
    return None


def _resolve_from_seed(
    manufacturer_id: str, condition_type: str
) -> tuple[str, str] | None:
    """Try to resolve detail from demo seed data."""
    prefix = _manufacturer_prefix(manufacturer_id)
    normalized = _normalize_condition(condition_type)
    key = (prefix, normalized)
    return _DEMO_SEED_DETAILS.get(key)


# ---------------------------------------------------------------------------
# Main resolver
# ---------------------------------------------------------------------------

def resolve_assembly(candidate: dict) -> dict:
    """Resolve an assembly candidate to a detail.

    Args:
        candidate: dict matching assembly_candidate.schema.json

    Returns:
        dict matching assembly_resolution_result.schema.json
    """
    candidate_id = candidate.get("candidate_id", "")
    manufacturer_id = candidate.get("manufacturer_id", "")
    system_id = candidate.get("system_id", "")
    condition_type = candidate.get("condition_type", "")
    candidate_status = candidate.get("status", "HALT")
    confidence = candidate.get("confidence", 0.0)

    resolution_id = f"RES-{uuid.uuid4().hex[:12].upper()}"
    now_utc = datetime.now(timezone.utc).isoformat()

    # If candidate is HALT, propagate halt
    if candidate_status == "HALT":
        return {
            "resolution_id": resolution_id,
            "candidate_id": candidate_id,
            "manufacturer_id": manufacturer_id,
            "system_id": system_id,
            "condition_type": condition_type,
            "resolution_status": "HALTED",
            "resolved_detail_id": "",
            "resolved_detail_label": "",
            "resolution_basis": candidate.get("halt_reason", "Candidate HALT propagated."),
            "confidence": 0.0,
            "source_mode": "NO_RESULT",
            "resolved_at_utc": now_utc,
        }

    # Try live resolution from recipes (LIVE_EXTRACTED path)
    recipes = _load_recipes()
    live_result = _resolve_from_recipes(system_id, condition_type, recipes)

    if live_result:
        detail_id, detail_label = live_result
        return {
            "resolution_id": resolution_id,
            "candidate_id": candidate_id,
            "manufacturer_id": manufacturer_id,
            "system_id": system_id,
            "condition_type": condition_type,
            "resolution_status": "RESOLVED",
            "resolved_detail_id": detail_id,
            "resolved_detail_label": detail_label,
            "resolution_basis": "Matched condition_type to Barrett recipe assembly_id.",
            "confidence": confidence,
            "source_mode": "LIVE_EXTRACTED",
            "resolved_at_utc": now_utc,
        }

    # Fallback to demo seed
    seed_result = _resolve_from_seed(manufacturer_id, condition_type)

    if seed_result:
        detail_id, detail_label = seed_result
        return {
            "resolution_id": resolution_id,
            "candidate_id": candidate_id,
            "manufacturer_id": manufacturer_id,
            "system_id": system_id,
            "condition_type": condition_type,
            "resolution_status": "RESOLVED",
            "resolved_detail_id": detail_id,
            "resolved_detail_label": detail_label,
            "resolution_basis": "Resolved from demo seed data (no live recipe match).",
            "confidence": max(confidence * 0.8, 0.0),  # discount for seed
            "source_mode": "DEMO_SEED",
            "resolved_at_utc": now_utc,
        }

    # No match anywhere
    return {
        "resolution_id": resolution_id,
        "candidate_id": candidate_id,
        "manufacturer_id": manufacturer_id,
        "system_id": system_id,
        "condition_type": condition_type,
        "resolution_status": "NO_MATCH",
        "resolved_detail_id": "",
        "resolved_detail_label": "",
        "resolution_basis": f"No detail found for system '{system_id}' + condition '{condition_type}'.",
        "confidence": 0.0,
        "source_mode": "NO_RESULT",
        "resolved_at_utc": now_utc,
    }
