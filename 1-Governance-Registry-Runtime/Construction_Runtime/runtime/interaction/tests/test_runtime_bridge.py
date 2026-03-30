"""Tests for the runtime bridge — VKBUS InteractionKernel facade."""

from runtime.interaction.runtime_bridge import (
    evaluate_condition_graph,
    resolve_detail,
    render_artifact,
    validate_state,
)
from runtime.interaction.runtime_bridge_types import (
    ChangeSet,
    ConditionGraphResult,
    DetailResult,
    ArtifactResult,
    RenderManifest,
    ResolutionContext,
    StateSnapshot,
    ValidationStateResult,
)


# ── evaluate_condition_graph ────────────────────────────────────────


class TestEvaluateConditionGraph:
    def test_empty_graph_fails_closed(self):
        result = evaluate_condition_graph(ChangeSet(graph={}))
        assert result.success is False
        assert len(result.errors) > 0

    def test_valid_graph_succeeds(self):
        graph = _minimal_valid_graph()
        result = evaluate_condition_graph(ChangeSet(graph=graph))
        assert result.success is True
        assert result.errors == ()
        assert result.node_count == 1
        assert result.edge_count == 0

    def test_missing_metadata_fails(self):
        result = evaluate_condition_graph(ChangeSet(graph={"nodes": [], "edges": []}))
        assert result.success is False
        assert any("Missing required metadata" in e for e in result.errors)

    def test_result_is_frozen(self):
        result = evaluate_condition_graph(ChangeSet(graph={}))
        assert isinstance(result, ConditionGraphResult)
        try:
            result.success = True  # type: ignore[misc]
            assert False, "Should raise FrozenInstanceError"
        except AttributeError:
            pass


# ── resolve_detail ──────────────────────────────────────────────────


class TestResolveDetail:
    def test_empty_condition_fails_closed(self):
        result = resolve_detail(ResolutionContext(condition={}))
        assert result.resolved is False
        assert len(result.errors) > 0

    def test_result_is_frozen(self):
        result = resolve_detail(ResolutionContext(condition={}))
        assert isinstance(result, DetailResult)
        try:
            result.resolved = True  # type: ignore[misc]
            assert False, "Should raise FrozenInstanceError"
        except AttributeError:
            pass


# ── render_artifact ─────────────────────────────────────────────────


class TestRenderArtifact:
    def test_empty_manifest_fails_closed(self):
        result = render_artifact(RenderManifest(condition={}))
        assert result.success is False
        assert len(result.errors) > 0

    def test_result_is_frozen(self):
        result = render_artifact(RenderManifest(condition={}))
        assert isinstance(result, ArtifactResult)
        try:
            result.success = True  # type: ignore[misc]
            assert False, "Should raise FrozenInstanceError"
        except AttributeError:
            pass


# ── validate_state ──────────────────────────────────────────────────


class TestValidateState:
    def test_empty_kind_fails(self):
        result = validate_state(StateSnapshot(kind="", payload={}))
        assert result.valid is False

    def test_empty_payload_fails(self):
        result = validate_state(StateSnapshot(kind="condition_graph", payload={}))
        assert result.valid is False

    def test_unknown_kind_fails(self):
        result = validate_state(StateSnapshot(kind="unknown_thing", payload={"a": 1}))
        assert result.valid is False
        assert any("Unknown state kind" in e for e in result.errors)

    def test_condition_graph_kind_delegates(self):
        graph = _minimal_valid_graph()
        result = validate_state(StateSnapshot(kind="condition_graph", payload=graph))
        assert result.valid is True

    def test_drawing_input_kind_delegates(self):
        condition = {
            "condition_id": "C-001",
            "assembly_type": "LOW_SLOPE",
            "interface_type": "PARAPET",
            "material_references": {"membrane": "epdm_membrane"},
            "view_intent": {
                "view_intent_type": "detail_section",
                "representation_depth": "full",
            },
        }
        result = validate_state(StateSnapshot(kind="drawing_input", payload=condition))
        assert result.valid is True

    def test_drawing_input_missing_fields(self):
        result = validate_state(StateSnapshot(kind="drawing_input", payload={"foo": "bar"}))
        assert result.valid is False

    def test_result_is_frozen(self):
        result = validate_state(StateSnapshot(kind="", payload={}))
        assert isinstance(result, ValidationStateResult)
        try:
            result.valid = True  # type: ignore[misc]
            assert False, "Should raise FrozenInstanceError"
        except AttributeError:
            pass


# ── Helpers ─────────────────────────────────────────────────────────


def _minimal_valid_graph() -> dict:
    return {
        "graph_id": "G-001",
        "source_refs": ["test"],
        "build_timestamp": "2026-01-01T00:00:00Z",
        "contract_version": "1.0",
        "checksum": "abc123",
        "nodes": [
            {
                "node_id": "N-001",
                "condition_type": "ROOF_FIELD",
                "label": "Main roof",
                "position_ref": "",
            },
        ],
        "edges": [],
    }
