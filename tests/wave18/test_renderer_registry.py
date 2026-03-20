"""Tests for renderer registry module."""

import pytest
from runtime.artifact_renderer.renderer_registry import (
    RendererRegistry,
    get_global_registry,
)
from runtime.artifact_renderer.dxf_renderer import DxfRenderer
from runtime.artifact_renderer.svg_renderer import SvgRenderer
from runtime.artifact_renderer.pdf_renderer import PdfRenderer
from runtime.artifact_renderer.renderer_errors import RendererNotFoundError


class TestRendererRegistry:
    def test_register_and_get(self):
        reg = RendererRegistry()
        dxf = DxfRenderer()
        reg.register(dxf)
        assert reg.get_renderer("DXF") is dxf

    def test_not_found_raises(self):
        reg = RendererRegistry()
        with pytest.raises(RendererNotFoundError):
            reg.get_renderer("TIFF")

    def test_has_renderer(self):
        reg = RendererRegistry()
        reg.register(DxfRenderer())
        assert reg.has_renderer("DXF")
        assert not reg.has_renderer("SVG")

    def test_list_formats(self, full_registry):
        formats = full_registry.list_formats()
        assert "DXF" in formats
        assert "SVG" in formats
        assert "PDF" in formats

    def test_renderer_count(self, full_registry):
        assert full_registry.renderer_count == 3

    def test_unregister(self, full_registry):
        full_registry.unregister("PDF")
        assert full_registry.renderer_count == 2
        assert not full_registry.has_renderer("PDF")

    def test_get_capability(self, full_registry):
        cap = full_registry.get_capability("DXF")
        assert cap is not None
        assert cap.output_format == "DXF"

    def test_list_capabilities(self, full_registry):
        caps = full_registry.list_capabilities()
        assert len(caps) == 3

    def test_replace_renderer(self):
        reg = RendererRegistry()
        dxf1 = DxfRenderer()
        dxf2 = DxfRenderer()
        reg.register(dxf1)
        reg.register(dxf2)
        assert reg.get_renderer("DXF") is dxf2
        assert reg.renderer_count == 1
