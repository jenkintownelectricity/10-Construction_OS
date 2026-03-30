"""
Wave 14 — Variant Generator Tests.

Tests:
- Variant payload validates schema
- Prohibited combinations excluded
- Canonical IDs unchanged
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.detail_variants.variant_generator import (
    generate_variant,
    generate_variant_manifest,
    VariantGenerationError,
    CANONICAL_DETAIL_FAMILIES,
)
from runtime.detail_variants.variant_validator import validate_variant, validate_variant_manifest
from runtime.detail_variants.geometry_parameter_mapper import (
    map_geometry_to_parameters,
    get_applicable_parameters,
)


def test_variant_payload_validates():
    """Generated variant payload passes validation."""
    variant = generate_variant(
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        {"parapet_height": 24, "membrane_thickness": 0.060},
        variant_sequence=1,
    )
    errors = validate_variant(variant)
    assert errors == [], f"Validation errors: {errors}"
    assert variant["variant_id"].startswith("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01-V")
    print("  PASS: variant_payload_validates")


def test_prohibited_combinations_excluded():
    """Prohibited parameter combinations are rejected."""
    try:
        generate_variant(
            "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
            {"parapet_height": 72, "membrane_thickness": 0.035},
        )
        assert False, "Should have raised VariantGenerationError"
    except VariantGenerationError as e:
        assert "Prohibited" in str(e)
    print("  PASS: prohibited_combinations_excluded")


def test_canonical_ids_unchanged():
    """Variant generation does not alter canonical IDs."""
    variant = generate_variant(
        "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
        {"pipe_diameter": 4, "membrane_thickness": 0.060},
    )
    assert variant["canonical_detail_id"] == "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01"
    assert variant["provenance"]["canonical_detail_id"] == "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01"
    print("  PASS: canonical_ids_unchanged")


def test_invalid_canonical_id_fails():
    """Non-canonical detail ID fails closed."""
    try:
        generate_variant("FABRICATED-ID-01", {"parapet_height": 24})
        assert False, "Should have raised VariantGenerationError"
    except VariantGenerationError:
        pass
    print("  PASS: invalid_canonical_id_fails")


def test_out_of_range_parameter_fails():
    """Parameter outside allowed range fails."""
    try:
        generate_variant(
            "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
            {"parapet_height": 200},
        )
        assert False, "Should have raised VariantGenerationError"
    except VariantGenerationError as e:
        assert "outside allowed range" in str(e)
    print("  PASS: out_of_range_parameter_fails")


def test_inapplicable_parameter_fails():
    """Parameter not applicable to condition fails."""
    try:
        generate_variant(
            "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
            {"pipe_diameter": 4},
        )
        assert False, "Should have raised VariantGenerationError"
    except VariantGenerationError as e:
        assert "not applicable" in str(e)
    print("  PASS: inapplicable_parameter_fails")


def test_variant_manifest_validates():
    """Complete variant manifest passes validation."""
    v1 = generate_variant(
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        {"parapet_height": 24, "membrane_thickness": 0.060},
        variant_sequence=1,
    )
    v2 = generate_variant(
        "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
        {"pipe_diameter": 4, "membrane_thickness": 0.060},
        variant_sequence=1,
    )
    manifest = generate_variant_manifest([v1, v2])
    errors = validate_variant_manifest(manifest)
    assert errors == [], f"Manifest validation errors: {errors}"
    print("  PASS: variant_manifest_validates")


def test_deterministic_variant_output():
    """Identical inputs produce identical variant outputs."""
    v1 = generate_variant(
        "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
        {"drain_diameter": 6, "membrane_thickness": 0.060},
    )
    v2 = generate_variant(
        "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
        {"drain_diameter": 6, "membrane_thickness": 0.060},
    )
    assert v1 == v2
    print("  PASS: deterministic_variant_output")


def test_geometry_parameter_mapping():
    """Geometry hints map correctly to variant parameters."""
    params = map_geometry_to_parameters(
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        {"parapet_height": 36, "membrane_thickness": 0.060},
    )
    assert params["parapet_height"] == 36.0
    assert params["membrane_thickness"] == 0.060
    print("  PASS: geometry_parameter_mapping")


def run_all():
    print("Variant Generator Tests:")
    test_variant_payload_validates()
    test_prohibited_combinations_excluded()
    test_canonical_ids_unchanged()
    test_invalid_canonical_id_fails()
    test_out_of_range_parameter_fails()
    test_inapplicable_parameter_fails()
    test_variant_manifest_validates()
    test_deterministic_variant_output()
    test_geometry_parameter_mapping()
    print("  All variant tests passed.\n")


if __name__ == "__main__":
    run_all()
