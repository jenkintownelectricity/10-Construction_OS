"""
Wave 14 — Determinism Tests.

Runs subsystem generation twice and compares checksums.
Outputs must match exactly.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.condition_graph.condition_graph_builder import ConditionGraphBuilder
from runtime.condition_graph.condition_graph_serializer import serialize_graph
from runtime.detail_resolver.detail_resolution_engine import resolve_details
from runtime.detail_variants.variant_generator import generate_variant, generate_variant_manifest
from runtime.detail_map.detail_route_query import get_all_detail_ids, get_neighbors
from runtime.detail_map.detail_pathfinder import find_path
from runtime.detail_map.detail_graph_visualizer import build_navigation_summary
from runtime.installation_sequence.sequence_engine import generate_sequence_manifest
from runtime.shop_drawing_prep.sheet_index_generator import generate_sheet_index
from runtime.shop_drawing_prep.detail_packager import package_details_batch
from runtime.shop_drawing_prep.drawing_manifest_builder import build_drawing_manifest


def _build_standard_graph():
    builder = ConditionGraphBuilder("det-standard-001", ["determinism-test"])
    builder.add_node("CN-PARAPET-0001", "PARAPET", "North Parapet", "A1")
    builder.add_node("CN-DRAIN-0001", "DRAIN", "Main Drain", "B1")
    builder.add_node("CN-EDGE-0001", "EDGE", "East Edge", "C1")
    builder.add_node("CN-PIPE_PENETRATION-0001", "PIPE_PENETRATION", "Vent Pipe", "D1")
    builder.add_node("CN-SCUPPER-0001", "SCUPPER", "Overflow Scupper", "E1")
    builder.add_node("CN-CURB-0001", "CURB", "HVAC Curb", "F1")
    builder.add_node("CN-EXPANSION_JOINT-0001", "EXPANSION_JOINT", "EJ-1", "G1")
    builder.add_node("CN-ROOF_FIELD-0001", "ROOF_FIELD", "Main Field", "H1")
    builder.add_edge("CN-ROOF_FIELD-0001", "CN-DRAIN-0001", "drains_to")
    builder.add_edge("CN-ROOF_FIELD-0001", "CN-SCUPPER-0001", "drains_to")
    builder.add_edge("CN-PARAPET-0001", "CN-EDGE-0001", "adjacent_to")
    builder.add_edge("CN-EDGE-0001", "CN-SCUPPER-0001", "terminates_at")
    builder.add_edge("CN-EXPANSION_JOINT-0001", "CN-PARAPET-0001", "terminates_at")
    builder.add_edge("CN-PIPE_PENETRATION-0001", "CN-ROOF_FIELD-0001", "penetrates")
    builder.add_edge("CN-CURB-0001", "CN-PIPE_PENETRATION-0001", "adjacent_to")
    return builder.build()


def test_condition_graph_determinism():
    """Condition graph checksums match across two builds."""
    g1 = _build_standard_graph()
    g2 = _build_standard_graph()
    assert g1["checksum"] == g2["checksum"], "Condition graph checksums must match"
    assert serialize_graph(g1) == serialize_graph(g2), "Serialized graphs must match"
    print("  PASS: condition_graph_determinism")


def test_resolved_manifest_determinism():
    """Resolved detail manifest checksums match."""
    graph = _build_standard_graph()
    m1 = resolve_details(graph, material_context="EPDM")
    m2 = resolve_details(graph, material_context="EPDM")
    assert m1["checksum"] == m2["checksum"], "Resolved manifest checksums must match"
    assert m1["resolved_items"] == m2["resolved_items"]
    print("  PASS: resolved_manifest_determinism")


def test_variant_manifest_determinism():
    """Variant manifest checksums match."""
    v1a = generate_variant(
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        {"parapet_height": 24, "membrane_thickness": 0.060}, 1,
    )
    v2a = generate_variant(
        "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
        {"pipe_diameter": 4, "membrane_thickness": 0.060}, 1,
    )
    m1 = generate_variant_manifest([v1a, v2a], "det-variant-001")

    v1b = generate_variant(
        "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
        {"parapet_height": 24, "membrane_thickness": 0.060}, 1,
    )
    v2b = generate_variant(
        "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
        {"pipe_diameter": 4, "membrane_thickness": 0.060}, 1,
    )
    m2 = generate_variant_manifest([v1b, v2b], "det-variant-001")

    assert m1["checksum"] == m2["checksum"], "Variant manifest checksums must match"
    print("  PASS: variant_manifest_determinism")


def test_detail_paths_determinism():
    """Detail path queries produce deterministic results."""
    all_ids = get_all_detail_ids()
    assert all_ids == sorted(all_ids), "Detail IDs must be deterministically sorted"

    n1 = get_neighbors(all_ids[0])
    n2 = get_neighbors(all_ids[0])
    assert n1 == n2, "Neighbor queries must be deterministic"

    if len(all_ids) >= 2:
        p1 = find_path(all_ids[0], all_ids[-1])
        p2 = find_path(all_ids[0], all_ids[-1])
        assert p1 == p2, "Path queries must be deterministic"

    s1 = build_navigation_summary()
    s2 = build_navigation_summary()
    assert json.dumps(s1, sort_keys=True) == json.dumps(s2, sort_keys=True)
    print("  PASS: detail_paths_determinism")


def test_sequence_manifest_determinism():
    """Installation sequence manifest checksums match."""
    from runtime.installation_sequence.sequence_engine import CANONICAL_DETAIL_FAMILIES
    ids = sorted(CANONICAL_DETAIL_FAMILIES)
    m1 = generate_sequence_manifest(ids, "det-seq-001")
    m2 = generate_sequence_manifest(ids, "det-seq-001")
    assert m1["checksum"] == m2["checksum"], "Sequence manifest checksums must match"
    assert m1["sequences"] == m2["sequences"]
    print("  PASS: sequence_manifest_determinism")


def test_shop_drawing_manifest_determinism():
    """Shop drawing manifest checksums match."""
    items = [
        {"canonical_detail_id": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01", "resolution_status": "RESOLVED", "condition_ref": "CN-PARAPET-0001"},
        {"canonical_detail_id": "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01", "resolution_status": "RESOLVED", "condition_ref": "CN-DRAIN-0001"},
    ]

    s1 = generate_sheet_index(items, "DET-001")
    p1, _ = package_details_batch([
        {"canonical_detail_id": i["canonical_detail_id"], "condition_ref": i["condition_ref"]}
        for i in items
    ])
    m1 = build_drawing_manifest("DET-001", s1, p1)

    s2 = generate_sheet_index(items, "DET-001")
    p2, _ = package_details_batch([
        {"canonical_detail_id": i["canonical_detail_id"], "condition_ref": i["condition_ref"]}
        for i in items
    ])
    m2 = build_drawing_manifest("DET-001", s2, p2)

    assert m1["checksum"] == m2["checksum"], "Shop drawing manifest checksums must match"
    assert m1["drawing_entries"] == m2["drawing_entries"]
    print("  PASS: shop_drawing_manifest_determinism")


def run_all():
    print("Determinism Tests:")
    test_condition_graph_determinism()
    test_resolved_manifest_determinism()
    test_variant_manifest_determinism()
    test_detail_paths_determinism()
    test_sequence_manifest_determinism()
    test_shop_drawing_manifest_determinism()
    print("  All determinism tests passed.\n")


if __name__ == "__main__":
    run_all()
