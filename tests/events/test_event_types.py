"""Tests for runtime event type constants."""

from runtime.events.event_types import (
    ConditionDetected,
    DetailResolved,
    ArtifactRendered,
    ValidationFailed,
    RuntimeError,
    EVENT_TYPES,
)


class TestEventTypeConstants:
    """Verify the five required event types exist with exact names."""

    def test_condition_detected_name(self):
        assert ConditionDetected == "ConditionDetected"

    def test_detail_resolved_name(self):
        assert DetailResolved == "DetailResolved"

    def test_artifact_rendered_name(self):
        assert ArtifactRendered == "ArtifactRendered"

    def test_validation_failed_name(self):
        assert ValidationFailed == "ValidationFailed"

    def test_runtime_error_name(self):
        assert RuntimeError == "RuntimeError"

    def test_exactly_five_event_types(self):
        assert len(EVENT_TYPES) == 5

    def test_all_required_types_in_set(self):
        expected = {
            "ConditionDetected",
            "DetailResolved",
            "ArtifactRendered",
            "ValidationFailed",
            "RuntimeError",
        }
        assert EVENT_TYPES == expected

    def test_event_types_frozen(self):
        """EVENT_TYPES must be immutable."""
        assert isinstance(EVENT_TYPES, frozenset)
