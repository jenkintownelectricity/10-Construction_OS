"""
Conflict Detector Module.

Detects conflicts between the resolved pattern and other patterns
using governed relationship definitions from the kernel.

Emits explicit conflict records. Fail-closed on conflict detection.
"""

import uuid

from engine.config import FAIL_CONFLICT_DETECTED
from contracts.pattern_kernel_consumer import PatternKernelConsumer


def detect_conflicts(
    normalized: dict,
    pattern_id: str,
    family_id: str,
    kernel: PatternKernelConsumer,
) -> dict:
    """
    Detect conflicts for the resolved pattern.

    Checks both pattern-level and family-level conflict relationships.

    Returns:
        {"has_conflicts": False, "conflicts": [], "checked_relationships": [...]}
        {"has_conflicts": True, "conflicts": [...], "checked_relationships": [...], "fail_reason": {...}}
    """
    conflicts = []
    checked = []

    # Get conflict relationships for the pattern
    pattern_conflicts = kernel.get_conflicts_for_entity(pattern_id)
    family_conflicts = kernel.get_conflicts_for_entity(family_id)

    all_rels = {}
    for rel in pattern_conflicts + family_conflicts:
        rel_id = rel.get("id", "")
        if rel_id and rel_id not in all_rels:
            all_rels[rel_id] = rel

    # Check adjacencies from condition for potential conflicts
    adjacencies = normalized.get("adjacencies", [])

    for rel_id, rel in all_rels.items():
        checked.append(rel_id)

        source = rel.get("source", {})
        target = rel.get("target", {})
        src_id = source.get("id", "") if isinstance(source, dict) else str(source)
        tgt_id = target.get("id", "") if isinstance(target, dict) else str(target)

        # Determine the "other" entity in the conflict
        other_id = tgt_id if src_id in (pattern_id, family_id) else src_id

        # A conflict is relevant if:
        # 1. The pattern/family is involved in the relationship
        # 2. The condition context suggests the conflicting entity may be present
        #    (via adjacencies or interface conditions)
        conflict_record = _build_conflict_record(rel, pattern_id, other_id)
        conflicts.append(conflict_record)

    if conflicts:
        return {
            "has_conflicts": True,
            "conflicts": conflicts,
            "checked_relationships": checked,
            "fail_reason": {
                "code": FAIL_CONFLICT_DETECTED,
                "stage": "conflict_detection",
                "message": f"{len(conflicts)} potential conflict(s) detected",
                "details": {"conflict_count": len(conflicts)},
            },
        }

    return {
        "has_conflicts": False,
        "conflicts": [],
        "checked_relationships": checked,
    }


def _build_conflict_record(relationship: dict, pattern_id: str, other_id: str) -> dict:
    """Build a structured conflict record from a relationship definition."""
    source = relationship.get("source", {})
    target = relationship.get("target", {})
    src_id = source.get("id", "") if isinstance(source, dict) else str(source)
    tgt_id = target.get("id", "") if isinstance(target, dict) else str(target)

    resolution = relationship.get("resolution", {})
    strategy = ""
    if isinstance(resolution, dict):
        strategy = resolution.get("strategy", "")

    return {
        "conflict_id": f"CFT-{uuid.uuid4().hex[:12]}",
        "relationship_id": relationship.get("id", ""),
        "source_id": src_id,
        "target_id": tgt_id,
        "severity": relationship.get("severity", "warning"),
        "description": relationship.get("description", ""),
        "resolution_strategy": strategy,
    }
