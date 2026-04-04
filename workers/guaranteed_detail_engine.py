"""
Guaranteed Detail Engine — Wave 9
Construction OS — Final result layer

Produces the guaranteed detail result by combining:
  - assembly_resolution_result (from assembly_resolver)
  - constraint_evaluator result (from constraint_evaluator)

Guarantee states:
  GUARANTEED_PASS     — constraint PASS + resolution RESOLVED
  PROVISIONAL_PARTIAL — constraint WARN, resolution partial, or DEMO_SEED source
  BLOCKED_HALT        — constraint BLOCK, resolution HALTED, or NO_MATCH

Fail-closed: unknown states → BLOCKED_HALT.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Guarantee state determination
# ---------------------------------------------------------------------------

def _determine_guarantee_state(
    resolution_status: str,
    source_mode: str,
    constraint_decision: str,
    constraint_action: str,
) -> str:
    """Determine the guarantee state from upstream signals.

    Rules (evaluated in order — first match wins):
      1. BLOCKED_HALT if constraint HALT or resolution HALTED or NO_MATCH
      2. PROVISIONAL_PARTIAL if constraint PARTIAL, or source DEMO_SEED,
         or constraint_action is WARN
      3. GUARANTEED_PASS if constraint PASS and resolution RESOLVED
      4. BLOCKED_HALT (fail-closed default)
    """
    # --- Blocking conditions ---
    if constraint_decision == "HALT":
        return "BLOCKED_HALT"
    if constraint_action in ("BLOCK", "REQUIRE_HUMAN_STAMP"):
        return "BLOCKED_HALT"
    if resolution_status == "HALTED":
        return "BLOCKED_HALT"
    if resolution_status == "NO_MATCH":
        return "BLOCKED_HALT"

    # --- Provisional conditions ---
    if constraint_decision == "PARTIAL":
        return "PROVISIONAL_PARTIAL"
    if constraint_action == "WARN":
        return "PROVISIONAL_PARTIAL"
    if constraint_action == "DEFER_FOR_MISSING_EVIDENCE":
        return "PROVISIONAL_PARTIAL"
    if source_mode == "DEMO_SEED":
        return "PROVISIONAL_PARTIAL"

    # --- Full pass ---
    if constraint_decision == "PASS" and resolution_status == "RESOLVED":
        return "GUARANTEED_PASS"

    # --- Fail-closed default ---
    return "BLOCKED_HALT"


def _build_reason_summary(
    guarantee_state: str,
    resolution_result: dict,
    constraint_result: dict,
) -> str:
    """Build a human-readable reason summary explaining the guarantee state."""
    resolution_status = resolution_result.get("resolution_status", "")
    source_mode = resolution_result.get("source_mode", "")
    resolution_basis = resolution_result.get("resolution_basis", "")
    constraint_decision = constraint_result.get("decision", "")
    constraint_action = constraint_result.get("constraint_action", "")

    parts: list[str] = []

    if guarantee_state == "GUARANTEED_PASS":
        parts.append("Detail admitted with full guarantee.")
        parts.append(f"Resolution: {resolution_status} via {source_mode}.")
        parts.append(f"Constraint evaluation: {constraint_decision}.")
        if resolution_basis:
            parts.append(f"Basis: {resolution_basis}")

    elif guarantee_state == "PROVISIONAL_PARTIAL":
        parts.append("Detail admitted provisionally — manual review recommended.")
        if source_mode == "DEMO_SEED":
            parts.append("Source: demo seed data (not live extraction).")
        if constraint_action == "WARN":
            warn_reasons = constraint_result.get("partial_reasons", [])
            if warn_reasons:
                parts.append(f"Warning: {warn_reasons[0]}")
        parts.append(f"Resolution: {resolution_status}. Constraint: {constraint_decision}.")

    elif guarantee_state == "BLOCKED_HALT":
        parts.append("Detail BLOCKED — cannot be guaranteed.")
        halt_reasons = constraint_result.get("halt_reasons", [])
        if halt_reasons:
            parts.append(f"Halt reason: {halt_reasons[0]}")
        if resolution_status in ("HALTED", "NO_MATCH"):
            parts.append(f"Resolution failed: {resolution_status}.")
            if resolution_basis:
                parts.append(f"Basis: {resolution_basis}")
        parts.append(f"Constraint: {constraint_decision} (action={constraint_action}).")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Main engine
# ---------------------------------------------------------------------------

def produce_guaranteed_result(
    resolution_result: dict,
    constraint_result: dict,
    candidate_id: str | None = None,
    receipt_reference: str | None = None,
) -> dict:
    """Produce the final guaranteed detail result.

    Args:
        resolution_result: dict matching assembly_resolution_result.schema.json
        constraint_result: dict from constraint_evaluator.evaluate_constraints()
        candidate_id: Override candidate_id (defaults to resolution_result's)
        receipt_reference: Optional receipt/audit reference

    Returns:
        dict matching guaranteed_detail_result.schema.json
    """
    # Extract upstream fields
    resolution_id = resolution_result.get("resolution_id", "")
    res_candidate_id = candidate_id or resolution_result.get("candidate_id", "")
    manufacturer_id = resolution_result.get("manufacturer_id", "")
    system_id = resolution_result.get("system_id", "")
    condition_type = resolution_result.get("condition_type", "")
    detail_id = resolution_result.get("resolved_detail_id", "")
    detail_label = resolution_result.get("resolved_detail_label", "")
    resolution_status = resolution_result.get("resolution_status", "")
    source_mode = resolution_result.get("source_mode", "NO_RESULT")
    resolution_confidence = resolution_result.get("confidence", 0.0)

    constraint_decision = constraint_result.get("decision", "HALT")
    constraint_action = constraint_result.get("constraint_action", "BLOCK")
    constraint_severity = constraint_result.get("severity", "CRITICAL")

    # Determine guarantee state
    guarantee_state = _determine_guarantee_state(
        resolution_status=resolution_status,
        source_mode=source_mode,
        constraint_decision=constraint_decision,
        constraint_action=constraint_action,
    )

    # Build reason summary
    reason_summary = _build_reason_summary(
        guarantee_state=guarantee_state,
        resolution_result=resolution_result,
        constraint_result=constraint_result,
    )

    # Confidence: pass through resolution confidence, zero if blocked
    if guarantee_state == "BLOCKED_HALT":
        confidence = 0.0
    elif guarantee_state == "PROVISIONAL_PARTIAL":
        confidence = resolution_confidence * 0.7  # discount for provisional
    else:
        confidence = resolution_confidence

    # Receipt reference
    receipt = receipt_reference or f"RCPT-{uuid.uuid4().hex[:12].upper()}"

    return {
        "result_id": f"GDE-{uuid.uuid4().hex[:12].upper()}",
        "manufacturer_id": manufacturer_id,
        "system_id": system_id,
        "condition_type": condition_type,
        "detail_id": detail_id,
        "detail_label": detail_label,
        "guarantee_state": guarantee_state,
        "constraint_action": constraint_action,
        "constraint_severity": constraint_severity,
        "reason_summary": reason_summary,
        "confidence": round(confidence, 4),
        "source_mode": source_mode,
        "resolution_id": resolution_id,
        "candidate_id": res_candidate_id,
        "receipt_reference": receipt,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
