"""
Tests for reflection_status_manager.py — ReflectionStatus, ReflectionEntry,
ReflectionStatusManager.
"""

from __future__ import annotations

import unittest

from runtime.mirror_control.reflection_status_manager import (
    VALID_TRANSITIONS,
    ReflectionStatus,
    ReflectionStatusManager,
)


class TestReflectionStatus(unittest.TestCase):
    """Tests for the ReflectionStatus enum and transition rules."""

    def test_status_values(self) -> None:
        self.assertEqual(ReflectionStatus.STAGED.value, "staged")
        self.assertEqual(ReflectionStatus.ACTIVE.value, "active")
        self.assertEqual(ReflectionStatus.FROZEN.value, "frozen")
        self.assertEqual(ReflectionStatus.DEPRECATED.value, "deprecated")

    def test_deprecated_is_terminal(self) -> None:
        self.assertEqual(len(VALID_TRANSITIONS[ReflectionStatus.DEPRECATED]), 0)

    def test_staged_can_go_to_active(self) -> None:
        self.assertIn(
            ReflectionStatus.ACTIVE,
            VALID_TRANSITIONS[ReflectionStatus.STAGED],
        )

    def test_active_can_go_to_frozen(self) -> None:
        self.assertIn(
            ReflectionStatus.FROZEN,
            VALID_TRANSITIONS[ReflectionStatus.ACTIVE],
        )

    def test_frozen_can_reactivate(self) -> None:
        self.assertIn(
            ReflectionStatus.ACTIVE,
            VALID_TRANSITIONS[ReflectionStatus.FROZEN],
        )


class TestReflectionStatusManager(unittest.TestCase):
    """Tests for the ReflectionStatusManager class."""

    def setUp(self) -> None:
        self.manager = ReflectionStatusManager()

    def test_register_reflection(self) -> None:
        entry = self.manager.register(
            reflection_id="ref-001",
            mirror_id="mirror-a",
            slice_id="slice-x",
        )
        self.assertEqual(entry.status, ReflectionStatus.STAGED)
        self.assertEqual(entry.mirror_id, "mirror-a")
        self.assertEqual(len(entry.history), 1)

    def test_register_duplicate_raises(self) -> None:
        self.manager.register("ref-001", "m1", "s1")
        with self.assertRaises(ValueError):
            self.manager.register("ref-001", "m1", "s1")

    def test_get_status(self) -> None:
        self.manager.register("ref-002", "m1", "s1")
        status = self.manager.get_status("ref-002")
        self.assertEqual(status, ReflectionStatus.STAGED)

    def test_get_status_not_found(self) -> None:
        with self.assertRaises(KeyError):
            self.manager.get_status("nonexistent")

    def test_set_status_valid_transition(self) -> None:
        self.manager.register("ref-003", "m1", "s1")
        entry = self.manager.set_status(
            "ref-003",
            ReflectionStatus.ACTIVE,
            reason="Activated",
        )
        self.assertEqual(entry.status, ReflectionStatus.ACTIVE)
        self.assertEqual(len(entry.history), 2)

    def test_set_status_invalid_transition_raises(self) -> None:
        self.manager.register("ref-004", "m1", "s1")
        with self.assertRaises(ValueError):
            self.manager.set_status("ref-004", ReflectionStatus.FROZEN)

    def test_set_status_not_found_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.manager.set_status("nonexistent", ReflectionStatus.ACTIVE)

    def test_deprecated_is_terminal(self) -> None:
        self.manager.register("ref-005", "m1", "s1")
        self.manager.set_status("ref-005", ReflectionStatus.ACTIVE)
        self.manager.set_status("ref-005", ReflectionStatus.DEPRECATED)
        with self.assertRaises(ValueError):
            self.manager.set_status("ref-005", ReflectionStatus.ACTIVE)

    def test_full_lifecycle(self) -> None:
        self.manager.register("ref-006", "m1", "s1")
        self.manager.set_status("ref-006", ReflectionStatus.ACTIVE)
        self.manager.set_status("ref-006", ReflectionStatus.FROZEN)
        self.manager.set_status("ref-006", ReflectionStatus.ACTIVE)
        self.manager.set_status("ref-006", ReflectionStatus.DEPRECATED)
        entry = self.manager.get_entry("ref-006")
        self.assertEqual(entry.status, ReflectionStatus.DEPRECATED)
        self.assertEqual(len(entry.history), 5)

    def test_validate_transition(self) -> None:
        self.assertTrue(
            self.manager.validate_transition(
                ReflectionStatus.STAGED, ReflectionStatus.ACTIVE
            )
        )
        self.assertFalse(
            self.manager.validate_transition(
                ReflectionStatus.STAGED, ReflectionStatus.FROZEN
            )
        )

    def test_list_reflections_no_filter(self) -> None:
        self.manager.register("ref-a", "m1", "s1")
        self.manager.register("ref-b", "m2", "s2")
        results = self.manager.list_reflections()
        self.assertEqual(len(results), 2)

    def test_list_reflections_filter_mirror(self) -> None:
        self.manager.register("ref-a", "m1", "s1")
        self.manager.register("ref-b", "m2", "s2")
        results = self.manager.list_reflections(mirror_id="m1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].mirror_id, "m1")

    def test_list_reflections_filter_status(self) -> None:
        self.manager.register("ref-a", "m1", "s1")
        self.manager.register("ref-b", "m1", "s2")
        self.manager.set_status("ref-a", ReflectionStatus.ACTIVE)
        results = self.manager.list_reflections(status=ReflectionStatus.ACTIVE)
        self.assertEqual(len(results), 1)

    def test_list_reflections_filter_slice(self) -> None:
        self.manager.register("ref-a", "m1", "slice-alpha")
        self.manager.register("ref-b", "m1", "slice-beta")
        results = self.manager.list_reflections(slice_id="slice-alpha")
        self.assertEqual(len(results), 1)

    def test_has_reflection(self) -> None:
        self.manager.register("ref-exists", "m1", "s1")
        self.assertTrue(self.manager.has_reflection("ref-exists"))
        self.assertFalse(self.manager.has_reflection("ref-nope"))

    def test_count(self) -> None:
        self.manager.register("ref-a", "m1", "s1")
        self.manager.register("ref-b", "m1", "s2")
        self.assertEqual(self.manager.count(), 2)
        self.assertEqual(self.manager.count(status=ReflectionStatus.STAGED), 2)
        self.assertEqual(self.manager.count(status=ReflectionStatus.ACTIVE), 0)

    def test_get_entry(self) -> None:
        self.manager.register("ref-get", "m1", "s1")
        entry = self.manager.get_entry("ref-get")
        self.assertEqual(entry.reflection_id, "ref-get")

    def test_get_entry_not_found(self) -> None:
        with self.assertRaises(KeyError):
            self.manager.get_entry("nonexistent")

    def test_entry_to_dict(self) -> None:
        entry = self.manager.register("ref-dict", "m1", "s1")
        d = entry.to_dict()
        self.assertEqual(d["reflection_id"], "ref-dict")
        self.assertEqual(d["status"], "staged")
        self.assertIn("history", d)


if __name__ == "__main__":
    unittest.main()
