"""
Wave 14 — Installation Sequence Tests.

Tests:
- Sequence has no circular dependency
- Invalid dependency chains fail closed
- Deterministic output
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.installation_sequence.sequence_engine import (
    generate_sequence,
    generate_sequence_manifest,
    SequenceGenerationError,
    CANONICAL_DETAIL_FAMILIES,
)
from runtime.installation_sequence.dependency_resolver import (
    validate_dependencies,
    get_execution_order,
)
from runtime.installation_sequence.sequence_validator import validate_sequence_manifest


def test_sequence_no_circular_dependency():
    """All generated sequences have valid acyclic dependencies."""
    for detail_id in sorted(CANONICAL_DETAIL_FAMILIES):
        seq = generate_sequence(detail_id)
        if seq["status"] == "RESOLVED":
            errors = validate_dependencies(seq)
            assert errors == [], f"Dependency errors for {detail_id}: {errors}"
    print("  PASS: sequence_no_circular_dependency")


def test_invalid_detail_fails():
    """Non-canonical detail ID fails closed."""
    try:
        generate_sequence("FABRICATED-DETAIL-ID-01")
        assert False, "Should have raised SequenceGenerationError"
    except SequenceGenerationError:
        pass
    print("  PASS: invalid_detail_fails")


def test_execution_order_valid():
    """Execution order can be computed for all sequences."""
    for detail_id in sorted(CANONICAL_DETAIL_FAMILIES):
        seq = generate_sequence(detail_id)
        if seq["status"] == "RESOLVED" and seq["steps"]:
            order = get_execution_order(seq)
            assert len(order) == len(seq["steps"]), f"Order length mismatch for {detail_id}"
    print("  PASS: execution_order_valid")


def test_sequence_manifest_validates():
    """Complete sequence manifest passes validation."""
    manifest = generate_sequence_manifest(list(CANONICAL_DETAIL_FAMILIES))
    errors = validate_sequence_manifest(manifest)
    assert errors == [], f"Manifest validation errors: {errors}"
    print("  PASS: sequence_manifest_validates")


def test_deterministic_sequence_output():
    """Identical inputs produce identical sequence outputs."""
    ids = sorted(CANONICAL_DETAIL_FAMILIES)
    m1 = generate_sequence_manifest(ids)
    m2 = generate_sequence_manifest(ids)
    assert m1["sequences"] == m2["sequences"]
    assert m1["checksum"] == m2["checksum"]
    print("  PASS: deterministic_sequence_output")


def test_all_canonical_details_have_sequences():
    """Every canonical detail has a sequence (RESOLVED or UNRESOLVED)."""
    for detail_id in sorted(CANONICAL_DETAIL_FAMILIES):
        seq = generate_sequence(detail_id)
        assert seq["status"] in ("RESOLVED", "UNRESOLVED"), f"Unexpected status for {detail_id}: {seq['status']}"
    print("  PASS: all_canonical_details_have_sequences")


def run_all():
    print("Installation Sequence Tests:")
    test_sequence_no_circular_dependency()
    test_invalid_detail_fails()
    test_execution_order_valid()
    test_sequence_manifest_validates()
    test_deterministic_sequence_output()
    test_all_canonical_details_have_sequences()
    print("  All sequence tests passed.\n")


if __name__ == "__main__":
    run_all()
