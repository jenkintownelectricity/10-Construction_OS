"""Tests for Wave 15 Detail Similarity subsystem."""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from runtime.detail_similarity.similarity_engine import (
    compute_detail_similarity,
    find_similar_details,
    DetailSimilarityError,
)
from runtime.detail_index.index_builder import build_detail_index


def _make_detail(detail_id, system="LOW_SLOPE", cls="TERMINATION",
                 condition="PARAPET", variant="COUNTERFLASHING",
                 family="EPDM", tags=None, materials=None):
    return {
        "detail_id": detail_id,
        "system": system,
        "class": cls,
        "condition": condition,
        "variant": variant,
        "assembly_family": family,
        "display_name": f"Test {detail_id}",
        "synonyms": ["test"],
        "tags": tags or ["fn-termination", "geo-vertical"],
        "compatible_material_classes": materials or ["EPDM"],
        "risk_tags": ["UV_EXPOSURE"],
    }


def _build_test_index():
    records = [
        _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
                      tags=["fn-termination", "fn-waterproofing", "geo-vertical"],
                      materials=["EPDM"]),
        _make_detail("LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01",
                      condition="VERTICAL_WALL", variant="TERMINATION_BAR",
                      family="TPO",
                      tags=["fn-termination", "fn-waterproofing", "geo-vertical"],
                      materials=["TPO"]),
        _make_detail("LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
                      cls="DRAINAGE", condition="DRAIN", variant="COPING",
                      family="TPO",
                      tags=["fn-drainage", "fn-waterproofing", "geo-circular"],
                      materials=["TPO"]),
    ]
    return build_detail_index(records)


DETAIL_PARAPET = "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"
DETAIL_WALL = "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01"
DETAIL_DRAIN = "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01"


class TestComputeSimilarity:
    def test_similar_details_high_score(self):
        index = _build_test_index()
        result = compute_detail_similarity(DETAIL_PARAPET, DETAIL_WALL, index)
        assert result["similarity_score"] > 0.3
        assert result["advisory"] is True
        assert result["deterministic"] is True

    def test_dissimilar_details_lower_score(self):
        index = _build_test_index()
        parapet_wall = compute_detail_similarity(DETAIL_PARAPET, DETAIL_WALL, index)
        parapet_drain = compute_detail_similarity(DETAIL_PARAPET, DETAIL_DRAIN, index)
        assert parapet_wall["similarity_score"] > parapet_drain["similarity_score"]

    def test_self_similarity_not_allowed(self):
        """find_similar_details skips self, but compute allows comparison."""
        index = _build_test_index()
        result = compute_detail_similarity(DETAIL_PARAPET, DETAIL_PARAPET, index)
        assert result["similarity_score"] == 1.0

    def test_unknown_detail_fail_closed(self):
        index = _build_test_index()
        with pytest.raises(DetailSimilarityError, match="Unknown detail_id"):
            compute_detail_similarity("NONEXISTENT", DETAIL_WALL, index)

    def test_deterministic(self):
        index = _build_test_index()
        r1 = compute_detail_similarity(DETAIL_PARAPET, DETAIL_WALL, index)
        r2 = compute_detail_similarity(DETAIL_PARAPET, DETAIL_WALL, index)
        assert r1["similarity_score"] == r2["similarity_score"]
        assert r1["factor_scores"] == r2["factor_scores"]

    def test_score_range(self):
        index = _build_test_index()
        result = compute_detail_similarity(DETAIL_PARAPET, DETAIL_DRAIN, index)
        assert 0.0 <= result["similarity_score"] <= 1.0


class TestFindSimilarDetails:
    def test_finds_similar(self):
        index = _build_test_index()
        results = find_similar_details(DETAIL_PARAPET, index)
        assert len(results) >= 1
        assert results[0]["candidate_id"] != DETAIL_PARAPET

    def test_most_similar_first(self):
        index = _build_test_index()
        results = find_similar_details(DETAIL_PARAPET, index)
        if len(results) >= 2:
            assert results[0]["similarity_score"] >= results[1]["similarity_score"]

    def test_top_n_limit(self):
        index = _build_test_index()
        results = find_similar_details(DETAIL_PARAPET, index, top_n=1)
        assert len(results) <= 1

    def test_min_score_filter(self):
        index = _build_test_index()
        results = find_similar_details(DETAIL_PARAPET, index, min_score=0.99)
        for r in results:
            assert r["similarity_score"] >= 0.99

    def test_unknown_detail_fail_closed(self):
        index = _build_test_index()
        with pytest.raises(DetailSimilarityError):
            find_similar_details("NONEXISTENT", index)

    def test_advisory_flag(self):
        index = _build_test_index()
        results = find_similar_details(DETAIL_PARAPET, index)
        for r in results:
            assert r["advisory"] is True
