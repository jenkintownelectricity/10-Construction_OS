"""Tests for assembly parser and normalizer."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.parsers.assembly_parser.normalizer import normalize_assembly_input
from runtime.parsers.assembly_parser.parser import parse_assembly


class TestAssemblyNormalizer:
    def test_empty_input(self):
        assert normalize_assembly_input("") == ""
        assert normalize_assembly_input("   ") == ""
        assert normalize_assembly_input(None) == ""

    def test_whitespace_collapse(self):
        result = normalize_assembly_input("hello   world")
        assert result == "hello world"

    def test_line_ending_normalization(self):
        result = normalize_assembly_input("line1\r\nline2\rline3")
        assert "\r" not in result
        assert "line1" in result
        assert "line2" in result
        assert "line3" in result

    def test_control_character_removal(self):
        result = normalize_assembly_input("clean\x00text\x07here")
        assert result == "clean text here" or "cleantext" in result.replace(" ", "")

    def test_strips_leading_trailing_blanks(self):
        result = normalize_assembly_input("\n\nhello\n\n")
        assert result == "hello"


class TestAssemblyParser:
    def test_empty_input(self):
        result = parse_assembly("")
        assert result["metadata"]["parse_status"] == "empty_input"
        assert result["components"] == []

    def test_basic_assembly(self):
        text = """Assembly: Test Assembly
Components:
- Steel Beam
- Bolt Set
Constraint: Clearance = 1 inch
"""
        result = parse_assembly(text)
        assert result["name"] == "Test Assembly"
        assert len(result["components"]) == 2
        assert result["components"][0]["name"] == "Steel Beam"
        assert len(result["constraints"]) == 1
        assert result["metadata"]["parse_status"] == "success"

    def test_explicit_component_lines(self):
        text = """Name: My Assembly
Part: W12x26 Beam
Part: Angle Bracket
"""
        result = parse_assembly(text)
        assert result["name"] == "My Assembly"
        assert len(result["components"]) == 2

    def test_multiple_constraint_types(self):
        text = """Assembly: Constraint Test
Component: Beam
Constraint: Must be level
Clearance: 2 inches
Spacing: 3 inches on center
Interface: Beam to column
Tolerance: +/- 1/16"
"""
        result = parse_assembly(text)
        assert len(result["constraints"]) == 5
        types = [c["type"] for c in result["constraints"]]
        assert "constraint" in types
        assert "clearance" in types
        assert "spacing" in types
        assert "interface" in types
        assert "tolerance" in types
