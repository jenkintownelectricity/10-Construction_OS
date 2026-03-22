"""Tests for the admission gate."""

import os
import shutil
import unittest

from bus.admission_gate import receive_event
from bus.config import BASE_DIR, MAX_PAYLOAD_BYTES


EVENTS_DIR = os.path.join(BASE_DIR, "state", "events")
REJECTIONS_DIR = os.path.join(BASE_DIR, "state", "rejections")


def _clean_state():
    for d in (EVENTS_DIR, REJECTIONS_DIR):
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, ".gitkeep"), "a").close()


def _valid_event(**overrides):
    event = {
        "event_id": "evt-001",
        "event_class": "Observation",
        "event_type": "sensor_reading",
        "schema_version": "0.1",
        "source_component": "Construction_Intelligence_Workers",
        "source_repo": "Construction_Intelligence_Workers",
        "timestamp": "2026-03-22T00:00:00+00:00",
        "payload": {"temperature": 72.5},
    }
    event.update(overrides)
    return event


class TestAdmissionGate(unittest.TestCase):

    def setUp(self):
        _clean_state()

    def tearDown(self):
        _clean_state()

    def test_valid_event_admitted(self):
        result = receive_event(_valid_event())
        self.assertTrue(result["admitted"])
        self.assertEqual(result["reason"], "admitted")
        self.assertIn("admission_path", result)
        self.assertIn("content_hash", result)
        self.assertIn("routing", result)

    def test_none_event_rejected(self):
        result = receive_event(None)
        self.assertFalse(result["admitted"])

    def test_missing_required_field_rejected(self):
        for field in ("event_id", "event_class", "schema_version",
                       "source_component", "source_repo", "timestamp", "payload"):
            event = _valid_event()
            del event[field]
            result = receive_event(event)
            self.assertFalse(result["admitted"], f"should reject missing {field}")

    def test_empty_required_field_rejected(self):
        event = _valid_event(event_id="")
        result = receive_event(event)
        self.assertFalse(result["admitted"])

    def test_invalid_schema_version_rejected(self):
        result = receive_event(_valid_event(schema_version="9.9"))
        self.assertFalse(result["admitted"])

    def test_invalid_event_class_rejected(self):
        result = receive_event(_valid_event(event_class="UnknownClass"))
        self.assertFalse(result["admitted"])
        self.assertIn("invalid event_class", result["reason"])

    def test_unknown_emitter_rejected(self):
        result = receive_event(_valid_event(source_component="UnknownService"))
        self.assertFalse(result["admitted"])
        self.assertIn("not in allowed set", result["reason"])

    def test_assistant_emitter_denied(self):
        result = receive_event(_valid_event(source_component="Construction_Assistant"))
        self.assertFalse(result["admitted"])
        self.assertIn("explicitly denied", result["reason"])

    def test_oversize_payload_rejected(self):
        big_payload = {"data": "x" * (MAX_PAYLOAD_BYTES + 1)}
        result = receive_event(_valid_event(payload=big_payload))
        self.assertFalse(result["admitted"])
        self.assertIn("exceeds size limit", result["reason"])

    def test_externally_validated_requires_authority(self):
        event = _valid_event(event_class="ExternallyValidatedEvent")
        result = receive_event(event)
        self.assertFalse(result["admitted"])
        self.assertIn("authority_status", result["reason"])

    def test_externally_validated_with_authority_admitted(self):
        event = _valid_event(
            event_id="evt-ext-001",
            event_class="ExternallyValidatedEvent",
            authority_status="validated by Construction_Kernel",
        )
        result = receive_event(event)
        self.assertTrue(result["admitted"])

    def test_routing_observation(self):
        result = receive_event(_valid_event())
        self.assertEqual(result["routing"]["targets"], ["diagnostics"])

    def test_routing_proposal(self):
        result = receive_event(_valid_event(event_id="evt-prop-001", event_class="Proposal"))
        self.assertIn("awareness_cache", result["routing"]["targets"])
        self.assertIn("diagnostics", result["routing"]["targets"])


if __name__ == "__main__":
    unittest.main()
