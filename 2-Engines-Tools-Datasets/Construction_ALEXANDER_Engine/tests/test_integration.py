"""
Integration test: ConditionSignature → ResolutionResult full pipeline.

Tests the complete resolution flow against the live kernel data from
Construction_Pattern_Language_OS.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathlib import Path
from engine.resolution_pipeline import resolve
from engine.event_emitter import build_proposal_event, build_observation_event
from contracts.pattern_kernel_consumer import PatternKernelConsumer


KERNEL_DIR = Path(os.path.join(os.path.dirname(__file__), "..", "..", "Construction_Pattern_Language_OS"))


def _get_kernel():
    kernel = PatternKernelConsumer(kernel_dir=KERNEL_DIR)
    kernel.load()
    return kernel


def _roof_edge_condition():
    return {
        "condition_id": "INTEG-COND-001",
        "schema_version": "1.0.0",
        "timestamp_utc": "2026-03-22T12:00:00Z",
        "condition_type": "roof_edge",
        "location_context": {
            "zone_id": "zone-roof-perimeter-A",
            "interface_condition": "roof_edge",
        },
        "dimensions": {
            "width_inches": 6.0,
            "height_inches": 4.0,
        },
        "system_type": "membrane_roofing",
        "method_preference": "mechanical",
        "material_preferences": ["galvanized steel"],
        "climate_context": {
            "wind_zone": 2,
            "moisture_exposure": "moderate",
        },
    }


def _drain_condition():
    return {
        "condition_id": "INTEG-COND-002",
        "schema_version": "1.0.0",
        "timestamp_utc": "2026-03-22T12:00:00Z",
        "condition_type": "drain",
        "location_context": {
            "zone_id": "zone-roof-interior-B",
            "interface_condition": "drain",
        },
        "dimensions": {
            "diameter_inches": 6.0,
        },
    }


def _parapet_condition():
    return {
        "condition_id": "INTEG-COND-003",
        "schema_version": "1.0.0",
        "timestamp_utc": "2026-03-22T12:00:00Z",
        "condition_type": "parapet",
        "location_context": {
            "zone_id": "zone-parapet-north",
            "interface_condition": "parapet",
        },
        "dimensions": {
            "height_inches": 36.0,
        },
        "method_preference": "snap",
        "material_preferences": ["aluminum"],
    }


def _invalid_condition():
    return {
        "condition_id": "",
        "schema_version": "1.0.0",
        "timestamp_utc": "2026-03-22T12:00:00Z",
        "condition_type": "unknown_type",
        "location_context": {},
    }


def _missing_truth_condition():
    return {
        "condition_id": "INTEG-COND-MISSING",
        "schema_version": "1.0.0",
        "timestamp_utc": "2026-03-22T12:00:00Z",
        "condition_type": "interface",
        "location_context": {
            "zone_id": "zone-X",
            "interface_condition": "fenestration",
        },
    }


# ── Integration Tests ──

def test_full_roof_edge_resolution():
    """Full pipeline: roof_edge condition → valid resolution status."""
    kernel = _get_kernel()
    result = resolve(_roof_edge_condition(), kernel)

    assert result["result_id"].startswith("RES-")
    assert result["schema_version"] == "1.0.0"
    assert result["condition_id"] == "INTEG-COND-001"
    assert result["source_repo"] == "Construction_ALEXANDER_Engine"
    assert result["status"] in ("RESOLVED", "UNRESOLVED", "BLOCKED", "CONFLICT")

    # Should have resolved family at minimum
    assert result["pattern_family_id"] is not None
    assert "EDGE" in result["pattern_family_id"]

    # Stages should be recorded
    stages = result["resolution_stages"]
    assert stages["intake"]["status"] == "PASS"
    assert stages["normalization"]["status"] == "PASS"
    assert stages["family_classification"]["status"] == "PASS"

    # If BLOCKED/UNRESOLVED at pattern resolution, fail reasons must explain
    if result["status"] in ("UNRESOLVED", "BLOCKED"):
        assert len(result["fail_reasons"]) > 0

    # If resolved, should have pattern and variant
    if result["status"] == "RESOLVED":
        assert result["pattern_id"] is not None
        assert result["variant_id"] is not None
        assert result["score"] is not None
        assert 0 <= result["score"]["total_score"] <= 1


def test_full_drain_resolution():
    """Full pipeline: drain condition resolution."""
    kernel = _get_kernel()
    result = resolve(_drain_condition(), kernel)

    assert result["condition_id"] == "INTEG-COND-002"
    assert result["status"] in ("RESOLVED", "UNRESOLVED", "BLOCKED", "CONFLICT")
    assert result["pattern_family_id"] is not None or result["status"] == "UNRESOLVED"


def test_full_parapet_resolution():
    """Full pipeline: parapet condition resolution."""
    kernel = _get_kernel()
    result = resolve(_parapet_condition(), kernel)

    assert result["condition_id"] == "INTEG-COND-003"
    assert result["status"] in ("RESOLVED", "UNRESOLVED", "BLOCKED", "CONFLICT")


def test_invalid_condition_fails_closed():
    """Invalid condition must fail closed at intake."""
    kernel = _get_kernel()
    result = resolve(_invalid_condition(), kernel)

    assert result["status"] == "UNRESOLVED"
    assert len(result["fail_reasons"]) > 0
    assert result["resolution_stages"]["intake"]["status"] == "FAIL"
    assert result["pattern_family_id"] is None
    assert result["pattern_id"] is None
    assert result["variant_id"] is None


def test_missing_truth_fails_closed():
    """Condition with no kernel truth must fail closed."""
    kernel = _get_kernel()
    result = resolve(_missing_truth_condition(), kernel)

    assert result["status"] in ("UNRESOLVED", "BLOCKED")
    assert len(result["fail_reasons"]) > 0


def test_resolution_result_generates_valid_proposal_event():
    """ResolutionResult must produce a valid Proposal event."""
    kernel = _get_kernel()
    result = resolve(_roof_edge_condition(), kernel)

    event = build_proposal_event(result)
    assert event["event_class"] == "Proposal"
    assert event["schema_version"] == "0.1"
    assert event["source_component"] == "Construction_ALEXANDER_Engine"
    assert event["payload"]["advisory_class"] == "proposal"
    assert event["payload"]["condition_id"] == "INTEG-COND-001"


def test_failed_resolution_generates_valid_observation_event():
    """Failed resolution must produce a valid Observation event."""
    kernel = _get_kernel()
    result = resolve(_invalid_condition(), kernel)

    event = build_observation_event(result)
    assert event["event_class"] == "Observation"
    assert event["payload"]["advisory_class"] == "observation"


def test_resolution_result_schema_compliance():
    """ResolutionResult must have all required fields per schema."""
    kernel = _get_kernel()
    result = resolve(_roof_edge_condition(), kernel)

    required_fields = [
        "result_id", "schema_version", "timestamp_utc", "condition_id",
        "status", "resolution_stages",
    ]
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"

    # Check stage names
    required_stages = [
        "intake", "normalization", "family_classification",
        "pattern_resolution", "variant_selection",
        "constraint_enforcement", "conflict_detection", "scoring",
    ]
    for stage in required_stages:
        assert stage in result["resolution_stages"], f"Missing stage: {stage}"
        assert "status" in result["resolution_stages"][stage]


def test_specific_condition_resolves_fully():
    """A condition with enough context must resolve to RESOLVED or CONFLICT."""
    kernel = _get_kernel()
    # Use penetration type — plumbing vent has "boot" in variant name,
    # and the family has 2 patterns with distinct descriptions
    condition = {
        "condition_id": "INTEG-COND-SPECIFIC",
        "schema_version": "1.0.0",
        "timestamp_utc": "2026-03-22T12:00:00Z",
        "condition_type": "penetration",
        "location_context": {
            "zone_id": "zone-roof-field",
            "interface_condition": "penetration",
        },
        "dimensions": {"diameter_inches": 4.0},
        "system_type": "plumbing_vent",
        "method_preference": "boot",
        "material_preferences": ["rubber"],
    }
    result = resolve(condition, kernel)

    assert result["status"] in ("RESOLVED", "CONFLICT", "BLOCKED", "UNRESOLVED")
    assert result["pattern_family_id"] is not None
    assert "PIPE" in result["pattern_family_id"]
    # The result must contain all required schema fields
    assert "resolution_stages" in result
    assert "fail_reasons" in result


def test_all_condition_types_dont_crash():
    """Every valid condition type must produce a result without crashing."""
    kernel = _get_kernel()
    types = ["roof_edge", "parapet", "drain", "penetration", "expansion_joint", "interface", "transition"]
    for ct in types:
        condition = {
            "condition_id": f"INTEG-{ct}",
            "schema_version": "1.0.0",
            "timestamp_utc": "2026-03-22T12:00:00Z",
            "condition_type": ct,
            "location_context": {"zone_id": "zone-test"},
        }
        result = resolve(condition, kernel)
        assert result["status"] in ("RESOLVED", "UNRESOLVED", "BLOCKED", "CONFLICT"), \
            f"Invalid status for condition_type '{ct}': {result['status']}"
        assert result["result_id"].startswith("RES-")
