"""
Resolution Pipeline — Main Orchestrator.

Executes the full ConditionSignature → ResolutionResult pipeline:
  intake → normalization → family classification → pattern resolution →
  variant selection → constraint enforcement → conflict detection → scoring

Fail-closed at every stage. Deterministic. Advisory only.
"""

import uuid
from datetime import datetime, timezone

from engine.config import (
    STATUS_RESOLVED,
    STATUS_UNRESOLVED,
    STATUS_BLOCKED,
    STATUS_CONFLICT,
    STAGE_PASS,
    STAGE_FAIL,
    STAGE_SKIP,
    FAIL_INTERNAL_ERROR,
)
from engine.condition_intake import validate_condition_signature
from engine.normalizer import normalize_condition
from engine.family_classifier import classify_family
from engine.pattern_resolver import resolve_pattern
from engine.variant_selector import select_variant
from engine.constraint_engine import enforce_constraints
from engine.conflict_detector import detect_conflicts
from engine.scoring_engine import score_resolution
from contracts.pattern_kernel_consumer import PatternKernelConsumer


def resolve(condition: dict, kernel: PatternKernelConsumer) -> dict:
    """
    Execute the full resolution pipeline.

    Args:
        condition: A ConditionSignature dict
        kernel: A loaded PatternKernelConsumer instance

    Returns:
        A ResolutionResult dict conforming to resolution_result.schema.json
    """
    result_id = f"RES-{uuid.uuid4().hex[:16]}"
    timestamp = datetime.now(timezone.utc).isoformat()
    fail_reasons = []
    stages = {}

    # ── Stage 1: Intake ──
    intake_result = validate_condition_signature(condition)
    if not intake_result["valid"]:
        fail_reasons.append(intake_result["fail_reason"])
        stages["intake"] = {"status": STAGE_FAIL, "detail": intake_result["fail_reason"]["message"]}
        return _build_result(
            result_id, timestamp, condition.get("condition_id", "unknown"),
            STATUS_UNRESOLVED, fail_reasons, stages,
        )
    stages["intake"] = {"status": STAGE_PASS}

    # ── Stage 2: Normalization ──
    norm_result = normalize_condition(condition)
    if not norm_result["valid"]:
        fail_reasons.append(norm_result["fail_reason"])
        stages["normalization"] = {"status": STAGE_FAIL, "detail": norm_result["fail_reason"]["message"]}
        return _build_result(
            result_id, timestamp, condition["condition_id"],
            STATUS_UNRESOLVED, fail_reasons, stages,
        )
    normalized = norm_result["normalized"]
    stages["normalization"] = {"status": STAGE_PASS}

    # ── Stage 3: Family Classification ──
    family_result = classify_family(normalized, kernel)
    if not family_result["matched"]:
        fail_reasons.append(family_result["fail_reason"])
        stages["family_classification"] = {
            "status": STAGE_FAIL,
            "detail": family_result["fail_reason"]["message"],
        }
        return _build_result(
            result_id, timestamp, normalized["condition_id"],
            STATUS_BLOCKED if family_result["fail_reason"]["code"] == "AMBIGUOUS_FAMILY" else STATUS_UNRESOLVED,
            fail_reasons, stages,
        )
    family_id = family_result["family_id"]
    stages["family_classification"] = {
        "status": STAGE_PASS,
        "candidates_in": len(kernel.get_all_families()),
        "candidates_out": 1,
    }

    # ── Stage 4: Pattern Resolution ──
    pattern_result = resolve_pattern(normalized, family_id, kernel)
    if not pattern_result["matched"]:
        fail_reasons.append(pattern_result["fail_reason"])
        code = pattern_result["fail_reason"]["code"]
        stages["pattern_resolution"] = {
            "status": STAGE_FAIL,
            "candidates_in": len(pattern_result.get("candidates", [])),
            "candidates_out": 0,
            "detail": pattern_result["fail_reason"]["message"],
        }
        return _build_result(
            result_id, timestamp, normalized["condition_id"],
            STATUS_BLOCKED if code == "AMBIGUOUS_PATTERN" else STATUS_UNRESOLVED,
            fail_reasons, stages,
            pattern_family_id=family_id,
        )
    pattern_id = pattern_result["pattern_id"]
    stages["pattern_resolution"] = {
        "status": STAGE_PASS,
        "candidates_in": len(pattern_result.get("candidates", [])),
        "candidates_out": 1,
    }

    # ── Stage 5: Variant Selection ──
    variant_result = select_variant(normalized, pattern_id, kernel)
    variant_id = None
    if not variant_result["matched"]:
        fail_reasons.append(variant_result["fail_reason"])
        stages["variant_selection"] = {
            "status": STAGE_FAIL,
            "candidates_in": len(variant_result.get("candidates", [])),
            "candidates_out": 0,
            "detail": variant_result["fail_reason"]["message"],
        }
        return _build_result(
            result_id, timestamp, normalized["condition_id"],
            STATUS_BLOCKED if variant_result["fail_reason"]["code"] == "AMBIGUOUS_VARIANT" else STATUS_UNRESOLVED,
            fail_reasons, stages,
            pattern_family_id=family_id,
            pattern_id=pattern_id,
        )
    variant_id = variant_result["variant_id"]
    stages["variant_selection"] = {
        "status": STAGE_PASS,
        "candidates_in": len(variant_result.get("candidates", [])),
        "candidates_out": 1,
    }

    # ── Stage 6: Constraint Enforcement ──
    constraint_result = enforce_constraints(normalized, pattern_id, variant_id, family_id, kernel)
    if not constraint_result["passed"]:
        fail_reasons.append(constraint_result["fail_reason"])
        stages["constraint_enforcement"] = {
            "status": STAGE_FAIL,
            "detail": constraint_result["fail_reason"]["message"],
        }
        return _build_result(
            result_id, timestamp, normalized["condition_id"],
            STATUS_BLOCKED, fail_reasons, stages,
            pattern_family_id=family_id,
            pattern_id=pattern_id,
            variant_id=variant_id,
            constraint_violations=constraint_result.get("violations", []),
        )
    stages["constraint_enforcement"] = {"status": STAGE_PASS}

    # ── Stage 7: Conflict Detection ──
    conflict_result = detect_conflicts(normalized, pattern_id, family_id, kernel)
    if conflict_result["has_conflicts"]:
        fail_reasons.append(conflict_result["fail_reason"])
        stages["conflict_detection"] = {
            "status": STAGE_FAIL,
            "detail": conflict_result["fail_reason"]["message"],
        }
        return _build_result(
            result_id, timestamp, normalized["condition_id"],
            STATUS_CONFLICT, fail_reasons, stages,
            pattern_family_id=family_id,
            pattern_id=pattern_id,
            variant_id=variant_id,
            conflicts=conflict_result.get("conflicts", []),
        )
    stages["conflict_detection"] = {"status": STAGE_PASS}

    # ── Stage 8: Scoring ──
    score_result = score_resolution(
        family_result, pattern_result, variant_result,
        constraint_result, conflict_result,
    )
    if not score_result["scored"]:
        fail_reasons.append(score_result["fail_reason"])
        stages["scoring"] = {
            "status": STAGE_FAIL,
            "detail": score_result["fail_reason"]["message"],
        }
        return _build_result(
            result_id, timestamp, normalized["condition_id"],
            STATUS_RESOLVED, fail_reasons, stages,
            pattern_family_id=family_id,
            pattern_id=pattern_id,
            variant_id=variant_id,
            score=None,
        )
    stages["scoring"] = {"status": STAGE_PASS}

    # ── Resolve artifact intent ──
    artifact_intent_id = _resolve_artifact_intent(pattern_id, kernel)

    # ── All stages passed — RESOLVED ──
    return _build_result(
        result_id, timestamp, normalized["condition_id"],
        STATUS_RESOLVED, fail_reasons, stages,
        pattern_family_id=family_id,
        pattern_id=pattern_id,
        variant_id=variant_id,
        artifact_intent_id=artifact_intent_id,
        score=score_result["score"],
    )


