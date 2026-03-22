"""Tests for snapshot reader behavior: read-only, fail closed, frozen only."""

import json
import os
import shutil
import tempfile
import unittest

from awareness.snapshot_reader import SnapshotReader, SnapshotReadError
from awareness.freeze_compiler import FreezeCompiler
from awareness.snapshot_store import SnapshotStore


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


class TestReaderReturnsFrozenSnapshots(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._snapshots_dir = os.path.join(self._tmpdir, "snapshots")
        os.makedirs(self._snapshots_dir)

    def tearDown(self):
        shutil.rmtree(self._tmpdir)

    def test_reader_returns_frozen_snapshot(self):
        """Reader returns a valid frozen snapshot by ID."""
        compiler = FreezeCompiler()
        snapshot = compiler.compile([_make_event()])

        store = SnapshotStore(snapshots_dir=self._snapshots_dir)
        store.store(snapshot)

        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        result = reader.get(snapshot["snapshot_id"])
        self.assertTrue(result["frozen"])
        self.assertEqual(result["snapshot_id"], snapshot["snapshot_id"])
        self.assertEqual(result["content_hash"], snapshot["content_hash"])
        self.assertEqual(result["entry_count"], 1)

    def test_list_snapshots(self):
        """Reader lists all available snapshot IDs."""
        compiler = FreezeCompiler()
        store = SnapshotStore(snapshots_dir=self._snapshots_dir)

        s1 = compiler.compile([_make_event("evt-001")])
        s2 = compiler.compile([_make_event("evt-002")])
        store.store(s1)
        store.store(s2)

        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        ids = reader.list_snapshots()
        self.assertEqual(len(ids), 2)
        self.assertIn(s1["snapshot_id"], ids)
        self.assertIn(s2["snapshot_id"], ids)

    def test_list_empty_dir(self):
        """Reader returns empty list when no snapshots exist."""
        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        self.assertEqual(reader.list_snapshots(), [])

    def test_list_nonexistent_dir(self):
        """Reader returns empty list for nonexistent directory."""
        reader = SnapshotReader(
            snapshots_dir=os.path.join(self._tmpdir, "nope")
        )
        self.assertEqual(reader.list_snapshots(), [])


class TestReaderFailsClosed(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._snapshots_dir = os.path.join(self._tmpdir, "snapshots")
        os.makedirs(self._snapshots_dir)

    def tearDown(self):
        shutil.rmtree(self._tmpdir)

    def test_fails_on_missing_snapshot(self):
        """Reader raises on nonexistent snapshot ID."""
        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        with self.assertRaises(SnapshotReadError):
            reader.get("does-not-exist")

    def test_fails_on_malformed_json(self):
        """Reader raises on file with invalid JSON."""
        path = os.path.join(self._snapshots_dir, "bad.json")
        with open(path, "w") as f:
            f.write("{not valid json")
        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        with self.assertRaises(SnapshotReadError):
            reader.get("bad")

    def test_fails_on_non_dict(self):
        """Reader raises when file contains a non-dict JSON value."""
        path = os.path.join(self._snapshots_dir, "array.json")
        with open(path, "w") as f:
            json.dump([1, 2, 3], f)
        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        with self.assertRaises(SnapshotReadError):
            reader.get("array")

    def test_fails_on_unfrozen_snapshot(self):
        """Reader raises when snapshot has frozen=False."""
        path = os.path.join(self._snapshots_dir, "unfrozen.json")
        with open(path, "w") as f:
            json.dump({
                "snapshot_id": "unfrozen",
                "frozen": False,
                "entries": [],
            }, f)
        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        with self.assertRaises(SnapshotReadError):
            reader.get("unfrozen")

    def test_fails_on_id_mismatch(self):
        """Reader raises when snapshot_id in file doesn't match filename."""
        path = os.path.join(self._snapshots_dir, "claimed-id.json")
        with open(path, "w") as f:
            json.dump({
                "snapshot_id": "different-id",
                "frozen": True,
                "entries": [],
            }, f)
        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        with self.assertRaises(SnapshotReadError):
            reader.get("claimed-id")


class TestReaderIsReadOnly(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._snapshots_dir = os.path.join(self._tmpdir, "snapshots")
        os.makedirs(self._snapshots_dir)

    def tearDown(self):
        shutil.rmtree(self._tmpdir)

    def test_reader_has_no_write_methods(self):
        """SnapshotReader exposes no store, delete, or update methods."""
        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        self.assertFalse(hasattr(reader, "store"))
        self.assertFalse(hasattr(reader, "delete"))
        self.assertFalse(hasattr(reader, "update"))
        self.assertFalse(hasattr(reader, "write"))

    def test_reading_does_not_modify_file(self):
        """Reading a snapshot does not alter the file on disk."""
        compiler = FreezeCompiler()
        snapshot = compiler.compile([_make_event()])
        store = SnapshotStore(snapshots_dir=self._snapshots_dir)
        store.store(snapshot)

        path = os.path.join(
            self._snapshots_dir, f"{snapshot['snapshot_id']}.json"
        )
        with open(path, "r") as f:
            before = f.read()

        reader = SnapshotReader(snapshots_dir=self._snapshots_dir)
        reader.get(snapshot["snapshot_id"])

        with open(path, "r") as f:
            after = f.read()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
