"""
Receipt Writer — Pipeline Execution Receipts
Writes JSON receipts for each pipeline stage result.

Receipt families:
  extraction_pass / extraction_partial / extraction_halt / extraction_fail
  assembly_resolution_pass / assembly_resolution_partial / assembly_resolution_halt
  constraint_pass / constraint_partial / constraint_halt
  guaranteed_detail_pass / guaranteed_detail_partial / guaranteed_detail_halt
"""

import json
import os
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


RECEIPT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "receipts", "pipeline"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_receipt(family: str, data: dict[str, Any]) -> str:
    """Write a receipt JSON file and return the file path."""
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    receipt_id = f"RCPT-{family.upper()}-{uuid4().hex[:8].upper()}"
    data["receipt_id"] = receipt_id
    data["receipt_family"] = family
    data["emitted_at_utc"] = utc_now()

    filename = f"{receipt_id}.json"
    path = os.path.join(RECEIPT_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    return path


def write_extraction_receipt(extraction_result: dict) -> str:
    """Write extraction receipt based on status."""
    status = extraction_result.get("extraction_status", "failed")
    family_map = {
        "extracted": "extraction_pass",
        "partial": "extraction_partial",
        "halted": "extraction_halt",
        "failed": "extraction_fail",
        "evidence_only": "extraction_evidence_only",
    }
    family = family_map.get(status, "extraction_fail")
    return _write_receipt(family, {
        "extraction_id": extraction_result.get("extraction_id"),
        "ingest_job_id": extraction_result.get("ingest_job_id"),
        "file_type": extraction_result.get("file_type"),
        "extraction_status": status,
        "entity_count": extraction_result.get("entity_count", 0),
        "halt_reason": extraction_result.get("halt_reason"),
    })


def write_resolution_receipt(resolution_result: dict) -> str:
    """Write assembly resolution receipt."""
    status = resolution_result.get("resolution_status", "HALTED")
    family_map = {
        "RESOLVED": "assembly_resolution_pass",
        "NO_MATCH": "assembly_resolution_halt",
        "HALTED": "assembly_resolution_halt",
    }
    family = family_map.get(status, "assembly_resolution_halt")
    return _write_receipt(family, {
        "resolution_id": resolution_result.get("resolution_id"),
        "candidate_id": resolution_result.get("candidate_id"),
        "resolved_detail_id": resolution_result.get("resolved_detail_id"),
        "resolution_status": status,
        "source_mode": resolution_result.get("source_mode"),
        "confidence": resolution_result.get("confidence"),
    })


def write_constraint_receipt(constraint_result: dict) -> str:
    """Write constraint evaluation receipt."""
    action = constraint_result.get("aggregate_action", "BLOCK")
    family_map = {
        "PASS": "constraint_pass",
        "WARN": "constraint_partial",
        "BLOCK": "constraint_halt",
        "REQUIRE_HUMAN_STAMP": "constraint_halt",
        "DEFER_FOR_MISSING_EVIDENCE": "constraint_partial",
    }
    family = family_map.get(action, "constraint_halt")
    return _write_receipt(family, {
        "aggregate_action": action,
        "aggregate_severity": constraint_result.get("aggregate_severity"),
        "decision_count": constraint_result.get("decision_count", 0),
        "halt_decisions": constraint_result.get("halt_decisions", []),
    })


def write_guaranteed_detail_receipt(guaranteed_result: dict) -> str:
    """Write guaranteed detail engine receipt."""
    state = guaranteed_result.get("guarantee_state", "BLOCKED_HALT")
    family_map = {
        "GUARANTEED_PASS": "guaranteed_detail_pass",
        "PROVISIONAL_PARTIAL": "guaranteed_detail_partial",
        "BLOCKED_HALT": "guaranteed_detail_halt",
    }
    family = family_map.get(state, "guaranteed_detail_halt")
    return _write_receipt(family, {
        "result_id": guaranteed_result.get("result_id"),
        "detail_id": guaranteed_result.get("detail_id"),
        "guarantee_state": state,
        "constraint_action": guaranteed_result.get("constraint_action"),
        "source_mode": guaranteed_result.get("source_mode"),
        "confidence": guaranteed_result.get("confidence"),
        "reason_summary": guaranteed_result.get("reason_summary"),
    })


def write_pipeline_receipt(pipeline_result: dict) -> str:
    """Write a full pipeline execution receipt."""
    guaranteed = pipeline_result.get("guaranteed_detail", {})
    return _write_receipt("pipeline_execution", {
        "pipeline_id": pipeline_result.get("pipeline_id"),
        "ingest_job_id": pipeline_result.get("ingest_job_id"),
        "pipeline_status": pipeline_result.get("pipeline_status"),
        "guarantee_state": guaranteed.get("guarantee_state"),
        "detail_id": guaranteed.get("detail_id"),
        "source_mode": guaranteed.get("source_mode"),
        "started_at_utc": pipeline_result.get("started_at_utc"),
        "completed_at_utc": pipeline_result.get("completed_at_utc"),
    })
