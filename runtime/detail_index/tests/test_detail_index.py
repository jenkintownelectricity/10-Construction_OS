"""Tests for Wave 15 Detail Index subsystem."""

import json
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from runtime.detail_index.index_builder import (
    build_detail_index,
    DetailIndexBuildError,
)
from runtime.detail_index.validator import validate_detail_index, DetailIndexValidationError
from runtime.detail_index.serializer import serialize_detail_index, deserialize_detail_index


def _make_detail(detail_id, system="LOW_SLOPE", cls="TERMINATION",
                 condition="PARAPET", variant="COUNTERFLASHING",
                 family="EPDM", tags=None):
    return {
        "detail_id": detail_id,
        "system": system,
        "class": cls,
        "condition": condition,
        "variant": variant,
        "assembly_family": family,
        "display_name": f"Test {detail_id}",
        "synonyms": ["test syn"],
        "tags": tags or ["fn-termination"],
        "compatible_material_classes": ["EPDM"],
        "risk_tags": ["UV_EXPOSURE"],
    }


class TestBuildDetailIndex:
    def test_builds_valid_index(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
            _make_detail("LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01",
                         cls="EDGE", condition="ROOF_TO_EDGE", variant="METAL_EDGE",
                         family="TPO", tags=["fn-termination", "fn-flashing"]),
        ]
        index = build_detail_index(records)

        assert index["version"] == "15.1.0"
        assert index["wave"] == "15"
        assert index["detail_count"] == 2
        assert "checksum" in index
        assert len(index["detail_lookup"]) == 2
        assert "EPDM" in index["family_index"]
        assert "TPO" in index["family_index"]
        assert "PARAPET" in index["condition_index"]
        assert "LOW_SLOPE" in index["system_index"]

    def test_deterministic_output(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
            _make_detail("LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01",
                         cls="EDGE", condition="ROOF_TO_EDGE", variant="METAL_EDGE", family="TPO"),
        ]
        index1 = build_detail_index(records)
        index2 = build_detail_index(records)
        assert index1["checksum"] == index2["checksum"]

    def test_empty_records_fail_closed(self):
        with pytest.raises(DetailIndexBuildError, match="empty"):
            build_detail_index([])

    def test_duplicate_id_fail_closed(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
        ]
        with pytest.raises(DetailIndexBuildError, match="Duplicate"):
            build_detail_index(records)

    def test_missing_field_fail_closed(self):
        record = _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01")
        del record["tags"]
        with pytest.raises(DetailIndexBuildError, match="missing required fields"):
            build_detail_index([record])

    def test_invalid_system_fail_closed(self):
        record = _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
                              system="INVALID")
        with pytest.raises(DetailIndexBuildError, match="invalid system"):
            build_detail_index([record])

    def test_invalid_class_fail_closed(self):
        record = _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
                              cls="INVALID")
        with pytest.raises(DetailIndexBuildError, match="invalid class"):
            build_detail_index([record])

    def test_tag_index_populated(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
                         tags=["fn-termination", "fn-waterproofing"]),
        ]
        index = build_detail_index(records)
        assert "fn-termination" in index["tag_index"]
        assert "fn-waterproofing" in index["tag_index"]


class TestValidateDetailIndex:
    def test_valid_index_passes(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
        ]
        index = build_detail_index(records)
        report = validate_detail_index(index)
        assert report["status"] == "PASS"

    def test_kernel_cross_ref_detects_unknown(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
        ]
        index = build_detail_index(records)
        with pytest.raises(DetailIndexValidationError):
            validate_detail_index(index, kernel_detail_ids=set())

    def test_checksum_tamper_detected(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
        ]
        index = build_detail_index(records)
        index["checksum"] = "tampered"
        with pytest.raises(DetailIndexValidationError):
            validate_detail_index(index)


class TestSerializer:
    def test_round_trip(self):
        records = [
            _make_detail("LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01"),
        ]
        index = build_detail_index(records)
        json_str = serialize_detail_index(index)
        restored = deserialize_detail_index(json_str)
        assert restored["checksum"] == index["checksum"]
        assert restored["detail_count"] == index["detail_count"]
