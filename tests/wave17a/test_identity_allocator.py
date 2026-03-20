"""
Tests for IdentityAllocator — Wave 17A.

Tests: identity determinism, collision rejection, idempotent replay,
valid/invalid types.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from runtime.reference_graph.identity_allocator import (
    IdentityAllocator,
    IdentityAllocationError,
    VALID_OBJECT_TYPES,
)


class TestIdentityDeterminism:
    """Identity allocation must be deterministic."""

    def test_same_inputs_produce_same_fingerprint(self):
        fp1 = IdentityAllocator.compute_fingerprint("sys", "ref", "DETAIL", "global")
        fp2 = IdentityAllocator.compute_fingerprint("sys", "ref", "DETAIL", "global")
        assert fp1 == fp2

    def test_different_inputs_produce_different_fingerprints(self):
        fp1 = IdentityAllocator.compute_fingerprint("sys", "ref1", "DETAIL", "global")
        fp2 = IdentityAllocator.compute_fingerprint("sys", "ref2", "DETAIL", "global")
        assert fp1 != fp2

    def test_allocated_id_format(self):
        alloc = IdentityAllocator()
        gid = alloc.allocate("Construction_Kernel", "D-001", "DETAIL", "global")
        assert gid.startswith("CRG-DETAIL-")
        assert len(gid.split("-")) == 3

    def test_sequential_ids_are_unique(self):
        alloc = IdentityAllocator()
        id1 = alloc.allocate("sys", "ref1", "DETAIL", "global")
        id2 = alloc.allocate("sys", "ref2", "DETAIL", "global")
        assert id1 != id2

    def test_id_number_is_zero_padded(self):
        alloc = IdentityAllocator()
        gid = alloc.allocate("sys", "ref1", "VARIANT", "global")
        assert gid == "CRG-VARIANT-000001"


class TestCollisionRejection:
    """Duplicate allocations with different payloads must fail closed."""

    def test_collision_with_different_payload_fails(self):
        alloc = IdentityAllocator()
        alloc.allocate("sys", "ref1", "DETAIL", "global", payload={"a": 1})
        try:
            alloc.allocate("sys", "ref1", "DETAIL", "global", payload={"a": 2})
            assert False, "Should have raised IdentityAllocationError"
        except IdentityAllocationError:
            pass

    def test_collision_detection_across_types(self):
        alloc = IdentityAllocator()
        alloc.allocate("sys", "ref1", "DETAIL", "global")
        # Same source but different type — should succeed (different fingerprint)
        gid2 = alloc.allocate("sys", "ref1", "VARIANT", "global")
        assert gid2.startswith("CRG-VARIANT-")


class TestIdempotentReplay:
    """Identical re-submissions must return existing ID."""

    def test_identical_payload_returns_same_id(self):
        alloc = IdentityAllocator()
        id1 = alloc.allocate("sys", "ref1", "DETAIL", "global", payload={"x": 1})
        id2 = alloc.allocate("sys", "ref1", "DETAIL", "global", payload={"x": 1})
        assert id1 == id2

    def test_empty_payload_replay(self):
        alloc = IdentityAllocator()
        id1 = alloc.allocate("sys", "ref1", "DETAIL", "global")
        id2 = alloc.allocate("sys", "ref1", "DETAIL", "global")
        assert id1 == id2


class TestInvalidTypes:
    """Invalid object types must fail closed."""

    def test_invalid_object_type_fails(self):
        alloc = IdentityAllocator()
        try:
            alloc.allocate("sys", "ref1", "INVALID_TYPE", "global")
            assert False, "Should have raised IdentityAllocationError"
        except IdentityAllocationError:
            pass

    def test_empty_source_system_fails(self):
        alloc = IdentityAllocator()
        try:
            alloc.allocate("", "ref1", "DETAIL", "global")
            assert False, "Should have raised IdentityAllocationError"
        except IdentityAllocationError:
            pass

    def test_empty_source_reference_fails(self):
        alloc = IdentityAllocator()
        try:
            alloc.allocate("sys", "", "DETAIL", "global")
            assert False, "Should have raised IdentityAllocationError"
        except IdentityAllocationError:
            pass

    def test_all_valid_types_accepted(self):
        alloc = IdentityAllocator()
        for i, obj_type in enumerate(sorted(VALID_OBJECT_TYPES)):
            gid = alloc.allocate("sys", f"ref-{i}", obj_type, "global")
            assert gid.startswith("CRG-")


class TestAllocatorReset:
    """Reset clears all state."""

    def test_reset_clears_counters(self):
        alloc = IdentityAllocator()
        alloc.allocate("sys", "ref1", "DETAIL", "global")
        assert alloc.count() == 1
        alloc.reset()
        assert alloc.count() == 0

    def test_after_reset_can_reallocate(self):
        alloc = IdentityAllocator()
        id1 = alloc.allocate("sys", "ref1", "DETAIL", "global")
        alloc.reset()
        id2 = alloc.allocate("sys", "ref1", "DETAIL", "global")
        assert id1 == id2  # same number since counter reset
