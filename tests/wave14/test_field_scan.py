"""
Wave 14 — Field Scan Tests.

Tests:
- Invalid scans fail closed
- Uncertain scans return UNKNOWN
- Scanner cannot mutate kernel
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.field_scan.condition_detector import (
    detect_condition_from_manual,
    detect_condition_from_image,
    detect_condition_from_lidar,
    ConditionDetectionError,
)
from runtime.field_scan.material_detector import detect_material_hints
from runtime.field_scan.geometry_estimator import estimate_geometry
from runtime.field_scan.scan_validation import validate_scan_result, validate_scan_batch


def test_invalid_scan_fails_closed():
    """Unsupported condition type fails closed."""
    try:
        detect_condition_from_manual("SKYLIGHT", "test", "evidence-001")
        assert False, "Should have raised ConditionDetectionError"
    except ConditionDetectionError as e:
        assert "Unsupported" in str(e)
    print("  PASS: invalid_scan_fails_closed")


def test_uncertain_scan_returns_unknown():
    """Low-confidence scans return UNKNOWN."""
    result = detect_condition_from_manual(
        "PARAPET", "Maybe parapet", "evidence-002", confidence=0.1
    )
    assert result["detection_status"] == "UNKNOWN"
    assert result["advisory_only"] is True
    print("  PASS: uncertain_scan_returns_unknown")


def test_scanner_advisory_only():
    """All scanner outputs must be advisory_only=True."""
    manual = detect_condition_from_manual("DRAIN", "Drain", "ev-001")
    image = detect_condition_from_image("img-001")
    lidar = detect_condition_from_lidar("lid-001")

    for result in [manual, image, lidar]:
        assert result["advisory_only"] is True, "Scanner output must be advisory_only"
    print("  PASS: scanner_advisory_only")


def test_image_detection_returns_unknown():
    """Image detection stub returns UNKNOWN (not yet implemented)."""
    result = detect_condition_from_image("image-ref-001")
    assert result["detection_status"] == "UNKNOWN"
    assert result["confidence"] == 0.0
    print("  PASS: image_detection_returns_unknown")


def test_lidar_detection_returns_unknown():
    """Lidar detection stub returns UNKNOWN (not yet implemented)."""
    result = detect_condition_from_lidar("lidar-ref-001")
    assert result["detection_status"] == "UNKNOWN"
    assert result["confidence"] == 0.0
    print("  PASS: lidar_detection_returns_unknown")


def test_material_detection():
    """Material detector identifies known materials from observation."""
    result = detect_material_hints("EPDM membrane visible on parapet", "ev-001")
    assert "EPDM" in result["detected_materials"]
    assert result["advisory_only"] is True
    print("  PASS: material_detection")


def test_material_detection_unknown():
    """Unknown material observations return UNKNOWN."""
    result = detect_material_hints("Some unknown material type", "ev-002")
    assert result["status"] == "UNKNOWN"
    assert result["advisory_only"] is True
    print("  PASS: material_detection_unknown")


def test_geometry_estimation():
    """Geometry estimator produces valid estimates."""
    result = estimate_geometry({"parapet_height": 24, "drain_diameter": 6}, "ev-001")
    assert result["status"] == "ESTIMATED"
    assert result["advisory_only"] is True
    assert result["estimated_parameters"]["parapet_height"] == 24.0
    print("  PASS: geometry_estimation")


def test_scan_validation():
    """Scan results pass validation when properly formed."""
    result = detect_condition_from_manual("PARAPET", "Parapet", "ev-001")
    errors = validate_scan_result(result)
    assert errors == [], f"Validation errors: {errors}"
    print("  PASS: scan_validation")


def test_scan_validation_catches_non_advisory():
    """Validation catches results without advisory_only flag."""
    bad_result = {"confidence": 0.5, "evidence_refs": ["ev-001"], "advisory_only": False}
    errors = validate_scan_result(bad_result)
    assert any("advisory_only" in e for e in errors)
    print("  PASS: scan_validation_catches_non_advisory")


def run_all():
    print("Field Scan Tests:")
    test_invalid_scan_fails_closed()
    test_uncertain_scan_returns_unknown()
    test_scanner_advisory_only()
    test_image_detection_returns_unknown()
    test_lidar_detection_returns_unknown()
    test_material_detection()
    test_material_detection_unknown()
    test_geometry_estimation()
    test_scan_validation()
    test_scan_validation_catches_non_advisory()
    print("  All field scan tests passed.\n")


if __name__ == "__main__":
    run_all()
