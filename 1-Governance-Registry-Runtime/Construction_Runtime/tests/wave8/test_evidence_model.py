"""Tests for evidence and candidate object models — Wave 8A structural validation."""

import pytest
from dataclasses import fields

from runtime.models.evidence_model import EvidenceRecord, CandidateObject


# ---------------------------------------------------------------------------
# EvidenceRecord
# ---------------------------------------------------------------------------

class TestEvidenceRecordFields:
    """Verify EvidenceRecord has all required fields."""

    REQUIRED_FIELDS = [
        "evidence_id",
        "source_document",
        "extraction_method",
        "confidence",
        "extracted_entities",
        "source_page",
        "source_section",
        "timestamp",
    ]

    def test_all_required_fields_present(self):
        field_names = {f.name for f in fields(EvidenceRecord)}
        for name in self.REQUIRED_FIELDS:
            assert name in field_names, f"EvidenceRecord missing field: {name}"

    def test_source_document_present(self):
        record = EvidenceRecord(source_document="specs/section-05.pdf")
        assert record.source_document == "specs/section-05.pdf"

    def test_extraction_method_present(self):
        record = EvidenceRecord(extraction_method="table_extraction")
        assert record.extraction_method == "table_extraction"

    def test_confidence_is_float(self):
        record = EvidenceRecord(confidence=0.87)
        assert isinstance(record.confidence, float)
        assert record.confidence == 0.87


class TestEvidenceTraceability:
    """Verify that evidence records support traceability requirements."""

    def test_source_document_field_exists(self):
        record = EvidenceRecord()
        assert hasattr(record, "source_document")

    def test_extraction_method_field_exists(self):
        record = EvidenceRecord()
        assert hasattr(record, "extraction_method")

    def test_source_page_field_exists(self):
        record = EvidenceRecord()
        assert hasattr(record, "source_page")

    def test_source_section_field_exists(self):
        record = EvidenceRecord()
        assert hasattr(record, "source_section")


# ---------------------------------------------------------------------------
# CandidateObject
# ---------------------------------------------------------------------------

class TestCandidateObjectFields:
    """Verify CandidateObject has confidence and source_evidence_refs."""

    def test_confidence_field_present(self):
        candidate = CandidateObject()
        assert hasattr(candidate, "confidence")

    def test_confidence_is_float(self):
        candidate = CandidateObject(confidence=0.75)
        assert isinstance(candidate.confidence, float)

    def test_source_evidence_refs_present(self):
        candidate = CandidateObject()
        assert hasattr(candidate, "source_evidence_refs")

    def test_source_evidence_refs_is_list(self):
        candidate = CandidateObject(source_evidence_refs=["ev-1", "ev-2"])
        assert candidate.source_evidence_refs == ["ev-1", "ev-2"]


class TestCandidateNonCanonical:
    """Verify candidates are non-canonical by default (resolved=False)."""

    def test_default_resolved_is_false(self):
        candidate = CandidateObject()
        assert candidate.resolved is False

    def test_resolved_can_be_set_true(self):
        candidate = CandidateObject(resolved=True)
        assert candidate.resolved is True

    def test_candidate_type_defaults_to_empty(self):
        candidate = CandidateObject()
        assert candidate.candidate_type == ""
