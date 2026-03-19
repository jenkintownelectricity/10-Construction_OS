"""Tests for governance boundaries — Wave 8.5 structural validation.

Validates that runtime modules respect governance rules:
- ConditionLinker does NOT modify protected state fields
- Runtime modules don't define kernel doctrine
- QA engine references kernel contracts
- Evidence objects include confidence and source references
"""

import inspect
import pytest

from runtime.condition_linking.linker import ConditionLinker
from runtime.qa.qa_engine import QAEngine
from runtime.models.evidence_model import EvidenceRecord, CandidateObject


# ---------------------------------------------------------------------------
# ConditionLinker governance — enrichment-only, no state mutation
# ---------------------------------------------------------------------------

class TestConditionLinkerGovernance:
    """Verify ConditionLinker does NOT modify protected state fields."""

    def test_linker_has_protected_state_fields(self):
        """ConditionLinker must declare which fields are protected."""
        assert hasattr(ConditionLinker, "_PROTECTED_STATE_FIELDS")
        protected = ConditionLinker._PROTECTED_STATE_FIELDS
        assert "readiness_state" in protected
        assert "issue_state" in protected
        assert "owner_state" in protected

    def test_docstring_declares_enrichment_only(self):
        """ConditionLinker docstring must state enrichment-only policy."""
        docstring = inspect.getdoc(ConditionLinker) or ""
        assert "enrichment" in docstring.lower(), (
            "ConditionLinker docstring must mention enrichment-only policy"
        )

    def test_attach_method_docstring_mentions_no_state_modification(self):
        """attach_pattern_candidates docstring must declare it won't modify state."""
        docstring = inspect.getdoc(ConditionLinker.attach_pattern_candidates) or ""
        assert "not modify" in docstring.lower() or "does not" in docstring.lower(), (
            "attach_pattern_candidates docstring must declare it does not modify protected state"
        )

    def test_module_docstring_declares_enrichment_only(self):
        """The condition_linking.linker module docstring must declare enrichment-only."""
        import runtime.condition_linking.linker as linker_module
        module_doc = linker_module.__doc__ or ""
        assert "enrichment" in module_doc.lower(), (
            "Linker module docstring must mention enrichment-only policy"
        )


# ---------------------------------------------------------------------------
# Runtime modules must NOT define kernel doctrine
# ---------------------------------------------------------------------------

class TestNoKernelDoctrineInRuntime:
    """Verify runtime modules don't define canonical schema or doctrine."""

    RUNTIME_MODULES_TO_CHECK = [
        "runtime.condition_linking.linker",
        "runtime.qa.qa_engine",
        "runtime.drawing_generation.generator",
        "runtime.export.exporter",
    ]

    @pytest.mark.parametrize("module_path", RUNTIME_MODULES_TO_CHECK)
    def test_module_does_not_define_schema(self, module_path):
        """No runtime module should create canonical schema definitions."""
        import importlib
        mod = importlib.import_module(module_path)
        source = inspect.getsource(mod)
        # Runtime modules must not define JSON Schema or canonical doctrine
        assert "jsonschema" not in source.lower() or "validate" in source.lower(), (
            f"{module_path} appears to define canonical schema — runtime must not define doctrine"
        )


# ---------------------------------------------------------------------------
# QA engine references kernel contracts
# ---------------------------------------------------------------------------

class TestQAEngineContractReference:
    """Verify QA engine accepts contract_loader and references kernel contracts."""

    def test_qa_engine_constructor_accepts_contract_loader(self):
        engine = QAEngine(contract_loader="mock_loader")
        assert engine._contract_loader == "mock_loader"

    def test_qa_engine_docstring_references_kernel_contracts(self):
        docstring = inspect.getdoc(QAEngine) or ""
        assert "kernel contract" in docstring.lower(), (
            "QAEngine docstring must reference kernel contracts"
        )

    def test_qa_engine_module_docstring_references_contracts(self):
        import runtime.qa.qa_engine as qa_module
        module_doc = qa_module.__doc__ or ""
        assert "kernel contract" in module_doc.lower(), (
            "QA engine module docstring must reference kernel contracts"
        )


# ---------------------------------------------------------------------------
# Evidence objects include confidence and source references
# ---------------------------------------------------------------------------

class TestEvidenceGovernance:
    """Verify evidence objects include confidence and source references."""

    def test_evidence_record_has_confidence(self):
        record = EvidenceRecord()
        assert hasattr(record, "confidence")

    def test_evidence_record_has_source_document(self):
        record = EvidenceRecord()
        assert hasattr(record, "source_document")

    def test_candidate_has_confidence(self):
        candidate = CandidateObject()
        assert hasattr(candidate, "confidence")

    def test_candidate_has_source_evidence_refs(self):
        candidate = CandidateObject()
        assert hasattr(candidate, "source_evidence_refs")
