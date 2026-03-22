"""Tests for Runtime-to-Cognitive-Bus adapter."""

import pytest

from runtime.events.bus_adapter import CognitiveBusAdapter, BusPublicationError
from runtime.events.event_builder import build_event_envelope


def _make_event(event_type="ConditionDetected"):
    return build_event_envelope(
        event_type=event_type,
        pipeline_stage="pipeline_entry",
        payload={"condition_signature_id": "CS-001"},
    )


class TestBusAdapterSuccess:
    """Verify successful publication path."""

    def test_publish_with_admitted_result(self):
        def mock_bus(event):
            return {"admitted": True, "reason": "admitted", "content_hash": "abc"}

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        result = adapter.publish(_make_event())
        assert result["admitted"] is True

    def test_result_passed_through(self):
        expected = {"admitted": True, "reason": "admitted", "routing": {"targets": ["diagnostics"]}}

        def mock_bus(event):
            return expected

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        result = adapter.publish(_make_event())
        assert result == expected


class TestBusAdapterFailClosed:
    """Verify fail-closed behavior on all failure modes."""

    def test_rejection_raises(self):
        def mock_bus(event):
            return {"admitted": False, "reason": "emitter not in allowed set"}

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        with pytest.raises(BusPublicationError, match="rejected"):
            adapter.publish(_make_event())

    def test_exception_in_bus_raises(self):
        def mock_bus(event):
            raise ConnectionError("bus unavailable")

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        with pytest.raises(BusPublicationError, match="ConnectionError"):
            adapter.publish(_make_event())

    def test_non_dict_result_raises(self):
        def mock_bus(event):
            return "not a dict"

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        with pytest.raises(BusPublicationError, match="non-dict"):
            adapter.publish(_make_event())

    def test_none_result_raises(self):
        def mock_bus(event):
            return None

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        with pytest.raises(BusPublicationError, match="non-dict"):
            adapter.publish(_make_event())

    def test_missing_admitted_key_raises(self):
        def mock_bus(event):
            return {"reason": "no admitted field"}

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        with pytest.raises(BusPublicationError):
            adapter.publish(_make_event())

    def test_bus_import_failure_raises(self):
        adapter = CognitiveBusAdapter()  # no mock, no bus module available
        with pytest.raises(BusPublicationError, match="not available"):
            adapter.publish(_make_event())

    def test_error_preserves_event_type(self):
        def mock_bus(event):
            return {"admitted": False, "reason": "denied"}

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        with pytest.raises(BusPublicationError) as exc_info:
            adapter.publish(_make_event("ValidationFailed"))
        assert exc_info.value.event_type == "ValidationFailed"

    def test_error_preserves_event_data(self):
        def mock_bus(event):
            raise RuntimeError("boom")

        adapter = CognitiveBusAdapter(publish_fn=mock_bus)
        with pytest.raises(BusPublicationError) as exc_info:
            adapter.publish(_make_event())
        assert exc_info.value.event is not None
