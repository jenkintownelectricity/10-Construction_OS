"""Doctrine compliance tests.

Verifies:
- No AI, proposal, assistant, worker, mailbox, or UI logic in event code
- Runtime remains deterministic and execution-only
- Event envelope contains no bus-owned metadata
- All five events and checkpoints exist
"""

import ast
import os
import pytest

from runtime.events.event_types import EVENT_TYPES
from runtime.events.event_builder import build_event_envelope


EVENTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "runtime", "events"
)

# Words that must not appear in runtime event code
FORBIDDEN_TERMS = [
    "proposal",
    "assistant",
    "worker",
    "mailbox",
    "ai_model",
    "llm",
    "chatbot",
    "recommendation",
    "suggest",
    "corrective_action",
    "inferred_action",
]

# Bus-owned metadata that runtime must never emit
BUS_OWNED_FIELDS = [
    "admission_decision",
    "admission_timestamp",
    "content_hash",
    "routing",
]


class TestNoCognitiveLogicInEventCode:
    """Runtime event code must contain no AI/proposal/assistant/worker logic."""

    def _get_event_source_files(self):
        files = []
        for fname in os.listdir(EVENTS_DIR):
            if fname.endswith(".py"):
                files.append(os.path.join(EVENTS_DIR, fname))
        return files

    def test_no_forbidden_terms_in_source(self):
        violations = []
        for fpath in self._get_event_source_files():
            with open(fpath) as f:
                content = f.read().lower()
            for term in FORBIDDEN_TERMS:
                if term in content:
                    violations.append(f"{os.path.basename(fpath)}: contains '{term}'")
        assert violations == [], f"Forbidden terms found: {violations}"

    def test_no_import_of_ai_modules(self):
        """Event code must not import AI/ML/assistant modules."""
        ai_modules = {"openai", "anthropic", "langchain", "transformers", "torch"}
        for fpath in self._get_event_source_files():
            with open(fpath) as f:
                try:
                    tree = ast.parse(f.read())
                except SyntaxError:
                    continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert alias.name not in ai_modules, (
                            f"{os.path.basename(fpath)} imports {alias.name}"
                        )
                elif isinstance(node, ast.ImportFrom):
                    if node.module and node.module.split(".")[0] in ai_modules:
                        pytest.fail(
                            f"{os.path.basename(fpath)} imports from {node.module}"
                        )


class TestNoBusMetadataEmitted:
    """Runtime must not emit bus-owned metadata."""

    @pytest.mark.parametrize("event_type", sorted(EVENT_TYPES))
    def test_no_bus_fields_in_envelope(self, event_type):
        env = build_event_envelope(
            event_type=event_type,
            pipeline_stage="test",
            payload={"test": True},
        )
        for field in BUS_OWNED_FIELDS:
            assert field not in env, (
                f"Bus-owned field '{field}' found in {event_type} envelope"
            )


class TestEventClassIsObservationOnly:
    """Runtime must emit only Observation-class events."""

    @pytest.mark.parametrize("event_type", sorted(EVENT_TYPES))
    def test_event_class_observation(self, event_type):
        env = build_event_envelope(
            event_type=event_type,
            pipeline_stage="test",
            payload={},
        )
        assert env["event_class"] == "Observation"


class TestAllFiveEventsExist:
    """All five required event types must be present."""

    def test_exactly_five_events(self):
        assert len(EVENT_TYPES) == 5

    def test_required_event_names(self):
        required = {
            "ConditionDetected",
            "DetailResolved",
            "ArtifactRendered",
            "ValidationFailed",
            "RuntimeError",
        }
        assert EVENT_TYPES == required


class TestDeterministicEnvelopeStructure:
    """Envelope structure must be deterministic given the same inputs."""

    def test_same_fields_every_time(self):
        """Same event type produces same set of keys."""
        keys_set = set()
        for _ in range(10):
            env = build_event_envelope(
                event_type="ConditionDetected",
                pipeline_stage="pipeline_entry",
                payload={"k": "v"},
            )
            keys_set.add(frozenset(env.keys()))
        assert len(keys_set) == 1, "Envelope key structure is non-deterministic"

    def test_source_fields_constant(self):
        for _ in range(10):
            env = build_event_envelope(
                event_type="DetailResolved",
                pipeline_stage="detail_resolution",
                payload={},
            )
            assert env["source_component"] == "Construction_Runtime"
            assert env["source_repo"] == "Construction_Runtime"
            assert env["schema_version"] == "0.1"
            assert env["event_class"] == "Observation"
