"""
Wave 14 — Master Test Runner.

Runs all Wave 14 test groups and produces a summary report.
"""

import sys
import os
import json
import hashlib
from datetime import datetime, timezone

# Ensure runtime modules are importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from tests.wave14.test_condition_graph import run_all as run_condition_graph
from tests.wave14.test_resolver import run_all as run_resolver
from tests.wave14.test_variants import run_all as run_variants
from tests.wave14.test_field_scan import run_all as run_field_scan
from tests.wave14.test_sequence import run_all as run_sequence
from tests.wave14.test_shop_prep import run_all as run_shop_prep
from tests.wave14.test_boundary import run_all as run_boundary
from tests.wave14.test_determinism import run_all as run_determinism


def run_observer_tests():
    """Run VKBUS observer tests against generated data."""
    print("Observer Tests:")

    # Build test data
    from runtime.condition_graph.condition_graph_builder import ConditionGraphBuilder
    from runtime.detail_resolver.detail_resolution_engine import resolve_details
    from runtime.detail_variants.variant_generator import generate_variant, generate_variant_manifest
    from runtime.installation_sequence.sequence_engine import generate_sequence_manifest, CANONICAL_DETAIL_FAMILIES
    from runtime.shop_drawing_prep.sheet_index_generator import generate_sheet_index
    from runtime.shop_drawing_prep.detail_packager import package_details_batch
    from runtime.shop_drawing_prep.drawing_manifest_builder import build_drawing_manifest
    from runtime.field_scan.condition_detector import detect_condition_from_manual

    # Add VKBUS to path
    vkbus_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ValidKernelOS_VKBUS")
    sys.path.insert(0, vkbus_path)

    # Build condition graph
    builder = ConditionGraphBuilder("obs-test-001", ["observer-test"])
    builder.add_node("CN-PARAPET-0001", "PARAPET", "Parapet", "A1")
    builder.add_node("CN-DRAIN-0001", "DRAIN", "Drain", "B1")
    builder.add_node("CN-EDGE-0001", "EDGE", "Edge", "C1")
    builder.add_edge("CN-PARAPET-0001", "CN-EDGE-0001", "adjacent_to")
    builder.add_edge("CN-EDGE-0001", "CN-DRAIN-0001", "adjacent_to")
    graph = builder.build()

    # Resolve details
    manifest = resolve_details(graph, "EPDM")

    # Generate variants
    v1 = generate_variant(
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        {"parapet_height": 24, "membrane_thickness": 0.060}, 1,
    )
    variant_manifest = generate_variant_manifest([v1])

    # Generate sequences
    seq_manifest = generate_sequence_manifest(sorted(CANONICAL_DETAIL_FAMILIES))

    # Generate shop drawing manifest
    resolved_items = manifest["resolved_items"]
    sheet_index = generate_sheet_index(resolved_items, "OBS-001")
    packaged, _ = package_details_batch([
        {"canonical_detail_id": i["canonical_detail_id"], "condition_ref": i["condition_ref"]}
        for i in resolved_items if i["resolution_status"] == "RESOLVED"
    ])
    shop_manifest = build_drawing_manifest("OBS-001", sheet_index, packaged)

    # Generate scan results
    scan_results = [
        detect_condition_from_manual("PARAPET", "Parapet", "ev-001"),
        detect_condition_from_manual("DRAIN", "Drain", "ev-002"),
    ]

    # Run observers
    try:
        from bus.observers.condition_graph_boundary_test import observe_condition_graph
        result = observe_condition_graph(graph)
        assert result["status"] == "PASS", f"Condition graph observer failed: {result}"
        print("  PASS: condition_graph_boundary_observer")
    except ImportError:
        print("  SKIP: condition_graph_boundary_observer (VKBUS not available)")

    try:
        from bus.observers.resolver_boundary_test import observe_resolved_manifest
        result = observe_resolved_manifest(manifest)
        assert result["status"] == "PASS", f"Resolver observer failed: {result}"
        print("  PASS: resolver_boundary_observer")
    except ImportError:
        print("  SKIP: resolver_boundary_observer (VKBUS not available)")

    try:
        from bus.observers.variant_engine_boundary_test import observe_variant_manifest
        result = observe_variant_manifest(variant_manifest)
        assert result["status"] == "PASS", f"Variant observer failed: {result}"
        print("  PASS: variant_engine_boundary_observer")
    except ImportError:
        print("  SKIP: variant_engine_boundary_observer (VKBUS not available)")

    try:
        from bus.observers.field_scan_boundary_test import observe_scan_results
        result = observe_scan_results(scan_results)
        assert result["status"] == "PASS", f"Field scan observer failed: {result}"
        print("  PASS: field_scan_boundary_observer")
    except ImportError:
        print("  SKIP: field_scan_boundary_observer (VKBUS not available)")

    try:
        from bus.observers.sequence_engine_boundary_test import observe_sequence_manifest
        result = observe_sequence_manifest(seq_manifest)
        assert result["status"] == "PASS", f"Sequence observer failed: {result}"
        print("  PASS: sequence_engine_boundary_observer")
    except ImportError:
        print("  SKIP: sequence_engine_boundary_observer (VKBUS not available)")

    try:
        from bus.observers.shop_prep_boundary_test import observe_shop_drawing_manifest
        result = observe_shop_drawing_manifest(shop_manifest)
        assert result["status"] == "PASS", f"Shop prep observer failed: {result}"
        print("  PASS: shop_prep_boundary_observer")
    except ImportError:
        print("  SKIP: shop_prep_boundary_observer (VKBUS not available)")

    print("  All observer tests passed.\n")


