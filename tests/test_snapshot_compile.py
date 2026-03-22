"""Tests for snapshot compilation and deterministic hashing."""

import unittest

from awareness.freeze_compiler import FreezeCompiler
from awareness.snapshot_model import compute_snapshot_hash


def _make_event(event_id="evt-001", event_class="Observation"):
    return {
        "event_id": event_id,
        "event_class": event_class,
        "event_type": "test.observation",
        "schema_version": "0.1",
        "source_component": "Construction_Intelligence_Workers",
        "source_repo": "Construction_Intelligence_Workers",
        "timestamp": "2026-03-22T00:00:00+00:00",
        "payload": {"key": "value"},
    }


class TestDeterministicHashing(unittest.TestCase):
    def test_same_input_same_hash(self):
        """Identical entries produce the same content hash."""
        entries = [{"a": 1}, {"b": 2}]
        h1 = compute_snapshot_hash(entries)
        h2 = compute_snapshot_hash(entries)
        self.assertEqual(h1, h2)

    def test_different_input_different_hash(self):
        """Different entries produce different hashes."""
        h1 = compute_snapshot_hash([{"a": 1}])
        h2 = compute_snapshot_hash([{"a": 2}])
        self.assertNotEqual(h1, h2)

    def test_order_matters(self):
        """Entry order affects the hash."""
        h1 = compute_snapshot_hash([{"a": 1}, {"b": 2}])
        h2 = compute_snapshot_hash([{"b": 2}, {"a": 1}])
        self.assertNotEqual(h1, h2)

    def test_hash_is_hex_sha256(self):
        """Hash is a 64-char hex string (SHA-256)."""
        h = compute_snapshot_hash([])
        self.assertEqual(len(h), 64)
        int(h, 16)  # must be valid hex


class TestSnapshotCompile(unittest.TestCase):
    def test_empty_input_produces_valid_snapshot(self):
        """Empty event list produces a valid empty snapshot."""
        compiler = FreezeCompiler()
        snapshot = compiler.compile([])
        self.assertTrue(snapshot["frozen"])
        self.assertEqual(snapshot["entry_count"], 0)
        self.assertEqual(snapshot["entries"], [])
        self.assertIn("snapshot_id", snapshot)
        self.assertIn("content_hash", snapshot)
        self.assertEqual(snapshot["source_summary"]["total_events"], 0)

    def test_single_event_compiles(self):
        """A single event compiles into a snapshot with one entry."""
        compiler = FreezeCompiler()
        snapshot = compiler.compile([_make_event()])
        self.assertEqual(snapshot["entry_count"], 1)
        self.assertEqual(snapshot["entries"][0]["event_id"], "evt-001")

    def test_multiple_events_compile(self):
        """Multiple events compile correctly with accurate summaries."""
        compiler = FreezeCompiler()
        events = [
            _make_event("evt-001", "Observation"),
            _make_event("evt-002", "Proposal"),
            _make_event("evt-003", "Observation"),
        ]
        snapshot = compiler.compile(events)
        self.assertEqual(snapshot["entry_count"], 3)
        summary = snapshot["source_summary"]
        self.assertEqual(summary["total_events"], 3)
        self.assertEqual(summary["by_class"]["Observation"], 2)
        self.assertEqual(summary["by_class"]["Proposal"], 1)

    def test_snapshot_content_hash_matches_entries(self):
        """Snapshot content_hash matches recomputed hash of entries."""
        compiler = FreezeCompiler()
        snapshot = compiler.compile([_make_event()])
        recomputed = compute_snapshot_hash(snapshot["entries"])
        self.assertEqual(snapshot["content_hash"], recomputed)


if __name__ == "__main__":
    unittest.main()
