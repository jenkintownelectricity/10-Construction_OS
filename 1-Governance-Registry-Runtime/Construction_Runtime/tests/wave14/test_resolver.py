"""
Wave 14 — Detail Resolver Tests.

Tests:
- Resolver selects valid canonical detail IDs
- Unresolved cases return explicit UNRESOLVED
- Identical inputs return identical outputs
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.detail_resolver.condition_classifier import classify_condition
from runtime.detail_resolver.detail_selector import select_detail, CANONICAL_DETAIL_FAMILIES
from runtime.detail_resolver.detail_resolution_engine import resolve_details
from runtime.detail_resolver.detail_resolution_validator import validate_resolution_manifest


def _build_test_graph():
    """Build a minimal test condition graph."""
    return {
        "graph_id": "test-resolver-001",
        "source_refs": ["test"],
        "build_timestamp": "2026-03-20T00:00:00Z",
        "contract_version": "14.1.0",
        "nodes": [
            {"node_id": "CN-DRAIN-0001", "condition_type": "DRAIN", "label": "Main Drain", "position_ref": "A1", "metadata": {}},
            {"node_id": "CN-PARAPET-0001", "condition_type": "PARAPET", "label": "North Parapet", "position_ref": "B1", "metadata": {}},
            {"node_id": "CN-PIPE_PENETRATION-0001", "condition_type": "PIPE_PENETRATION", "label": "Vent Pipe", "position_ref": "C1", "metadata": {}},
            {"node_id": "CN-ROOF_FIELD-0001", "condition_type": "ROOF_FIELD", "label": "Field Area", "position_ref": "D1", "metadata": {}},
        ],
        "edges": [],
        "checksum": "",
    }


def test_resolver_selects_valid_canonical_ids():
    """Resolver returns only canonical detail IDs."""
    graph = _build_test_graph()
    manifest = resolve_details(graph, material_context="EPDM")

    for item in manifest["resolved_items"]:
        if item["resolution_status"] == "RESOLVED":
            assert item["canonical_detail_id"] in CANONICAL_DETAIL_FAMILIES, \
                f"Non-canonical ID: {item['canonical_detail_id']}"
    print("  PASS: resolver_selects_valid_canonical_ids")


def test_unresolved_cases_return_explicit_status():
    """Unresolvable conditions return UNKNOWN/UNRESOLVED explicitly."""
    graph = _build_test_graph()
    manifest = resolve_details(graph)

    # ROOF_FIELD has no detail families - should be UNKNOWN
    roof_field = next(
        (i for i in manifest["resolved_items"] if i["condition_ref"] == "CN-ROOF_FIELD-0001"),
        None,
    )
    assert roof_field is not None
    assert roof_field["resolution_status"] == "UNKNOWN"
    assert roof_field["canonical_detail_id"] is None
    print("  PASS: unresolved_cases_return_explicit_status")


def test_identical_inputs_return_identical_outputs():
    """Determinism: same inputs produce same outputs."""
    graph = _build_test_graph()
    m1 = resolve_details(graph, material_context="TPO")
    m2 = resolve_details(graph, material_context="TPO")

    assert m1["resolved_items"] == m2["resolved_items"]
    assert m1["checksum"] == m2["checksum"]
    print("  PASS: identical_inputs_return_identical_outputs")


def test_resolver_never_fabricates_ids():
    """Verify no ID is fabricated - all resolved IDs exist in canonical set."""
    selection = select_detail("PARAPET", "EPDM")
    if selection.canonical_detail_id:
        assert selection.canonical_detail_id in CANONICAL_DETAIL_FAMILIES

    selection = select_detail("NONEXISTENT_CONDITION")
    assert selection.status == "UNRESOLVED"
    assert selection.canonical_detail_id is None
    print("  PASS: resolver_never_fabricates_ids")


def test_classifier_unsupported_fails_closed():
    """Classifier returns UNSUPPORTED for unknown condition types."""
    node = {"node_id": "CN-TEST-0001", "condition_type": "SKYLIGHT"}
    result = classify_condition(node)
    assert result.status == "UNSUPPORTED"
    print("  PASS: classifier_unsupported_fails_closed")


def test_manifest_validation():
    """Validate a complete manifest passes validation."""
    graph = _build_test_graph()
    manifest = resolve_details(graph, material_context="EPDM")
    errors = validate_resolution_manifest(manifest)
    assert errors == [], f"Validation errors: {errors}"
    print("  PASS: manifest_validation")


def run_all():
    print("Detail Resolver Tests:")
    test_resolver_selects_valid_canonical_ids()
    test_unresolved_cases_return_explicit_status()
    test_identical_inputs_return_identical_outputs()
    test_resolver_never_fabricates_ids()
    test_classifier_unsupported_fails_closed()
    test_manifest_validation()
    print("  All resolver tests passed.\n")


if __name__ == "__main__":
    run_all()
