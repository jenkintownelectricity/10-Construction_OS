"""Tests for DXF, SVG, and PDF renderers."""

import pytest
from runtime.artifact_renderer.dxf_renderer import DxfRenderer, RENDERER_ID as DXF_ID
from runtime.artifact_renderer.svg_renderer import SvgRenderer, RENDERER_ID as SVG_ID
from runtime.artifact_renderer.pdf_renderer import PdfRenderer, RENDERER_ID as PDF_ID
from runtime.artifact_renderer.geometry_primitives import SUPPORTED_PRIMITIVES


class TestDxfRenderer:
    def test_renderer_id(self, dxf_renderer):
        assert dxf_renderer.renderer_id() == DXF_ID

    def test_output_format(self, dxf_renderer):
        assert dxf_renderer.output_format() == "DXF"

    def test_capability_covers_all_primitives(self, dxf_renderer):
        cap = dxf_renderer.capability()
        for pt in SUPPORTED_PRIMITIVES:
            assert cap.supports_primitive(pt)

    def test_render_line(self, dxf_renderer, sample_line, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_line], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "LINE" in content
        assert "EOF" in content

    def test_render_arc(self, dxf_renderer, sample_arc, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_arc], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "ARC" in content

    def test_render_full_circle(self, dxf_renderer, sample_full_circle, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_full_circle], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "CIRCLE" in content

    def test_render_polyline(self, dxf_renderer, sample_polyline, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_polyline], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "LWPOLYLINE" in content

    def test_render_rectangle(self, dxf_renderer, sample_rectangle, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_rectangle], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "LWPOLYLINE" in content

    def test_render_text(self, dxf_renderer, sample_text, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_text], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "PARAPET CAP" in content

    def test_render_hatch(self, dxf_renderer, sample_hatch, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_hatch], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "HATCH" in content
        assert "ANSI31" in content

    def test_render_dimension(self, dxf_renderer, sample_dimension, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_dimension], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert '12"' in content

    def test_render_callout(self, dxf_renderer, sample_callout, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([sample_callout], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "A1" in content

    def test_render_all_primitives(self, dxf_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert content.startswith("0\nSECTION")
        assert content.endswith("EOF")

    def test_header_contains_units(self, dxf_renderer, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([], sample_sheet, sample_layers, sample_metadata)
        assert "$INSUNITS" in content
        assert "AC1015" in content

    def test_layers_defined(self, dxf_renderer, sample_sheet, sample_layers, sample_metadata):
        content, errors = dxf_renderer.render([], sample_sheet, sample_layers, sample_metadata)
        for layer in sample_layers:
            assert layer in content

    def test_deterministic_output(self, dxf_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        c1, _ = dxf_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        c2, _ = dxf_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert c1 == c2


class TestSvgRenderer:
    def test_renderer_id(self, svg_renderer):
        assert svg_renderer.renderer_id() == SVG_ID

    def test_output_format(self, svg_renderer):
        assert svg_renderer.output_format() == "SVG"

    def test_capability_covers_all_primitives(self, svg_renderer):
        cap = svg_renderer.capability()
        for pt in SUPPORTED_PRIMITIVES:
            assert cap.supports_primitive(pt)

    def test_render_line(self, svg_renderer, sample_line, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_line], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "<line" in content
        assert "<svg" in content

    def test_render_arc(self, svg_renderer, sample_arc, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_arc], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "<path" in content

    def test_render_full_circle_as_circle(self, svg_renderer, sample_full_circle, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_full_circle], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "<circle" in content

    def test_render_polyline(self, svg_renderer, sample_polyline, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_polyline], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "<polygon" in content  # closed polyline renders as polygon

    def test_render_open_polyline(self, svg_renderer, sample_sheet, sample_layers, sample_metadata):
        from runtime.artifact_renderer.geometry_primitives import PolylinePrimitive, Point2D
        pl = PolylinePrimitive(points=[Point2D(0, 0), Point2D(5, 0), Point2D(5, 5)], closed=False, layer="A-DETAIL")
        content, errors = svg_renderer.render([pl], sample_sheet, sample_layers, sample_metadata)
        assert "<polyline" in content

    def test_render_rectangle(self, svg_renderer, sample_rectangle, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_rectangle], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "<rect" in content

    def test_render_text(self, svg_renderer, sample_text, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_text], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "PARAPET CAP" in content

    def test_render_hatch(self, svg_renderer, sample_hatch, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_hatch], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "<pattern" in content

    def test_render_dimension(self, svg_renderer, sample_dimension, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_dimension], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "12&quot;" in content or '12"' in content

    def test_render_callout(self, svg_renderer, sample_callout, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([sample_callout], sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert "A1" in content

    def test_svg_structure(self, svg_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert content.startswith("<svg")
        assert content.strip().endswith("</svg>")

    def test_layers_as_groups(self, svg_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert '<g id="A-DETAIL"' in content

    def test_deterministic_output(self, svg_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        c1, _ = svg_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        c2, _ = svg_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert c1 == c2

    def test_title_block_present(self, svg_renderer, sample_sheet, sample_layers, sample_metadata):
        content, errors = svg_renderer.render([], sample_sheet, sample_layers, sample_metadata)
        assert "LOW_SLOPE-PARAPET-EPDM-01" in content

    def test_xml_escaping(self, svg_renderer, sample_sheet, sample_layers, sample_metadata):
        from runtime.artifact_renderer.geometry_primitives import TextPrimitive, Point2D
        text = TextPrimitive(text="<test> & \"quote\"", position=Point2D(1, 1), height=0.2, layer="A-TEXT")
        content, errors = svg_renderer.render([text], sample_sheet, sample_layers, sample_metadata)
        assert "&lt;test&gt;" in content
        assert "&amp;" in content


class TestPdfRenderer:
    def test_renderer_id(self, pdf_renderer):
        assert pdf_renderer.renderer_id() == PDF_ID

    def test_output_format(self, pdf_renderer):
        assert pdf_renderer.output_format() == "PDF"

    def test_capability_covers_all_primitives(self, pdf_renderer):
        cap = pdf_renderer.capability()
        for pt in SUPPORTED_PRIMITIVES:
            assert cap.supports_primitive(pt)

    def test_render_produces_pdf(self, pdf_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        content, errors = pdf_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert len(errors) == 0
        assert content.startswith("%PDF-")
        assert "%%EOF" in content

    def test_pdf_has_pages(self, pdf_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        content, errors = pdf_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert "/Type /Pages" in content
        assert "/Type /Page" in content

    def test_pdf_has_mediabox(self, pdf_renderer, sample_sheet, sample_layers, sample_metadata):
        content, errors = pdf_renderer.render([], sample_sheet, sample_layers, sample_metadata)
        assert "/MediaBox" in content

    def test_pdf_has_title(self, pdf_renderer, sample_sheet, sample_layers, sample_metadata):
        content, errors = pdf_renderer.render([], sample_sheet, sample_layers, sample_metadata)
        assert "LOW_SLOPE-PARAPET-EPDM-01" in content

    def test_deterministic_output(self, pdf_renderer, all_primitives, sample_sheet, sample_layers, sample_metadata):
        c1, _ = pdf_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        c2, _ = pdf_renderer.render(all_primitives, sample_sheet, sample_layers, sample_metadata)
        assert c1 == c2
