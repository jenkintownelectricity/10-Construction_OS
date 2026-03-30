"""Tests for Wave 15 Detail Search subsystem."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from runtime.detail_search.search_engine import search_details, DetailSearchError
from runtime.detail_search.validator import validate_search_result
from runtime.detail_index.index_builder import build_detail_index


def _make_detail(detail_id, system="LOW_SLOPE", cls="TERMINATION",
                 condition="PARAPET", variant="COUNTERFLASHING",
                 family="EPDM", tags=None, synonyms=None):
    return {
        "detail_id": detail_id,
        "system": system,
        "class": cls,
        "condition": condition,
        "variant": variant,
        "assembly_family": family,
        "display_name": f"Test {detail_id}",
        "synonyms": synonyms or ["test syn"],
        "tags": tags or ["fn-termination"],
        "compatible_material_classes": ["EPDM"],
        "risk_tags": ["UV_EXPOSURE"],
    }


def _build_test_index():
    records = [
        _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
                      tags=["fn-termination", "fn-waterproofing", "fn-flashing"],
                      synonyms=["parapet cap detail", "parapet flashing"]),
        _make_detail("LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01",
                      cls="EDGE", condition="ROOF_TO_EDGE", variant="METAL_EDGE",
                      family="TPO", tags=["fn-termination", "acc-metal-edge"],
                      synonyms=["drip edge", "edge metal"]),
        _make_detail("LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
                      cls="DRAINAGE", condition="DRAIN", variant="COPING",
                      family="TPO", tags=["fn-drainage", "fn-waterproofing"],
                      synonyms=["roof drain"]),
    ]
    return build_detail_index(records)


class TestTagSearch:
    def test_exact_tag_match(self):
        index = _build_test_index()
        result = search_details("fn-drainage", "tag", index)
        assert result["total_results"] >= 1
        assert result["deterministic"] is True
        ids = [r["detail_id"] for r in result["results"]]
        assert "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01" in ids

    def test_prefix_tag_match(self):
        index = _build_test_index()
        result = search_details("fn-", "tag", index)
        assert result["total_results"] >= 2


class TestFamilySearch:
    def test_family_match(self):
        index = _build_test_index()
        result = search_details("epdm", "family", index)
        assert result["total_results"] >= 1

    def test_family_no_match(self):
        index = _build_test_index()
        result = search_details("pvc", "family", index)
        assert result["total_results"] == 0


class TestConditionSearch:
    def test_condition_match(self):
        index = _build_test_index()
        result = search_details("parapet", "condition", index)
        assert result["total_results"] >= 1

    def test_condition_partial(self):
        index = _build_test_index()
        result = search_details("drain", "condition", index)
        assert result["total_results"] >= 1


class TestNameSearch:
    def test_name_match(self):
        index = _build_test_index()
        result = search_details("parapet", "name", index)
        assert result["total_results"] >= 1


class TestSynonymSearch:
    def test_synonym_match(self):
        index = _build_test_index()
        result = search_details("parapet cap", "synonym", index)
        assert result["total_results"] >= 1

    def test_synonym_no_match(self):
        index = _build_test_index()
        result = search_details("zzz_nonexistent_zzz", "synonym", index)
        assert result["total_results"] == 0


class TestCompositeSearch:
    def test_composite_deduplicates(self):
        index = _build_test_index()
        result = search_details("parapet", "composite", index)
        ids = [r["detail_id"] for r in result["results"]]
        assert len(ids) == len(set(ids))
        assert result["total_results"] >= 1


class TestSearchValidation:
    def test_invalid_type_fail_closed(self):
        index = _build_test_index()
        with pytest.raises(DetailSearchError, match="Unknown search_type"):
            search_details("test", "invalid_type", index)

    def test_empty_query_returns_empty(self):
        index = _build_test_index()
        result = search_details("", "tag", index)
        assert result["total_results"] == 0

    def test_deterministic_results(self):
        index = _build_test_index()
        r1 = search_details("fn-termination", "tag", index)
        r2 = search_details("fn-termination", "tag", index)
        assert r1["results"] == r2["results"]


class TestValidateSearchResult:
    def test_valid_result_passes(self):
        index = _build_test_index()
        result = search_details("parapet", "name", index)
        report = validate_search_result(result)
        assert report["status"] == "PASS"
