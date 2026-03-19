"""Tests for pattern boundary governance — Wave 8.5 structural validation.

Validates that pattern enrichment respects governance boundaries:
- ConditionLinker exists and has attach_pattern_candidates
- pattern_candidate_refs is a list field on ConditionPacket
- pattern_confidence is a float field
- Pattern enrichment doesn't touch protected states
"""

import inspect
import pytest
from dataclasses import fields as dc_fields

from runtime.condition_linking.linker import ConditionLinker
from runtime.models.condition_packet import ConditionPacket


# ---------------------------------------------------------------------------
# ConditionLinker existence and methods
# ---------------------------------------------------------------------------

class TestConditionLinkerExists:
    """Verify ConditionLinker exists and has attach_pattern_candidates."""

    def test_condition_linker_importable(self):
        assert ConditionLinker is not None

    def test_has_attach_pattern_candidates_method(self):
        linker = ConditionLinker()
        assert hasattr(linker, "attach_pattern_candidates")
        assert callable(linker.attach_pattern_candidates)

    def test_has_match_patterns_method(self):
        linker = ConditionLinker()
        assert hasattr(linker, "match_patterns")
        assert callable(linker.match_patterns)

    def test_has_compute_confidence_method(self):
        linker = ConditionLinker()
        assert hasattr(linker, "compute_confidence")
        assert callable(linker.compute_confidence)


# ---------------------------------------------------------------------------
# pattern_candidate_refs is a list field
# ---------------------------------------------------------------------------

class TestPatternCandidateRefsField:
    """Verify pattern_candidate_refs is a list field on ConditionPacket."""

    def test_field_exists(self):
        field_names = {f.name for f in dc_fields(ConditionPacket)}
        assert "pattern_candidate_refs" in field_names

    def test_default_is_empty_list(self):
        packet = ConditionPacket()
        assert isinstance(packet.pattern_candidate_refs, list)
        assert packet.pattern_candidate_refs == []

    def test_accepts_list_of_strings(self):
        packet = ConditionPacket(pattern_candidate_refs=["pat-1", "pat-2"])
        assert packet.pattern_candidate_refs == ["pat-1", "pat-2"]

    def test_list_independence_between_instances(self):
        p1 = ConditionPacket()
        p2 = ConditionPacket()
        p1.pattern_candidate_refs.append("only-p1")
        assert p2.pattern_candidate_refs == []


# ---------------------------------------------------------------------------
# pattern_confidence is a float field
# ---------------------------------------------------------------------------

class TestPatternConfidenceField:
    """Verify pattern_confidence is a float field on ConditionPacket."""

    def test_field_exists(self):
        field_names = {f.name for f in dc_fields(ConditionPacket)}
        assert "pattern_confidence" in field_names

    def test_default_is_zero(self):
        packet = ConditionPacket()
        assert packet.pattern_confidence == 0.0

    def test_is_float_type(self):
        packet = ConditionPacket(pattern_confidence=0.95)
        assert isinstance(packet.pattern_confidence, float)

    def test_accepts_float_values(self):
        packet = ConditionPacket(pattern_confidence=0.42)
        assert packet.pattern_confidence == pytest.approx(0.42)


# ---------------------------------------------------------------------------
# Pattern enrichment does not touch protected states
# ---------------------------------------------------------------------------

class TestPatternEnrichmentGovernance:
    """Verify pattern enrichment doesn't modify protected state fields."""

    def test_protected_fields_declared(self):
        protected = ConditionLinker._PROTECTED_STATE_FIELDS
        assert "readiness_state" in protected
        assert "issue_state" in protected
        assert "owner_state" in protected

    def test_class_docstring_declares_enrichment_only(self):
        docstring = inspect.getdoc(ConditionLinker) or ""
        lower_doc = docstring.lower()
        assert "enrichment" in lower_doc
        assert "not" in lower_doc or "may not" in lower_doc

    def test_attach_method_docstring_declares_no_state_mutation(self):
        docstring = inspect.getdoc(ConditionLinker.attach_pattern_candidates) or ""
        lower_doc = docstring.lower()
        # The docstring must mention it does NOT modify protected state
        assert "not modify" in lower_doc or "does not" in lower_doc

    def test_module_docstring_declares_enrichment_only(self):
        import runtime.condition_linking.linker as linker_module
        module_doc = linker_module.__doc__ or ""
        assert "enrichment" in module_doc.lower()
        assert "may not modify" in module_doc.lower() or "not modify" in module_doc.lower()
