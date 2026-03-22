"""Tests for replay reader."""

import json
import os
import shutil
import unittest

from bus.admission_gate import receive_event
from bus.config import BASE_DIR, EVENTS_DIR
from bus.replay import replay


REJECTIONS_DIR = os.path.join(BASE_DIR, "state", "rejections")


def _clean_state():
    for d in (EVENTS_DIR, REJECTIONS_DIR):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, ".gitkeep"), "a").close()


def _valid_event(event_id="evt-r-001", event_class="Observation", source_component="Construction_Intelligence_Workers"):
    return {
        "event_id": event_id,
        "event_class": event_class,
        "event_type": "test_event",
        "schema_version": "0.1",
        "source_component": source_component,
        "source_repo": source_component,
        "timestamp": "2026-03-22T00:00:00+00:00",
        "payload": {"data": event_id},
    }


class TestReplay(unittest.TestCase):

    def setUp(self):
        _clean_state()

    def tearDown(self):
        _clean_state()

    def test_replay_deterministic_ordering(self):
        for i in range(5):
            receive_event(_valid_event(event_id=f"evt-det-{i:03d}"))
        records = replay()
        ids = [r["event"]["event_id"] for r in records]
        self.assertEqual(ids, sorted(ids))

    def test_replay_filter_by_event_class(self):
        receive_event(_valid_event(event_id="obs-1", event_class="Observation"))
        receive_event(_valid_event(event_id="prop-1", event_class="Proposal"))
        records = replay(event_class="Observation")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["event"]["event_class"], "Observation")

    def test_replay_filter_by_source_component(self):
        receive_event(_valid_event(
            event_id="w-1",
            source_component="Construction_Intelligence_Workers",
        ))
        receive_event(_valid_event(
            event_id="r-1",
            source_component="Construction_Reference_Intelligence",
        ))
        records = replay(source_component="Construction_Reference_Intelligence")
        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0]["event"]["source_component"],
            "Construction_Reference_Intelligence",
        )

    def test_replay_empty_log(self):
        records = replay()
        self.assertEqual(records, [])

    def test_malformed_record_fails_closed(self):
        os.makedirs(EVENTS_DIR, exist_ok=True)
        bad_path = os.path.join(EVENTS_DIR, "bad-record.json")
        with open(bad_path, "w") as f:
            f.write("NOT VALID JSON{{{")
        with self.assertRaises(RuntimeError):
            replay()

    def test_malformed_structure_fails_closed(self):
        os.makedirs(EVENTS_DIR, exist_ok=True)
        bad_path = os.path.join(EVENTS_DIR, "bad-struct.json")
        with open(bad_path, "w") as f:
            json.dump({"no_event_key": True}, f)
        with self.assertRaises(RuntimeError):
            replay()


if __name__ == "__main__":
    unittest.main()
