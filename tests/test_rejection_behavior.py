"""Tests for rejection logging behavior."""

import os
import shutil
import unittest

from bus.admission_gate import receive_event
from bus.config import BASE_DIR
from bus.rejection_log import list_rejection_files, read_rejection_record


EVENTS_DIR = os.path.join(BASE_DIR, "state", "events")
REJECTIONS_DIR = os.path.join(BASE_DIR, "state", "rejections")


def _clean_state():
    for d in (EVENTS_DIR, REJECTIONS_DIR):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, ".gitkeep"), "a").close()


class TestRejectionBehavior(unittest.TestCase):

    def setUp(self):
        _clean_state()

    def tearDown(self):
        _clean_state()

    def test_rejected_event_logged(self):
        receive_event({"event_id": "bad"})
        files = list_rejection_files()
        self.assertEqual(len(files), 1)

    def test_rejection_record_contains_reason(self):
        receive_event(None)
        files = list_rejection_files()
        record = read_rejection_record(files[0])
        self.assertIn("rejection_reason", record)
        self.assertIn("rejection_timestamp", record)

    def test_rejection_record_contains_original_event(self):
        bad_event = {"event_id": "bad-002", "event_class": "Observation"}
        receive_event(bad_event)
        files = list_rejection_files()
        record = read_rejection_record(files[0])
        self.assertEqual(record["event"]["event_id"], "bad-002")

    def test_multiple_rejections_all_logged(self):
        for i in range(5):
            receive_event({"event_id": f"bad-{i}"})
        files = list_rejection_files()
        self.assertEqual(len(files), 5)


if __name__ == "__main__":
    unittest.main()
