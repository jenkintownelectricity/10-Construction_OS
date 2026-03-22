"""Tests for worker event submission through the Cognitive Bus.

Validates that valid events are admitted, invalid events are rejected,
and workers cannot emit ExternallyValidatedEvent through the bus.
"""

import glob
import os
import sys
import unittest

# Ensure both repos are importable.
sys.path.insert(0, "/home/user/Construction_Intelligence_Workers")
sys.path.insert(0, "/home/user/Construction_Cognitive_Bus")

from workers.event_adapter import EventAdapter
from workers.observation_emitter import ObservationEmitter
from workers.proposal_emitter import ProposalEmitter
from workers.schema_builder import build_event

# State directories in the bus repo that tests may write into.
_BUS_STATE = "/home/user/Construction_Cognitive_Bus/state"
_EVENTS_DIR = os.path.join(_BUS_STATE, "events")
_REJECTIONS_DIR = os.path.join(_BUS_STATE, "rejections")


class _BusStateCleanupMixin:
    """Mixin that cleans up bus state dirs after each test,
    restoring .gitkeep files so the working tree stays clean."""

    def setUp(self):
        super().setUp()
        self._snapshot_events = set(os.listdir(_EVENTS_DIR))
        self._snapshot_rejections = set(os.listdir(_REJECTIONS_DIR))

    def tearDown(self):
        # Remove any files created during the test.
        for path in glob.glob(os.path.join(_EVENTS_DIR, "*")):
            name = os.path.basename(path)
            if name not in self._snapshot_events:
                os.remove(path)
        for path in glob.glob(os.path.join(_REJECTIONS_DIR, "*")):
            name = os.path.basename(path)
            if name not in self._snapshot_rejections:
                os.remove(path)
        # Restore .gitkeep files if they were present before.
        for d, snap in [(_EVENTS_DIR, self._snapshot_events),
                        (_REJECTIONS_DIR, self._snapshot_rejections)]:
            if ".gitkeep" in snap:
                gitkeep = os.path.join(d, ".gitkeep")
                if not os.path.exists(gitkeep):
                    open(gitkeep, "w").close()
        super().tearDown()


class TestValidObservationAdmitted(_BusStateCleanupMixin, unittest.TestCase):
    """A valid Observation event is admitted by the bus."""

    def test_observation_admitted(self):
        result = ObservationEmitter.emit(
            "material.detected", {"material": "steel", "confidence": 0.95}
        )
        self.assertTrue(result["admitted"])
        self.assertEqual(result["reason"], "admitted")


class TestValidProposalAdmitted(_BusStateCleanupMixin, unittest.TestCase):
    """A valid Proposal event is admitted by the bus."""

    def test_proposal_admitted(self):
        result = ProposalEmitter.emit(
            "assembly.suggestion", {"assembly_id": "A-001", "action": "review"}
        )
        self.assertTrue(result["admitted"])
        self.assertEqual(result["reason"], "admitted")


class TestCannotEmitExternallyValidated(_BusStateCleanupMixin, unittest.TestCase):
    """Workers cannot emit ExternallyValidatedEvent."""

    def test_schema_builder_refuses(self):
        """schema_builder raises before anything reaches the bus."""
        with self.assertRaises(ValueError):
            build_event("ExternallyValidatedEvent", "test.ext", {"data": 1})

    def test_direct_submit_rejected_by_bus(self):
        """Even if someone hand-crafts an ExternallyValidatedEvent envelope
        and submits it directly, the bus rejects it (no authority_status)."""
        import uuid
        from datetime import datetime, timezone

        crafted = {
            "event_id": str(uuid.uuid4()),
            "event_class": "ExternallyValidatedEvent",
            "event_type": "test.crafted",
            "schema_version": "0.1",
            "source_component": "Construction_Intelligence_Workers",
            "source_repo": "Construction_Intelligence_Workers",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {"data": "crafted"},
        }
        result = EventAdapter.submit(crafted)
        # Bus should reject: ExternallyValidatedEvent requires authority_status.
        self.assertFalse(result["admitted"])


class TestInvalidPayloadRejected(_BusStateCleanupMixin, unittest.TestCase):
    """Invalid payloads are rejected."""

    def test_non_dict_payload_rejected_by_builder(self):
        with self.assertRaises(ValueError):
            build_event("Observation", "test.bad", "not a dict")

    def test_empty_event_type_rejected(self):
        with self.assertRaises(ValueError):
            build_event("Observation", "", {"data": 1})

    def test_whitespace_event_type_rejected(self):
        with self.assertRaises(ValueError):
            build_event("Observation", "   ", {"data": 1})


if __name__ == "__main__":
    unittest.main()
