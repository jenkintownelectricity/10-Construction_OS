"""Tests for geometry primitives module."""

import math
import pytest
from runtime.artifact_renderer.geometry_primitives import (
    Point2D,
    LinePrimitive,
    ArcPrimitive,
    PolylinePrimitive,
    RectanglePrimitive,
    TextPrimitive,
    HatchPrimitive,
    DimensionPrimitive,
    CalloutPrimitive,
    SUPPORTED_PRIMITIVES,
    get_primitive_type,
    validate_primitive,
)


class TestPoint2D:
    def test_creation(self):
        p = Point2D(3.0, 4.0)
        assert p.x == 3.0
        assert p.y == 4.0

    def test_distance(self):
        p1 = Point2D(0.0, 0.0)
        p2 = Point2D(3.0, 4.0)
        assert p1.distance_to(p2) == 5.0

    def test_to_tuple(self):
        p = Point2D(1.5, 2.5)
        assert p.to_tuple() == (1.5, 2.5)

    def test_immutable(self):
        p = Point2D(1.0, 2.0)
        with pytest.raises(AttributeError):
            p.x = 5.0


class TestLinePrimitive:
    def test_creation(self, sample_line):
        assert sample_line.primitive_type == "LINE"
        assert sample_line.layer == "A-DETAIL"

    def test_length(self, sample_line):
        expected = math.sqrt(10**2 + 5**2)
        assert abs(sample_line.length() - expected) < 0.001

    def test_zero_length_validation(self):
        line = LinePrimitive(start=Point2D(1, 1), end=Point2D(1, 1), layer="A-DETAIL")
        errors = validate_primitive(line)
        assert any("zero length" in e for e in errors)


class TestArcPrimitive:
    def test_sweep_angle(self, sample_arc):
        assert sample_arc.sweep_angle() == 90.0

    def test_full_circle(self, sample_full_circle):
        assert sample_full_circle.is_full_circle()

    def test_not_full_circle(self, sample_arc):
        assert not sample_arc.is_full_circle()

    def test_negative_radius_validation(self):
        arc = ArcPrimitive(center=Point2D(0, 0), radius=-1.0, layer="A-DETAIL")
        errors = validate_primitive(arc)
        assert any("non-positive radius" in e for e in errors)


class TestPolylinePrimitive:
    def test_vertex_count(self, sample_polyline):
        assert sample_polyline.vertex_count() == 4

    def test_segment_count_closed(self, sample_polyline):
        assert sample_polyline.segment_count() == 4

    def test_segment_count_open(self):
        pl = PolylinePrimitive(
            points=[Point2D(0, 0), Point2D(1, 0), Point2D(2, 0)],
            closed=False,
            layer="A-DETAIL",
        )
        assert pl.segment_count() == 2

    def test_too_few_points(self):
        pl = PolylinePrimitive(points=[Point2D(0, 0)], layer="A-DETAIL")
        errors = validate_primitive(pl)
        assert any("fewer than 2" in e for e in errors)


class TestRectanglePrimitive:
    def test_area(self, sample_rectangle):
        assert sample_rectangle.area() == 32.0

    def test_corners(self, sample_rectangle):
        corners = sample_rectangle.corners()
        assert len(corners) == 4
        assert corners[0] == Point2D(2.0, 3.0)
        assert corners[2] == Point2D(10.0, 7.0)

    def test_zero_dimensions_validation(self):
        rect = RectanglePrimitive(origin=Point2D(0, 0), width=0, height=5, layer="A-COMP")
        errors = validate_primitive(rect)
        assert any("non-positive" in e for e in errors)


class TestTextPrimitive:
    def test_creation(self, sample_text):
        assert sample_text.text == "PARAPET CAP"
        assert sample_text.primitive_type == "TEXT"

    def test_empty_text_validation(self):
        t = TextPrimitive(text="", layer="A-TEXT")
        errors = validate_primitive(t)
        assert any("empty text" in e for e in errors)


class TestHatchPrimitive:
    def test_boundary_count(self, sample_hatch):
        assert sample_hatch.boundary_vertex_count() == 4

    def test_too_few_boundary_points(self):
        h = HatchPrimitive(boundary=[Point2D(0, 0), Point2D(1, 1)], layer="A-HATCH")
        errors = validate_primitive(h)
        assert any("fewer than 3" in e for e in errors)


class TestDimensionPrimitive:
    def test_measured_value(self, sample_dimension):
        assert sample_dimension.measured_value() == 12.0

    def test_zero_length_validation(self):
        d = DimensionPrimitive(start=Point2D(5, 5), end=Point2D(5, 5), layer="A-DIMS")
        errors = validate_primitive(d)
        assert any("zero length" in e for e in errors)


class TestCalloutPrimitive:
    def test_creation(self, sample_callout):
        assert sample_callout.text == "A1"
        assert sample_callout.primitive_type == "CALLOUT"

    def test_empty_text_validation(self):
        c = CalloutPrimitive(anchor=Point2D(0, 0), leader_end=Point2D(1, 1), text="", layer="A-ANNO")
        errors = validate_primitive(c)
        assert any("empty text" in e for e in errors)


class TestSupportedPrimitives:
    def test_all_eight_primitives(self):
        assert len(SUPPORTED_PRIMITIVES) == 8
        for pt in ["LINE", "ARC", "POLYLINE", "RECTANGLE", "TEXT", "HATCH", "DIMENSION", "CALLOUT"]:
            assert pt in SUPPORTED_PRIMITIVES

    def test_get_primitive_type(self, sample_line):
        assert get_primitive_type(sample_line) == "LINE"


class TestValidation:
    def test_no_layer_validation(self):
        line = LinePrimitive(start=Point2D(0, 0), end=Point2D(1, 1), layer="")
        errors = validate_primitive(line)
        assert any("no layer" in e for e in errors)

    def test_valid_primitive_no_errors(self, sample_line):
        errors = validate_primitive(sample_line)
        assert len(errors) == 0
