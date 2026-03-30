"""Unit tests for scoring engine."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.scoring_engine import score_resolution


def test_perfect_score():
    result = score_resolution(
        family_result={"matched": True, "confidence": 1.0},
        pattern_result={"matched": True, "confidence": 1.0},
        variant_result={"matched": True, "confidence": 1.0},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": False, "conflicts": []},
    )
    assert result["scored"] is True
    assert result["score"]["total_score"] == 1.0
    assert result["score"]["breakdown"]["family_confidence"] == 1.0
    assert result["score"]["breakdown"]["pattern_fit"] == 1.0
    assert result["score"]["breakdown"]["variant_match"] == 1.0
    assert result["score"]["breakdown"]["constraint_compliance"] == 1.0
    assert result["score"]["breakdown"]["conflict_free"] == 1.0


def test_zero_score_no_matches():
    result = score_resolution(
        family_result={"matched": False, "confidence": 0.0},
        pattern_result={"matched": False, "confidence": 0.0},
        variant_result={"matched": False, "confidence": 0.0},
        constraint_result={"passed": False, "violations": [1, 2, 3, 4]},
        conflict_result={"has_conflicts": True, "conflicts": [{"severity": "critical"}, {"severity": "critical"}]},
    )
    assert result["scored"] is True
    assert result["score"]["total_score"] == 0.0


def test_partial_score():
    result = score_resolution(
        family_result={"matched": True, "confidence": 0.8},
        pattern_result={"matched": True, "confidence": 0.6},
        variant_result={"matched": True, "confidence": 0.5},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": False, "conflicts": []},
    )
    assert result["scored"] is True
    score = result["score"]["total_score"]
    assert 0 < score < 1


def test_constraint_violations_reduce_score():
    perfect = score_resolution(
        family_result={"matched": True, "confidence": 1.0},
        pattern_result={"matched": True, "confidence": 1.0},
        variant_result={"matched": True, "confidence": 1.0},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": False, "conflicts": []},
    )
    with_violations = score_resolution(
        family_result={"matched": True, "confidence": 1.0},
        pattern_result={"matched": True, "confidence": 1.0},
        variant_result={"matched": True, "confidence": 1.0},
        constraint_result={"passed": False, "violations": [{"v": 1}]},
        conflict_result={"has_conflicts": False, "conflicts": []},
    )
    assert with_violations["score"]["total_score"] < perfect["score"]["total_score"]


def test_conflicts_reduce_score():
    perfect = score_resolution(
        family_result={"matched": True, "confidence": 1.0},
        pattern_result={"matched": True, "confidence": 1.0},
        variant_result={"matched": True, "confidence": 1.0},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": False, "conflicts": []},
    )
    with_conflicts = score_resolution(
        family_result={"matched": True, "confidence": 1.0},
        pattern_result={"matched": True, "confidence": 1.0},
        variant_result={"matched": True, "confidence": 1.0},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": True, "conflicts": [{"severity": "critical"}]},
    )
    assert with_conflicts["score"]["total_score"] < perfect["score"]["total_score"]


def test_critical_conflicts_reduce_more_than_warnings():
    critical = score_resolution(
        family_result={"matched": True, "confidence": 1.0},
        pattern_result={"matched": True, "confidence": 1.0},
        variant_result={"matched": True, "confidence": 1.0},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": True, "conflicts": [{"severity": "critical"}]},
    )
    warning = score_resolution(
        family_result={"matched": True, "confidence": 1.0},
        pattern_result={"matched": True, "confidence": 1.0},
        variant_result={"matched": True, "confidence": 1.0},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": True, "conflicts": [{"severity": "warning"}]},
    )
    assert critical["score"]["total_score"] < warning["score"]["total_score"]


def test_score_bounded_0_to_1():
    result = score_resolution(
        family_result={"matched": True, "confidence": 2.0},  # over 1
        pattern_result={"matched": True, "confidence": 2.0},
        variant_result={"matched": True, "confidence": 2.0},
        constraint_result={"passed": True, "violations": []},
        conflict_result={"has_conflicts": False, "conflicts": []},
    )
    assert result["score"]["total_score"] <= 1.0
    assert result["score"]["total_score"] >= 0.0
