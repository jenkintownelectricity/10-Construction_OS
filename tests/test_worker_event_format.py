"""Tests for worker event envelope format and constraints.

Validates that built envelopes match the Cognitive Bus schema,
that only Observation and Proposal are allowed, and that payload
limits are enforced.
"""

import sys
import unittest

# Workers package is in the parent directory.
sys.path.insert(0, "/home/user/Construction_Intelligence_Workers")

from workers.schema_builder import MAX_PAYLOAD_BYTES, build_event


REQUIRED_FIELDS = {
    "event_id",
    "event_class",
    "event_type",
    "schema_version",
    "source_component",
    "source_repo",
    "timestamp",
    "payload",
}


class TestEventEnvelopeFormat(unittest.TestCase):
    """Event envelope has all required fields."""

    def test_observation_has_all_required_fields(self):
        event = build_event("Observation", "test.signal", {"key": "value"})
        self.assertTrue(REQUIRED_FIELDS.issubset(event.keys()))

    def test_proposal_has_all_required_fields(self):
        event = build_event("Proposal", "test.proposal", {"key": "value"})
        self.assertTrue(REQUIRED_FIELDS.issubset(event.keys()))


class TestObservationEventClass(unittest.TestCase):
    """Observation events have correct event_class."""

    def test_observation_event_class(self):
        event = build_event("Observation", "test.signal", {"data": 1})
        self.assertEqual(event["event_class"], "Observation")


class TestProposalEventClass(unittest.TestCase):
    """Proposal events have correct event_class."""

    def test_proposal_event_class(self):
        event = build_event("Proposal", "test.proposal", {"data": 1})
        self.assertEqual(event["event_class"], "Proposal")


class TestExternallyValidatedEventDenied(unittest.TestCase):
    """ExternallyValidatedEvent cannot be built by workers."""

    def test_externally_validated_event_refused(self):
        with self.assertRaises(ValueError) as ctx:
            build_event("ExternallyValidatedEvent", "test.ext", {"data": 1})
        self.assertIn("must not emit", str(ctx.exception))


class TestPayloadSizeLimit(unittest.TestCase):
    """Payload size limit is enforced."""

    def test_oversized_payload_rejected(self):
        # Build a payload that exceeds 64 KiB.
        big_payload = {"data": "x" * (MAX_PAYLOAD_BYTES + 1)}
        with self.assertRaises(ValueError) as ctx:
            build_event("Observation", "test.big", big_payload)
        self.assertIn("exceeds size limit", str(ctx.exception))

    def test_valid_payload_accepted(self):
        event = build_event("Observation", "test.ok", {"data": "small"})
        self.assertIsInstance(event, dict)


class TestEventIdUniqueness(unittest.TestCase):
    """Each event gets a unique event_id."""

    def test_event_ids_are_unique(self):
        events = [
            build_event("Observation", "test.unique", {"i": i})
            for i in range(10)
        ]
        ids = [e["event_id"] for e in events]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