def _resolve_artifact_intent(pattern_id: str, kernel: PatternKernelConsumer) -> str | None:
    """Attempt to find a matching artifact intent for the pattern."""
    intents = kernel.get_artifact_intents_for_pattern(pattern_id)
    if intents and len(intents) == 1:
        return intents[0].get("id")
    elif intents and len(intents) > 1:
        # Return the first one — deterministic since kernel is ordered
        return intents[0].get("id")
    return None


def _build_result(
    result_id: str,
    timestamp: str,
    condition_id: str,
    status: str,
    fail_reasons: list,
    stages: dict,
    pattern_family_id: str = None,
    pattern_id: str = None,
    variant_id: str = None,
    artifact_intent_id: str = None,
    score: dict = None,
    conflicts: list = None,
    constraint_violations: list = None,
) -> dict:
    """Build a ResolutionResult conforming to the schema."""
    # Fill in missing stages as SKIP
    all_stage_names = [
        "intake", "normalization", "family_classification",
        "pattern_resolution", "variant_selection",
        "constraint_enforcement", "conflict_detection", "scoring",
    ]
    for sn in all_stage_names:
        if sn not in stages:
            stages[sn] = {"status": STAGE_SKIP}

    return {
        "result_id": result_id,
        "schema_version": "1.0.0",
        "timestamp_utc": timestamp,
        "condition_id": condition_id,
        "status": status,
        "pattern_family_id": pattern_family_id,
        "pattern_id": pattern_id,
        "variant_id": variant_id,
        "artifact_intent_id": artifact_intent_id,
        "fail_reasons": fail_reasons,
        "conflicts": conflicts or [],
        "constraint_violations": constraint_violations or [],
        "score": score,
        "resolution_stages": stages,
        "correlation_refs": [],
        "source_repo": "Construction_ALEXANDER_Engine",
    }
