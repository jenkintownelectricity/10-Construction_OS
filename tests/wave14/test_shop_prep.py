"""
Wave 14 — Shop Drawing Preparation Tests.

Tests:
- Manifest builds successfully
- Unsupported detail cannot silently enter package
- Deterministic output
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.shop_drawing_prep.sheet_index_generator import generate_sheet_index
from runtime.shop_drawing_prep.detail_packager import (
    package_detail,
    package_details_batch,
    DetailPackagingError,
    CANONICAL_DETAIL_FAMILIES,
)
from runtime.shop_drawing_prep.drawing_manifest_builder import (
    build_drawing_manifest,
    build_drawing_package_manifest,
)
from runtime.shop_drawing_prep.shop_prep_validator import (
    validate_shop_drawing_manifest,
    validate_sheet_index,
)


def _build_test_resolved_items():
    return [
        {"canonical_detail_id": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01", "resolution_status": "RESOLVED", "condition_ref": "CN-PARAPET-0001"},
        {"canonical_detail_id": "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01", "resolution_status": "RESOLVED", "condition_ref": "CN-DRAIN-0001"},
        {"canonical_detail_id": "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01", "resolution_status": "RESOLVED", "condition_ref": "CN-PIPE-0001"},
        {"canonical_detail_id": None, "resolution_status": "UNKNOWN", "condition_ref": "CN-FIELD-0001"},
    ]


def test_manifest_builds_successfully():
    """Shop drawing manifest builds from resolved items."""
    items = _build_test_resolved_items()
    sheet_index = generate_sheet_index(items, "TEST-001")
    packaged, rejected = package_details_batch([
        {"canonical_detail_id": i["canonical_detail_id"], "condition_ref": i["condition_ref"]}
        for i in items if i["resolution_status"] == "RESOLVED"
    ])
    manifest = build_drawing_manifest("TEST-001", sheet_index, packaged)

    assert manifest["manifest_id"] == "shop-drawing-TEST-001"
    assert len(manifest["drawing_entries"]) > 0
    assert manifest["checksum"]
    print("  PASS: manifest_builds_successfully")


def test_unsupported_detail_cannot_enter():
    """Unsupported details are rejected, never silently packaged."""
    try:
        package_detail("FABRICATED-DETAIL-ID-01")
        assert False, "Should have raised DetailPackagingError"
    except DetailPackagingError:
        pass

    items = [
        {"canonical_detail_id": "FABRICATED-ID", "condition_ref": "CN-TEST-0001"},
        {"canonical_detail_id": "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01", "condition_ref": "CN-DRAIN-0001"},
    ]
    packaged, rejected = package_details_batch(items)
    assert len(rejected) == 1
    assert len(packaged) == 1
    print("  PASS: unsupported_detail_cannot_enter")


def test_shop_manifest_validates():
    """Generated manifest passes validation."""
    items = _build_test_resolved_items()
    sheet_index = generate_sheet_index(items, "VAL-001")
    packaged, _ = package_details_batch([
        {"canonical_detail_id": i["canonical_detail_id"], "condition_ref": i["condition_ref"]}
        for i in items if i["resolution_status"] == "RESOLVED"
    ])
    manifest = build_drawing_manifest("VAL-001", sheet_index, packaged)
    errors = validate_shop_drawing_manifest(manifest)
    assert errors == [], f"Validation errors: {errors}"
    print("  PASS: shop_manifest_validates")


def test_sheet_index_validates():
    """Generated sheet index passes validation."""
    items = _build_test_resolved_items()
    index = generate_sheet_index(items, "IDX-001")
    errors = validate_sheet_index(index)
    assert errors == [], f"Validation errors: {errors}"
    print("  PASS: sheet_index_validates")


def test_deterministic_shop_output():
    """Identical inputs produce identical shop prep output."""
    items = _build_test_resolved_items()
    s1 = generate_sheet_index(items, "DET-001")
    s2 = generate_sheet_index(items, "DET-001")
    assert s1["checksum"] == s2["checksum"]
    assert s1["sheets"] == s2["sheets"]
    print("  PASS: deterministic_shop_output")


def test_drawing_package_manifest():
    """Drawing package manifest builds correctly."""
    items = _build_test_resolved_items()
    sheet_index = generate_sheet_index(items, "PKG-001")
    packaged, _ = package_details_batch([
        {"canonical_detail_id": i["canonical_detail_id"], "condition_ref": i["condition_ref"]}
        for i in items if i["resolution_status"] == "RESOLVED"
    ])
    shop_manifest = build_drawing_manifest("PKG-001", sheet_index, packaged)
    pkg = build_drawing_package_manifest("PKG-001", shop_manifest, sheet_index)
    assert pkg["package_id"] == "pkg-PKG-001"
    assert pkg["checksum"]
    print("  PASS: drawing_package_manifest")


def run_all():
    print("Shop Drawing Preparation Tests:")
    test_manifest_builds_successfully()
    test_unsupported_detail_cannot_enter()
    test_shop_manifest_validates()
    test_sheet_index_validates()
    test_deterministic_shop_output()
    test_drawing_package_manifest()
    print("  All shop prep tests passed.\n")


if __name__ == "__main__":
    run_all()
