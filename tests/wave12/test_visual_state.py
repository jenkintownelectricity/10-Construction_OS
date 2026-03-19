"""Tests for VisualStateMapper — readiness-to-visual state mapping."""

import pytest

from runtime.navigation_state.visual_state import VisualStateMapper


@pytest.fixture()
def vsm():
    return VisualStateMapper()


class TestKnownStatesMapCorrectly:
    def test_known_states_map_correctly(self, vsm):
        assert vsm.map_readiness_to_visual("ready") == "ready"
        assert vsm.map_readiness_to_visual("pending") == "pending"
        assert vsm.map_readiness_to_visual("blocked") == "blocked"
        assert vsm.map_readiness_to_visual("completed") == "completed"

    def test_resolved_maps_to_completed(self, vsm):
        assert vsm.map_readiness_to_visual("resolved") == "completed"

    def test_in_progress_maps_to_pending(self, vsm):
        assert vsm.map_readiness_to_visual("in_progress") == "pending"


class TestUnknownStateExplicit:
    def test_none_maps_to_unknown(self, vsm):
        assert vsm.map_readiness_to_visual(None) == "unknown"

    def test_empty_string_maps_to_unknown(self, vsm):
        assert vsm.map_readiness_to_visual("") == "unknown"

    def test_unrecognised_state_maps_to_unknown(self, vsm):
        assert vsm.map_readiness_to_visual("nonexistent_state") == "unknown"


class TestVisualStatesAreComplete:
    def test_visual_states_are_complete(self, vsm):
        expected = {"ready", "pending", "blocked", "completed", "unknown"}
        assert vsm.VISUAL_STATES == expected

    def test_all_five_states_reachable(self, vsm):
        """Verify that all 5 visual states can actually be reached."""
        reachable = set()
        reachable.add(vsm.map_readiness_to_visual("ready"))
        reachable.add(vsm.map_readiness_to_visual("pending"))
        reachable.add(vsm.map_readiness_to_visual("blocked"))
        reachable.add(vsm.map_readiness_to_visual("completed"))
        reachable.add(vsm.map_readiness_to_visual(None))
        assert reachable == {"ready", "pending", "blocked", "completed", "unknown"}


class TestMapReadinessChainToVisual:
    def test_ready_chain(self, vsm):
        assert vsm.map_readiness_chain_to_visual(
            {"ready": True, "blockers": [], "dependencies_met": True}
        ) == "ready"

    def test_blocked_chain(self, vsm):
        assert vsm.map_readiness_chain_to_visual(
            {"ready": False, "blockers": ["blk"], "dependencies_met": True}
        ) == "blocked"

    def test_pending_chain(self, vsm):
        assert vsm.map_readiness_chain_to_visual(
            {"ready": False, "blockers": [], "dependencies_met": False}
        ) == "pending"

    def test_non_dict_returns_unknown(self, vsm):
        assert vsm.map_readiness_chain_to_visual("not_a_dict") == "unknown"


class TestAnnotateWithVisualState:
    def test_annotate_adds_visual_state(self, vsm):
        node = {"state_summary": {"status": "ready"}, "is_enrichment_derived": False}
        result = vsm.annotate_with_visual_state(node)
        assert result["visual_state"] == "ready"
        assert result["visual_state_source"] == "hard_fact"
        # Original not mutated
        assert "visual_state" not in node

    def test_annotate_enrichment_source(self, vsm):
        node = {"state_summary": {"status": "pending"}, "is_enrichment_derived": True}
        result = vsm.annotate_with_visual_state(node)
        assert result["visual_state"] == "pending"
        assert result["visual_state_source"] == "enrichment"
