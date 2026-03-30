"""Unit tests for conflict detection."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engine.conflict_detector import detect_conflicts
from unittest.mock import MagicMock


def _mock_kernel(conflicts=None):
    kernel = MagicMock()
    kernel.get_conflicts_for_entity = MagicMock(return_value=conflicts or [])
    return kernel


def _normalized(**overrides):
    base = {
        "condition_id": "COND-001",
        "condition_type": "roof_edge",
        "zone_id": "zone-A1",
        "adjacencies": [],
        "dimensions": {},
        "material_preferences": [],
        "climate_context": {},
    }
    base.update(overrides)
    return base


def test_no_conflicts():
    kernel = _mock_kernel([])
    result = detect_conflicts(
        _normalized(), "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", "DNA-CONSTR-FAM-EDGE-001-R1", kernel,
    )
    assert result["has_conflicts"] is False
    assert result["conflicts"] == []


def test_conflict_detected():
    conflict_rel = {
        "id": "SOUND-CONSTR-REL-EDGEJOINT-003-R1",
        "type": "conflict",
        "source": {"id": "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", "name": "Drip Edge"},
        "target": {"id": "DNA-CONSTR-PAT-JOINT-ROOF-050-R1", "name": "Roof Expansion Joint"},
        "severity": "critical",
        "description": "Drip edge cannot cross expansion joint",
        "resolution": {"strategy": "transition_detail_required"},
    }
    kernel = _mock_kernel([conflict_rel])
    result = detect_conflicts(
        _normalized(), "DNA-CONSTR-PAT-EDGE-DRIP-010-R1", "DNA-CONSTR-FAM-EDGE-001-R1", kernel,
    )
    assert result["has_conflicts"] is True
    assert len(result["conflicts"]) == 1
    assert result["conflicts"][0]["severity"] == "critical"
    assert result["conflicts"][0]["relationship_id"] == "SOUND-CONSTR-REL-EDGEJOINT-003-R1"


def test_conflict_record_structure():
    conflict_rel = {
        "id": "SOUND-CONSTR-REL-TEST-001-R1",
        "type": "conflict",
        "source": {"id": "SRC-001"},
        "target": {"id": "TGT-001"},
        "severity": "warning",
        "description": "test conflict",
        "resolution": {"strategy": "manual_review"},
    }
    kernel = _mock_kernel([conflict_rel])
    result = detect_conflicts(_normalized(), "SRC-001", "FAM-001", kernel)
    assert result["has_conflicts"] is True
    c = result["conflicts"][0]
    assert "conflict_id" in c
    assert c["relationship_id"] == "SOUND-CONSTR-REL-TEST-001-R1"
    assert c["source_id"] == "SRC-001"
    assert c["target_id"] == "TGT-001"
    assert c["severity"] == "warning"
    assert c["resolution_strategy"] == "manual_review"


def test_conflict_fail_reason():
    conflict_rel = {
        "id": "REL-001",
        "type": "conflict",
        "source": {"id": "PAT-001"},
        "target": {"id": "PAT-002"},
        "severity": "critical",
        "description": "conflict",
        "resolution": {},
    }
    kernel = _mock_kernel([conflict_rel])
    result = detect_conflicts(_normalized(), "PAT-001", "FAM-001", kernel)
    assert result["fail_reason"]["code"] == "CONFLICT_DETECTED"
    assert result["fail_reason"]["stage"] == "conflict_detection"


def test_multiple_conflicts():
    rels = [
        {"id": "REL-001", "type": "conflict", "source": {"id": "PAT-001"}, "target": {"id": "PAT-002"}, "severity": "critical", "description": "c1", "resolution": {}},
        {"id": "REL-002", "type": "conflict", "source": {"id": "PAT-001"}, "target": {"id": "PAT-003"}, "severity": "warning", "description": "c2", "resolution": {}},
    ]
    kernel = _mock_kernel(rels)
    result = detect_conflicts(_normalized(), "PAT-001", "FAM-001", kernel)
    assert result["has_conflicts"] is True
    assert len(result["conflicts"]) == 2
