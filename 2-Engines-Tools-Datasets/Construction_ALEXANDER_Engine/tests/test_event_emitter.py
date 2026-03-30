"""Unit tests for Cognitive Bus event emitter."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.event_emitter import (
    build_proposal_event,
    build_observation_event,
    build_anomaly_event,
)


def _resolution_result(**overrides):
    base = {
        "result_id": "RES-001",
        "condition_id": "COND-001",
        "status": "RESOLVED",
        "pattern_family_id": "DNA-CONSTR-FAM-EDGE-001-R1",
        "pattern_id": "DNA-CONSTR-PAT-EDGE-DRIP-010-R1",
        "variant_id": "CHEM-CONSTR-VAR-DRIPMECH-101-R1",
        "artifact_intent_id": "COLOR-CONSTR-ART-EDGESHOP-001-R1",
        "fail_reasons": [],
        "conflicts": [],
        "score": {"total_score": 0.95, "breakdown": {}},
        "correlation_refs": ["corr-001"],
    }
    base.update(overrides)
    return base


def test_proposal_event_structure():
    event = build_proposal_event(_resolution_result())
    assert event["event_class"] == "Proposal"
    assert event["schema_version"] == "0.1"
    assert event["source_component"] == "Construction_ALEXANDER_Engine"
    assert event["source_repo"] == "Construction_ALEXANDER_Engine"
    assert "event_id" in event
    assert "timestamp" in event
    assert event["payload"]["advisory_class"] == "proposal"
    assert event["payload"]["status"] == "RESOLVED"
    assert event["payload"]["condition_id"] == "COND-001"


def test_proposal_event_type_variant():
    event = build_proposal_event(_resolution_result())
    assert event["event_type"] == "variant_selection_proposal"


def test_proposal_event_type_pattern_only():
    event = build_proposal_event(_resolution_result(variant_id=None))
    assert event["event_type"] == "pattern_resolution_proposal"


def test_observation_event_structure():
    event = build_observation_event(_resolution_result())
    assert event["event_class"] == "Observation"
    assert event["schema_version"] == "0.1"
    assert event["source_component"] == "Construction_ALEXANDER_Engine"
    assert event["payload"]["advisory_class"] == "observation"


def test_observation_conflict_type():
    event = build_observation_event(_resolution_result(status="CONFLICT"))
    assert event["payload"]["observation_type"] == "conflict"


def test_observation_missing_truth_type():
    event = build_observation_event(_resolution_result(
        status="UNRESOLVED",
        fail_reasons=[{"code": "MISSING_TRUTH", "stage": "family_classification", "message": "missing"}],
    ))
    assert event["payload"]["observation_type"] == "missing_truth"


def test_anomaly_event_structure():
    event = build_anomaly_event(
        condition_id="COND-001",
        anomaly_detail="Unexpected condition shape",
        affected_entities=["ENT-001"],
        severity="warning",
        correlation_refs=["corr-001"],
    )
    assert event["event_class"] == "Observation"
    assert event["event_type"] == "anomaly_detected"
    assert event["payload"]["observation_type"] == "anomaly"
    assert event["payload"]["advisory_class"] == "observation"
    assert event["payload"]["severity"] == "warning"


def test_event_includes_correlation_refs():
    event = build_proposal_event(_resolution_result(correlation_refs=["ref-A", "ref-B"]))
    assert event["payload"]["correlation_refs"] == ["ref-A", "ref-B"]


def test_event_id_unique():
    e1 = build_proposal_event(_resolution_result())
    e2 = build_proposal_event(_resolution_result())
    assert e1["event_id"] != e2["event_id"]


def test_proposal_never_execution_class():
    event = build_proposal_event(_resolution_result())
    assert event["payload"]["advisory_class"] == "proposal"
    assert event["event_class"] != "ExternallyValidatedEvent"


def test_observation_never_execution_class():
    event = build_observation_event(_resolution_result())
    assert event["payload"]["advisory_class"] == "observation"
    assert event["event_class"] != "ExternallyValidatedEvent"
