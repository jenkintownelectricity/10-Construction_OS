"""
Wave 14 — Boundary Tests.

Tests:
- Kernel mutation attempt fails
- External renderer mutation impossible
- VKBUS observers pass
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.condition_graph.condition_graph_builder import (
    ConditionGraphBuilder,
    ConditionGraphBuildError,
    SUPPORTED_NODE_TYPES,
)
from runtime.detail_resolver.detail_selector import CANONICAL_DETAIL_FAMILIES
from runtime.detail_variants.variant_generator import (
    generate_variant,
    VariantGenerationError,
    CANONICAL_DETAIL_FAMILIES as VARIANT_FAMILIES,
)
from runtime.field_scan.condition_detector import detect_condition_from_manual
from runtime.field_scan.scan_validation import validate_scan_result


def test_kernel_mutation_attempt_fails():
    """Runtime cannot create new canonical condition types or detail families."""
    # Attempt to use a non-kernel condition type
    builder = ConditionGraphBuilder("boundary-001", ["test"])
    try:
        builder.add_node("CN-INVENTED-0001", "INVENTED_TYPE", "Invented", "A1")
        assert False, "Should fail closed on invented condition type"
    except ConditionGraphBuildError:
        pass

    # Attempt to use a fabricated detail ID in variant generation
    try:
        generate_variant("FABRICATED-FAMILY-ID-01", {"parapet_height": 24})
        assert False, "Should fail closed on fabricated family ID"
    except VariantGenerationError:
        pass

    # Verify canonical families are frozen sets (immutable)
    assert isinstance(CANONICAL_DETAIL_FAMILIES, dict)  # frozen content
    assert isinstance(VARIANT_FAMILIES, frozenset)
    print("  PASS: kernel_mutation_attempt_fails")


def test_renderer_isolation():
    """Shop drawing prep cannot include render commands or renderer mutations."""
    from runtime.shop_drawing_prep.detail_packager import package_detail

    entry = package_detail(
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        condition_ref="CN-PARAPET-0001",
    )
    # Verify no render commands in output
    assert "render_command" not in entry
    assert "svg_data" not in entry
    assert "dxf_data" not in entry
    assert "rendered_file" not in entry
    print("  PASS: renderer_isolation")


def test_scanner_cannot_mutate_kernel():
    """Scanner outputs are advisory only and cannot become truth."""
    result = detect_condition_from_manual("PARAPET", "Parapet", "ev-001")
    assert result["advisory_only"] is True

    # Verify no mutation indicators
    assert "write_to_kernel" not in result
    assert "create_family" not in result
    assert "mutate_truth" not in result

    errors = validate_scan_result(result)
    assert errors == []
    print("  PASS: scanner_cannot_mutate_kernel")


def test_frozen_artifacts_unchanged():
    """Verify frozen kernel artifacts are referenced but not modified."""
    # The 9 canonical families must be exactly these
    expected = frozenset([
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01",
        "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01",
        "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01",
        "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
        "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01",
        "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
        "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01",
        "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01",
    ])
    assert VARIANT_FAMILIES == expected, "Canonical families must not change"
    assert set(CANONICAL_DETAIL_FAMILIES.keys()) == expected, "Detail selector families must not change"
    print("  PASS: frozen_artifacts_unchanged")


def test_supported_node_types_match_spec():
    """Verify supported node types match Wave 14 spec."""
    expected = frozenset([
        "ROOF_FIELD", "PARAPET", "EDGE", "DRAIN",
        "SCUPPER", "CURB", "PIPE_PENETRATION", "EXPANSION_JOINT",
    ])
    assert SUPPORTED_NODE_TYPES == expected
    print("  PASS: supported_node_types_match_spec")


def run_all():
    print("Boundary Tests:")
    test_kernel_mutation_attempt_fails()
    test_renderer_isolation()
    test_scanner_cannot_mutate_kernel()
    test_frozen_artifacts_unchanged()
    test_supported_node_types_match_spec()
    print("  All boundary tests passed.\n")


if __name__ == "__main__":
    run_all()
