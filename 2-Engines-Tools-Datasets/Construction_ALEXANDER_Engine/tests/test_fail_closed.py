"""Unit tests for fail-closed behavior across all stages."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.condition_intake import validate_condition_signature
from engine.normalizer import normalize_condition
from engine.family_classifier import classify_family
from engine.pattern_resolver import resolve_pattern
from engine.variant_selector import select_variant
from engine.constraint_engine import enforce_constraints
from engine.conflict_detector import detect_conflicts
from engine.event_emitter import build_proposal_event, build_anomaly_event, _validate_not_forbidden
from unittest.mock import MagicMock
import pytest


# ── Intake fail-closed ──

def test_intake_rejects_none():
    result = validate_condition_signature(None)
    assert result["valid"] is False


def test_intake_rejects_empty_dict():
    result = validate_condition_signature({})
    assert result["valid"] is False


def test_intake_rejects_list():
    result = validate_condition_signature([])
    assert result["valid"] is False


# ── Normalizer fail-closed ──

def test_normalizer_handles_malformed_input():
    result = normalize_condition({"condition_id": 123, "schema_version": None, "timestamp_utc": "", "condition_type": "", "location_context": None})
    assert result["valid"] is False


# ── Family classifier fail-closed ──

def test_classifier_fails_on_empty_kernel():
    kernel = MagicMock()
    kernel.get_families_by_domain_key = MagicMock(return_value=[])
    result = classify_family({"condition_type": "roof_edge"}, kernel)
    assert result["matched"] is False


def test_classifier_fails_on_unknown_interface():
    kernel = MagicMock()
    kernel.get_families_by_domain_key = MagicMock(return_value=[])
    result = classify_family({"condition_type": "interface", "interface_condition": "unknown_thing"}, kernel)
    assert result["matched"] is False


# ── Pattern resolver fail-closed ──

def test_resolver_fails_on_no_patterns():
    kernel = MagicMock()
    kernel.get_patterns_for_family = MagicMock(return_value=[])
    result = resolve_pattern({}, "FAM-001", kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] == "MISSING_TRUTH"


# ── Variant selector fail-closed ──

def test_selector_fails_on_no_variants():
    kernel = MagicMock()
    kernel.get_variants_for_pattern = MagicMock(return_value=[])
    result = select_variant({}, "PAT-001", kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] == "MISSING_TRUTH"


# ── Constraint engine fail-closed ──

def test_constraint_fails_on_violation():
    kernel = MagicMock()
    kernel.get_constraints_for_pattern = MagicMock(return_value=[{
        "id": "CNS-001",
        "constraint_type": "code",
        "parameters": {"min_drain_size_inches": 4},
    }])
    kernel.get_constraints_for_family = MagicMock(return_value=[])
    result = enforce_constraints(
        {"dimensions": {"diameter_inches": 2}, "material_preferences": [], "manufacturer_refs": [], "climate_context": {}},
        "PAT-001", "VAR-001", "FAM-001", kernel,
    )
    assert result["passed"] is False


# ── Event emitter fail-closed ──

def test_emitter_rejects_forbidden_event_class():
    with pytest.raises(ValueError, match="may NOT emit"):
        _validate_not_forbidden("ExternallyValidatedEvent")


def test_emitter_rejects_unknown_event_class():
    with pytest.raises(ValueError, match="Unknown event class"):
        _validate_not_forbidden("ExecutionCommand")


# ── Conflict detector fail-closed ──

def test_conflict_detector_reports_all_conflicts():
    kernel = MagicMock()
    conflicts = [
        {"id": "R1", "type": "conflict", "source": {"id": "P1"}, "target": {"id": "P2"}, "severity": "critical", "description": "c1", "resolution": {}},
        {"id": "R2", "type": "conflict", "source": {"id": "P1"}, "target": {"id": "P3"}, "severity": "warning", "description": "c2", "resolution": {}},
    ]
    kernel.get_conflicts_for_entity = MagicMock(return_value=conflicts)
    result = detect_conflicts({"adjacencies": []}, "P1", "FAM-001", kernel)
    assert result["has_conflicts"] is True
    assert len(result["conflicts"]) == 2
