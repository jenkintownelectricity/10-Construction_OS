"""Tests for the full thaw -> ingest -> validate -> compile -> freeze cycle."""

import json
import os
import shutil
import tempfile
import unittest

from awareness.thaw_manager import ThawManager, ThawError
from awareness.ingest_pipeline import IngestPipeline
from awareness.validation_gate import ValidationGate
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


def _make_admission_record(event_id="evt-001", event_class="Observation"):
    return {
        "record_type": "admitted",
        "event": _make_event(event_id, event_class),
        "content_hash": "abc123",
        "admission_timestamp": "2026-03-22T00:00:00+00:00",
        "admission_decision": "admitted",
    }


class TestThawCycle(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        self._events_dir = os.path.join(self._tmpdir, "events")
        self._snapshots_dir = os.path.join(self._tmpdir, "snapshots")
        os.makedirs(self._events_dir)
        os.makedirs(self._snapshots_dir)

    def tearDown(self):
        shutil.rmtree(self._tmpdir)

    def test_full_lifecycle(self):
        """Full thaw -> ingest -> validate -> compile -> freeze cycle."""
        # Write an admission record
        record = _make_admission_record()
        with open(os.path.join(self._events_dir, "001.json"), "w") as f:
            json.dump(record, f)

        # Thaw
        mgr = ThawManager()
        mgr.thaw()
        self.assertTrue(mgr.is_thawed)

        # Ingest
        pipeline = IngestPipeline(events_dir=self._events_dir)
        events = pipeline.ingest()
        self.assertEqual(len(events), 1)

        # Validate
        gate = ValidationGate()
        valid, rejected = gate.validate(events)
        self.assertEqual(len(valid), 1)
        self.assertEqual(len(rejected), 0)

        # Add to session
        mgr.add_validated(valid)

        # Freeze
        frozen_data = mgr.freeze()
        self.assertFalse(mgr.is_thawed)
        self.assertEqual(len(frozen_data), 1)

        # Compile
        compiler = FreezeCompiler()
        snapshot = compiler.compile(frozen_data)
        self.assertTrue(snapshot["frozen"])
        self.assertEqual(snapshot["entry_count"], 1)

        # Store
        store = SnapshotStore(snapshots_dir=self._snapshots_dir)
        path = store.store(snapshot)
        self.assertTrue(os.path.isfile(path))

    def test_cannot_thaw_while_thawed(self):
        """Cannot open a second thaw session."""
        mgr = ThawManager()
        mgr.thaw()
        with self.assertRaises(ThawError):
            mgr.thaw()

    def test_cannot_freeze_without_thaw(self):
        """Cannot freeze if not thawed."""
        mgr = ThawManager()
        with self.assertRaises(ThawError):
            mgr.freeze()

    def test_cannot_add_without_thaw(self):
        """Cannot add records without an active thaw session."""
        mgr = ThawManager()
        with self.assertRaises(ThawError):
            mgr.add_validated([_make_event()])

    def test_freeze_produces_immutable_artifact(self):
        """Frozen snapshot stored to disk cannot be overwritten."""
        record = _make_admission_record()
        with open(os.path.join(self._events_dir, "001.json"), "w") as f:
            json.dump(record, f)

        mgr = ThawManager()
        mgr.thaw()
        pipeline = IngestPipeline(events_dir=self._events_dir)
        events = pipeline.ingest()
        gate = ValidationGate()
        valid, _ = gate.validate(events)
        mgr.add_validated(valid)
        frozen_data = mgr.freeze()

        compiler = FreezeCompiler()
        snapshot = compiler.compile(frozen_data)
        store = SnapshotStore(snapshots_dir=self._snapshots_dir)
        store.store(snapshot)

        # Verify the stored file is valid JSON with frozen=True
        sid = snapshot["snapshot_id"]
        path = os.path.join(self._snapshots_dir, f"{sid}.json")
        with open(path, "r") as f:
            stored = json.load(f)
        self.assertTrue(stored["frozen"])
        self.assertEqual(stored["content_hash"], snapshot["content_hash"])

    def test_skips_non_admission_records(self):
        """Ingest pipeline skips rejection records."""
        rejection = {
            "record_type": "rejected",
            "event": None,
            "rejection_timestamp": "2026-03-22T00:00:00+00:00",
            "rejection_reason": "bad",
        }
        with open(os.path.join(self._events_dir, "001.json"), "w") as f:
            json.dump(rejection, f)

        pipeline = IngestPipeline(events_dir=self._events_dir)
        events = pipeline.ingest()
        self.assertEqual(len(events), 0)


if __name__ == "__main__":
    unittest.main()
