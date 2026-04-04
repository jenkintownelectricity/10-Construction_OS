"""
Pipeline Orchestrator — Guaranteed Detail Engine
Coordinates the full evidence-to-detail execution bridge.

Flow:
  ingest_job claimed
  → file dispatched
  → geometry extracted (DXF path)
  → ownership classified
  → condition detected
  → assembly candidate generated
  → assembly resolved
  → constraint evaluated
  → guaranteed detail result produced
  → Supabase writeback
  → receipt emitted

This module wires all pipeline stages together.
Each stage returns a dict matching its schema contract.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

# Add repo root to path for imports
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from workers.file_dispatcher import dispatch
from workers.ownership_classifier import classify_entities
from workers.condition_bridge import bridge_to_condition
from workers.assembly_candidate_generator import generate_candidate
from workers.assembly_resolver import resolve_assembly
from workers.constraint_evaluator import evaluate_constraints
from workers.guaranteed_detail_engine import produce_guaranteed_result


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_pipeline(
    file_path: str,
    file_type: str,
    manufacturer_id: str = "d0000000-0000-0000-0000-000000000001",
    system_id: str = "f0000000-0000-0000-0000-000000000001",
    ingest_job_id: str | None = None,
) -> dict[str, Any]:
    """
    Run the full evidence-to-detail pipeline on a local file.

    Returns a complete pipeline result dict with all intermediate results.
    Fail-closed: any unhandled error produces a BLOCKED_HALT guaranteed result.
    """
    job_id = ingest_job_id or str(uuid4())
    pipeline_id = f"PL-{uuid4().hex[:8].upper()}"
    results: dict[str, Any] = {
        "pipeline_id": pipeline_id,
        "ingest_job_id": job_id,
        "started_at_utc": utc_now(),
    }

    try:
        # Wave 1-2: Dispatch and extract
        extraction = dispatch(file_path, ingest_job_id=job_id)
        results["extraction"] = extraction

        if extraction.get("extraction_status") in ("halted", "failed"):
            return _halt_result(results, extraction.get("halt_reason", "Extraction failed"))

        if extraction.get("extraction_status") == "evidence_only":
            return _evidence_only_result(results)

        # Wave 4: Ownership classification
        ownership = classify_entities(extraction)
        results["ownership"] = ownership

        # Wave 5: Condition detection
        condition = bridge_to_condition(
            ownership_classification=ownership,
            extraction_id=extraction.get("extraction_id", ""),
        )
        results["condition"] = condition

        if condition.get("support_state") in ("NO_SOURCE", "UNSUPPORTED_CONDITION"):
            return _halt_result(results, f"Condition: {condition.get('support_state')}")

        # Wave 6: Assembly candidate
        candidate = generate_candidate(
            condition_result=condition,
            manufacturer_id=manufacturer_id,
            system_id=system_id,
        )
        results["candidate"] = candidate

        if candidate.get("status") == "HALT":
            return _halt_result(results, candidate.get("halt_reason", "No assembly candidate"))

        # Wave 7: Assembly resolution
        resolution = resolve_assembly(candidate=candidate)
        results["resolution"] = resolution

        # Wave 8: Constraint evaluation
        constraint = evaluate_constraints(
            resolution_result=resolution,
            candidate=candidate,
        )
        results["constraint"] = constraint

        # Wave 9: Guaranteed detail result
        guaranteed = produce_guaranteed_result(
            resolution_result=resolution,
            constraint_result=constraint,
            candidate_id=candidate.get("candidate_id"),
        )
        results["guaranteed_detail"] = guaranteed
        results["completed_at_utc"] = utc_now()
        results["pipeline_status"] = "completed"

        return results

    except Exception as e:
        results["error"] = str(e)
        results["pipeline_status"] = "failed"
        results["completed_at_utc"] = utc_now()
        # Fail-closed: produce BLOCKED_HALT
        results["guaranteed_detail"] = {
            "result_id": f"GDR-{uuid4().hex[:8].upper()}",
            "manufacturer_id": manufacturer_id,
            "system_id": system_id,
            "condition_type": "unknown",
            "guarantee_state": "BLOCKED_HALT",
            "constraint_action": "BLOCK",
            "constraint_severity": "CRITICAL",
            "reason_summary": f"Pipeline failure: {e}",
            "confidence": 0.0,
            "source_mode": "NO_RESULT",
            "generated_at_utc": utc_now(),
        }
        return results


def _halt_result(results: dict, reason: str) -> dict:
    results["pipeline_status"] = "halted"
    results["halt_reason"] = reason
    results["completed_at_utc"] = utc_now()
    results["guaranteed_detail"] = {
        "result_id": f"GDR-{uuid4().hex[:8].upper()}",
        "manufacturer_id": results.get("ingest_job_id", ""),
        "system_id": "",
        "condition_type": results.get("condition", {}).get("condition_type", "unknown"),
        "guarantee_state": "BLOCKED_HALT",
        "constraint_action": "BLOCK",
        "constraint_severity": "HIGH",
        "reason_summary": reason,
        "confidence": 0.0,
        "source_mode": "NO_RESULT",
        "generated_at_utc": utc_now(),
    }
    return results


def _evidence_only_result(results: dict) -> dict:
    results["pipeline_status"] = "evidence_only"
    results["completed_at_utc"] = utc_now()
    results["guaranteed_detail"] = {
        "result_id": f"GDR-{uuid4().hex[:8].upper()}",
        "manufacturer_id": "",
        "system_id": "",
        "condition_type": "none",
        "guarantee_state": "BLOCKED_HALT",
        "constraint_action": "DEFER_FOR_MISSING_EVIDENCE",
        "constraint_severity": "INFO",
        "reason_summary": "Non-geometry evidence file. Stored as evidence record only.",
        "confidence": 0.0,
        "source_mode": "NO_RESULT",
        "generated_at_utc": utc_now(),
    }
    return results


# --- CLI entry point ---

def main():
    """Run pipeline on a local file."""
    if len(sys.argv) < 2:
        print("Usage: python -m workers.pipeline_orchestrator <file_path> [file_type] [manufacturer_id] [system_id]")
        sys.exit(1)

    file_path = sys.argv[1]
    file_type = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(file_path)[1].lstrip(".")
    manufacturer_id = sys.argv[3] if len(sys.argv) > 3 else "d0000000-0000-0000-0000-000000000001"
    system_id = sys.argv[4] if len(sys.argv) > 4 else "f0000000-0000-0000-0000-000000000001"

    result = run_pipeline(file_path, file_type, manufacturer_id, system_id)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