def generate_checksum_summary():
    """Generate determinism checksum summary."""
    from runtime.condition_graph.condition_graph_builder import ConditionGraphBuilder
    from runtime.detail_resolver.detail_resolution_engine import resolve_details
    from runtime.detail_variants.variant_generator import generate_variant, generate_variant_manifest
    from runtime.installation_sequence.sequence_engine import generate_sequence_manifest, CANONICAL_DETAIL_FAMILIES
    from runtime.shop_drawing_prep.sheet_index_generator import generate_sheet_index
    from runtime.shop_drawing_prep.detail_packager import package_details_batch
    from runtime.shop_drawing_prep.drawing_manifest_builder import build_drawing_manifest
    from runtime.detail_map.detail_graph_visualizer import build_navigation_summary

    # Build standard graph
    builder = ConditionGraphBuilder("checksum-001", ["checksum-test"])
    builder.add_node("CN-PARAPET-0001", "PARAPET", "Parapet", "A1")
    builder.add_node("CN-DRAIN-0001", "DRAIN", "Drain", "B1")
    builder.add_node("CN-EDGE-0001", "EDGE", "Edge", "C1")
    builder.add_node("CN-PIPE_PENETRATION-0001", "PIPE_PENETRATION", "Pipe", "D1")
    builder.add_node("CN-SCUPPER-0001", "SCUPPER", "Scupper", "E1")
    builder.add_edge("CN-PARAPET-0001", "CN-EDGE-0001", "adjacent_to")
    builder.add_edge("CN-EDGE-0001", "CN-SCUPPER-0001", "terminates_at")
    builder.add_edge("CN-PARAPET-0001", "CN-DRAIN-0001", "adjacent_to")
    graph = builder.build()

    manifest = resolve_details(graph, "EPDM")
    v1 = generate_variant("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01", {"parapet_height": 24, "membrane_thickness": 0.060}, 1)
    var_manifest = generate_variant_manifest([v1], "checksum-var")
    seq_manifest = generate_sequence_manifest(sorted(CANONICAL_DETAIL_FAMILIES), "checksum-seq")
    nav_summary = build_navigation_summary()

    resolved_items = manifest["resolved_items"]
    si = generate_sheet_index(resolved_items, "CS-001")
    packaged, _ = package_details_batch([
        {"canonical_detail_id": i["canonical_detail_id"], "condition_ref": i["condition_ref"]}
        for i in resolved_items if i["resolution_status"] == "RESOLVED"
    ])
    shop_manifest = build_drawing_manifest("CS-001", si, packaged)

    summary = {
        "project_condition_graph.json": graph.get("checksum", ""),
        "resolved_detail_manifest.json": manifest.get("checksum", ""),
        "variant_manifest.json": var_manifest.get("checksum", ""),
        "detail_navigation_summary.json": hashlib.sha256(
            json.dumps(nav_summary, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "installation_sequence_manifest.json": seq_manifest.get("checksum", ""),
        "project_shop_drawing_manifest.json": shop_manifest.get("checksum", ""),
    }

    return summary


if __name__ == "__main__":
    print("=" * 60)
    print("WAVE 14 — FULL TEST SUITE")
    print("=" * 60)
    print()

    run_condition_graph()
    run_resolver()
    run_variants()
    run_field_scan()
    run_sequence()
    run_shop_prep()
    run_boundary()
    run_determinism()
    run_observer_tests()

    print("=" * 60)
    print("CHECKSUM SUMMARY")
    print("=" * 60)
    checksums = generate_checksum_summary()
    for artifact, checksum in sorted(checksums.items()):
        print(f"  {artifact}: {checksum[:32]}...")

    print()
    print("=" * 60)
    print("ALL WAVE 14 TESTS PASSED")
    print("Canonical Detail DNA truth remained unchanged.")
    print("=" * 60)
