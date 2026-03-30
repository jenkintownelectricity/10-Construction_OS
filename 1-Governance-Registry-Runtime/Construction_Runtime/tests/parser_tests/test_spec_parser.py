"""Tests for spec parser and normalizer."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.parsers.spec_parser.normalizer import normalize_spec_input
from runtime.parsers.spec_parser.parser import parse_spec


class TestSpecNormalizer:
    def test_empty_input(self):
        assert normalize_spec_input("") == ""
        assert normalize_spec_input("   ") == ""

    def test_whitespace_normalization(self):
        result = normalize_spec_input("hello   world")
        assert result == "hello world"

    def test_preserves_internal_blank_lines(self):
        result = normalize_spec_input("line1\n\nline2")
        assert "line1" in result
        assert "line2" in result


class TestSpecParser:
    def test_empty_input(self):
        result = parse_spec("")
        assert result["metadata"]["parse_status"] == "empty_input"
        assert result["sections"] == []
        assert result["requirements"] == []

    def test_section_detection(self):
        text = """1.1 - Summary
This section covers sealants.
2.1 - Products
Products are listed below.
"""
        result = parse_spec(text)
        assert len(result["sections"]) == 2
        assert result["sections"][0]["number"] == "1.1"
        assert result["sections"][0]["title"] == "Summary"

    def test_requirement_detection(self):
        text = """The sealant shall comply with ASTM C920.
Joint width must be minimum 1/4".
Surface preparation is recommended.
"""
        result = parse_spec(text)
        assert len(result["requirements"]) == 2
        assert result["requirements"][0]["type"] == "mandatory"

    def test_product_reference_detection(self):
        text = """Manufacturer: Dow Corning
Product: 795 Silicone Sealant
Basis of Design: Dow Corning 795
Model No: 795-SBS
"""
        result = parse_spec(text)
        assert len(result["product_references"]) == 4
        types = [r["type"] for r in result["product_references"]]
        assert "manufacturer" in types
        assert "product" in types
        assert "basis_of_design" in types
        assert "model" in types

    def test_full_spec_parse(self):
        text = """1.0 - General
The system shall meet all applicable codes.
Manufacturer: Acme Corp
2.0 - Materials
Material must be fire-rated.
"""
        result = parse_spec(text)
        assert result["metadata"]["parse_status"] == "success"
        assert len(result["sections"]) == 2
        assert len(result["requirements"]) == 2
        assert len(result["product_references"]) == 1
