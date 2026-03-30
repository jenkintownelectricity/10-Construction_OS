"""Wave 18 test fixtures for artifact rendering pipeline."""

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
)
from runtime.artifact_renderer.artifact_contract import RenderManifest
from runtime.artifact_renderer.renderer_registry import RendererRegistry
from runtime.artifact_renderer.dxf_renderer import DxfRenderer
from runtime.artifact_renderer.svg_renderer import SvgRenderer
from runtime.artifact_renderer.pdf_renderer import PdfRenderer


@pytest.fixture
def sample_point():
    return Point2D(5.0, 10.0)


@pytest.fixture
def sample_line():
    return LinePrimitive(
        start=Point2D(0.0, 0.0),
        end=Point2D(10.0, 5.0),
        layer="A-DETAIL",
        lineweight=0.25,
    )


@pytest.fixture
def sample_arc():
    return ArcPrimitive(
        center=Point2D(5.0, 5.0),
        radius=3.0,
        start_angle=0.0,
        end_angle=90.0,
        layer="A-DETAIL",
    )


@pytest.fixture
def sample_full_circle():
    return ArcPrimitive(
        center=Point2D(5.0, 5.0),
        radius=2.0,
        start_angle=0.0,
        end_angle=360.0,
        layer="A-DETAIL",
    )


@pytest.fixture
def sample_polyline():
    return PolylinePrimitive(
        points=[Point2D(0, 0), Point2D(5, 0), Point2D(5, 5), Point2D(0, 5)],
        closed=True,
        layer="A-COMP",
    )


@pytest.fixture
def sample_rectangle():
    return RectanglePrimitive(
        origin=Point2D(2.0, 3.0),
        width=8.0,
        height=4.0,
        layer="A-COMP",
    )


@pytest.fixture
def sample_text():
    return TextPrimitive(
        text="PARAPET CAP",
        position=Point2D(12.0, 20.0),
        height=0.25,
        layer="A-TEXT",
    )


@pytest.fixture
def sample_hatch():
    return HatchPrimitive(
        boundary=[Point2D(0, 0), Point2D(4, 0), Point2D(4, 4), Point2D(0, 4)],
        pattern="ANSI31",
        scale=1.0,
        angle=45.0,
        layer="A-HATCH",
    )


@pytest.fixture
def sample_dimension():
    return DimensionPrimitive(
        start=Point2D(0.0, 0.0),
        end=Point2D(12.0, 0.0),
        offset=0.5,
        text='12"',
        unit="in",
        layer="A-DIMS",
    )


@pytest.fixture
def sample_callout():
    return CalloutPrimitive(
        anchor=Point2D(6.0, 18.0),
        leader_end=Point2D(10.0, 15.0),
        text="A1",
        bubble_radius=0.375,
        layer="A-ANNO",
    )


@pytest.fixture
def all_primitives(
    sample_line, sample_arc, sample_polyline, sample_rectangle,
    sample_text, sample_hatch, sample_dimension, sample_callout,
):
    return [
        sample_line, sample_arc, sample_polyline, sample_rectangle,
        sample_text, sample_hatch, sample_dimension, sample_callout,
    ]


@pytest.fixture
def sample_sheet():
    return {"width": 36.0, "height": 24.0, "unit": "in", "scale": "1:1"}


@pytest.fixture
def sample_layers():
    return ["A-COMP", "A-DETAIL", "A-DIMS", "A-TEXT", "A-HATCH", "A-ANNO"]


@pytest.fixture
def sample_metadata():
    return {
        "title": {
            "detail_id": "LOW_SLOPE-PARAPET-EPDM-01",
            "display_name": "EPDM Parapet Termination",
            "assembly_family": "parapet_termination",
        },
        "provenance": {
            "source_detail_id": "LOW_SLOPE-PARAPET-EPDM-01",
            "builder_version": "18.0",
            "resolved_by": "Construction_Runtime",
            "wave": "18",
        },
    }


@pytest.fixture
def sample_detail_dna():
    return {
        "detail_id": "LOW_SLOPE-PARAPET-EPDM-01",
        "variant_id": "v1",
        "assembly_family": "parapet_termination",
        "display_name": "EPDM Parapet Termination",
        "sheet_width": 36.0,
        "sheet_height": 24.0,
        "scale": "3:1",
        "entities": [
            {
                "type": "LINE",
                "layer": "A-DETAIL",
                "properties": {"x1": 0, "y1": 0, "x2": 10, "y2": 0},
            },
            {
                "type": "LINE",
                "layer": "A-DETAIL",
                "properties": {"x1": 10, "y1": 0, "x2": 10, "y2": 8},
            },
            {
                "type": "RECTANGLE",
                "layer": "A-COMP",
                "properties": {"x": 1, "y": 1, "width": 8, "height": 6},
            },
            {
                "type": "ARC",
                "layer": "A-DETAIL",
                "properties": {"cx": 5, "cy": 4, "radius": 2, "start_angle": 0, "end_angle": 180},
            },
            {
                "type": "TEXT",
                "layer": "A-TEXT",
                "properties": {"text": "EPDM MEMBRANE", "x": 2, "y": 9, "height": 0.2},
            },
            {
                "type": "HATCH",
                "layer": "A-HATCH",
                "properties": {
                    "boundary": [[1, 1], [9, 1], [9, 7], [1, 7]],
                    "pattern": "ANSI31",
                },
            },
            {
                "type": "DIMENSION",
                "layer": "A-DIMS",
                "properties": {"x1": 1, "y1": 0.5, "x2": 9, "y2": 0.5, "text": '8"'},
            },
            {
                "type": "CALLOUT",
                "layer": "A-ANNO",
                "properties": {"ax": 5, "ay": 12, "lx": 8, "ly": 10, "text": "1"},
            },
        ],
    }


@pytest.fixture
def sample_manifest():
    return RenderManifest(
        manifest_id="MAN-test-001",
        detail_id="LOW_SLOPE-PARAPET-EPDM-01",
        variant_id="v1",
        assembly_family="parapet_termination",
        instruction_set_id="IS-test-001",
        requested_formats=["DXF", "SVG", "PDF"],
        metadata={"display_name": "EPDM Parapet Termination"},
    )


@pytest.fixture
def dxf_renderer():
    return DxfRenderer()


@pytest.fixture
def svg_renderer():
    return SvgRenderer()


@pytest.fixture
def pdf_renderer():
    return PdfRenderer()


@pytest.fixture
def full_registry():
    reg = RendererRegistry()
    reg.register(DxfRenderer())
    reg.register(SvgRenderer())
    reg.register(PdfRenderer())
    return reg
