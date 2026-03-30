"""Tests for append-only event log."""

import os
import shutil
import unittest

from bus.admission_gate import receive_event
from bus.config import BASE_DIR
from bus.event_log import list_event_files, read_event_record


EVENTS_DIR = os.path.join(BASE_DIR, "state", "events")
REJECTIONS_DIR = os.path.join(BASE_DIR, "state", "rejections")


def _clean_state():
    for d in (EVENTS_DIR, REJECTIONS_DIR):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, ".gitkeep"), "a").close()


def _valid_event(event_id="evt-log-001"):
    return {
        "event_id": event_id,
        "event_class": "Observation",
        "event_type": "sensor_reading",
        "schema_version": "0.1",
        "source_component": "Construction_Intelligence_Workers",
        "source_repo": "Construction_Intelligence_Workers",
        "timestamp": "2026-03-22T00:00:00+00:00",
        "payload": {"value": 42},
    }


class TestEventLog(unittest.TestCase):

    def setUp(self):
        _clean_state()

    def tearDown(self):
        _clean_state()

    def test_admitted_event_logged(self):
        receive_event(_valid_event())
        files = list_event_files()
        self.assertEqual(len(files), 1)

    def test_event_record_readable(self):
        receive_event(_valid_event())
        files = list_event_files()
        record = read_event_record(files[0])
        self.assertEqual(record["event"]["event_id"], "evt-log-001")
        self.assertEqual(record["record_type"], "admitted")
        self.assertIn("content_hash", record)
        self.assertIn("admission_timestamp", record)

    def test_multiple_events_logged_in_order(self):
        for i in range(3):
            receive_event(_valid_event(event_id=f"evt-order-{i:03d}"))
        files = list_event_files()
        self.assertEqual(len(files), 3)
        # Files should be in sorted order
        self.assertEqual(files, sorted(files))

    def test_immutability_no_overwrite(self):
        """Admitted records are append-only; each admission creates a distinct record."""
        receive_event(_valid_event(event_id="evt-imm-001"))
        receive_event(_valid_event(event_id="evt-imm-002"))
        files = list_event_files()
        self.assertEqual(len(files), 2)
        r1 = read_event_record(files[0])
        r2 = read_event_record(files[1])
        self.assertNotEqual(r1["admission_timestamp"], r2["admission_timestamp"])


if __name__ == "__main__":
    unittest.main()
