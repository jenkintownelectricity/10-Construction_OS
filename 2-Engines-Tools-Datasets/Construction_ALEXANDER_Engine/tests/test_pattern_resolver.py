"""Unit tests for pattern resolution."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.pattern_resolver import resolve_pattern
from unittest.mock import MagicMock


def _mock_kernel(patterns=None):
    kernel = MagicMock()
    kernel.get_patterns_for_family = MagicMock(return_value=patterns or [])
    return kernel


def _normalized(**overrides):
    base = {
        "condition_id": "COND-001",
        "condition_type": "roof_edge",
        "zone_id": "zone-A1",
        "interface_condition": None,
        "dimensions": {},
        "material_preferences": [],
        "method_preference": None,
        "manufacturer_refs": [],
        "climate_context": {},
        "system_type": None,
    }
    base.update(overrides)
    return base


def test_single_pattern_match():
    pat = {"id": "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", "name": "Drip Edge", "description": "drip edge", "detail_intents": []}
    kernel = _mock_kernel([pat])
    result = resolve_pattern(_normalized(), "DNA-CONSTR-FAM-EDGE-001-R1", kernel)
    assert result["matched"] is True
    assert result["pattern_id"] == "DNA-CONSTR-PAT-EDGE-DRIP-010-R1"
    assert result["confidence"] == 1.0


def test_no_patterns_found():
    kernel = _mock_kernel([])
    result = resolve_pattern(_normalized(), "DNA-CONSTR-FAM-EDGE-001-R1", kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] == "MISSING_TRUTH"


def test_disambiguates_by_method_preference():
    p1 = {"id": "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", "name": "Drip Edge", "description": "mechanical fastened drip", "detail_intents": []}
    p2 = {"id": "DNA-CONSTR-PAT-EDGE-GRAVELSTOP-011-R1", "name": "Gravel Stop", "description": "gravel stop edge", "detail_intents": []}
    kernel = _mock_kernel([p1, p2])
    result = resolve_pattern(_normalized(method_preference="mechanical"), "DNA-CONSTR-FAM-EDGE-001-R1", kernel)
    assert result["matched"] is True
    assert result["pattern_id"] == "DNA-CONSTR-PAT-EDGE-DRIP-010-R1"


def test_ambiguous_patterns():
    p1 = {"id": "DNA-CONSTR-PAT-A-010-R1", "name": "Pattern A", "description": "identical", "detail_intents": []}
    p2 = {"id": "DNA-CONSTR-PAT-B-011-R1", "name": "Pattern B", "description": "identical", "detail_intents": []}
    kernel = _mock_kernel([p1, p2])
    result = resolve_pattern(_normalized(), "DNA-CONSTR-FAM-EDGE-001-R1", kernel)
    assert result["matched"] is False
    assert result["fail_reason"]["code"] in ("AMBIGUOUS_PATTERN", "NO_PATTERN_MATCH")


def test_no_match_all_zero_score():
    p1 = {"id": "DNA-CONSTR-PAT-X-010-R1", "name": "X", "description": "unrelated", "detail_intents": []}
    p2 = {"id": "DNA-CONSTR-PAT-Y-011-R1", "name": "Y", "description": "also unrelated", "detail_intents": []}
    kernel = _mock_kernel([p1, p2])
    result = resolve_pattern(_normalized(), "DNA-CONSTR-FAM-EDGE-001-R1", kernel)
    assert result["matched"] is False


def test_material_preference_scores():
    p1 = {"id": "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", "name": "Drip Edge", "description": "galvanized steel drip edge", "detail_intents": []}
    p2 = {"id": "DNA-CONSTR-PAT-EDGE-GRAVELSTOP-011-R1", "name": "Gravel Stop", "description": "aluminum gravel stop", "detail_intents": []}
    kernel = _mock_kernel([p1, p2])
    result = resolve_pattern(_normalized(material_preferences=["galvanized"]), "DNA-CONSTR-FAM-EDGE-001-R1", kernel)
    assert result["matched"] is True
    assert result["pattern_id"] == "DNA-CONSTR-PAT-EDGE-DRIP-010-R1"
