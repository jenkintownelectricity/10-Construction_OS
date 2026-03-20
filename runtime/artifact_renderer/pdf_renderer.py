"""PDF artifact renderer.

Renders geometry primitives to PDF via SVG intermediate.
Pipeline: Primitives -> SVG -> PDF content stream.

Since Cairo/ReportLab are optional dependencies, this renderer
generates a minimal PDF with embedded SVG data. For production,
an SVG-to-Cairo bridge would produce native PDF vector output.

The PDF renderer wraps SVG output in a valid PDF container to ensure
the artifact is a genuine PDF file that can be opened by readers.
"""

from typing import Any
import math

from runtime.artifact_renderer.geometry_primitives import (
    Primitive,
    SUPPORTED_PRIMITIVES,
)
from runtime.artifact_renderer.artifact_contract import RendererCapability
from runtime.artifact_renderer.svg_renderer import SvgRenderer


RENDERER_ID = "artifact_pdf_renderer_v18"
OUTPUT_FORMAT = "PDF"
PDF_VERSION = "1.4"


class PdfRenderer:
    """Renders geometry primitives to PDF format via SVG intermediate."""

    def __init__(self) -> None:
        self._svg_renderer = SvgRenderer()

    def renderer_id(self) -> str:
        return RENDERER_ID

    def output_format(self) -> str:
        return OUTPUT_FORMAT

    def capability(self) -> RendererCapability:
        return RendererCapability(
            renderer_id=RENDERER_ID,
            output_format=OUTPUT_FORMAT,
            supported_primitives=sorted(SUPPORTED_PRIMITIVES),
            version="18.0",
        )

    def render(
        self,
        primitives: list[Primitive],
        sheet: dict[str, Any],
        layers: list[str],
        metadata: dict[str, Any],
    ) -> tuple[str, list[dict[str, str]]]:
        """Render primitives to PDF content.

        Uses SVG intermediate, then wraps in minimal PDF container.
        Returns PDF as a text representation of the content stream.
        """
        # First render to SVG
        svg_content, svg_errors = self._svg_renderer.render(
            primitives, sheet, layers, metadata
        )

        if svg_errors:
            return "", svg_errors

        # Convert SVG to PDF content stream
        width_pt = sheet.get("width", 36.0) * 72.0
        height_pt = sheet.get("height", 24.0) * 72.0

        pdf_content = self._build_pdf(svg_content, width_pt, height_pt, metadata)
        return pdf_content, []

    def _build_pdf(
        self,
        svg_content: str,
        width_pt: float,
        height_pt: float,
        metadata: dict[str, Any],
    ) -> str:
        """Build a minimal PDF document with embedded SVG annotation."""
        title = metadata.get("title", {})
        detail_id = title.get("detail_id", "")
        display_name = title.get("display_name", "")

        # Encode SVG as PDF stream content
        svg_bytes = svg_content.encode("utf-8")
        stream_length = len(svg_bytes)

        objects: list[str] = []

        # Object 1: Catalog
        objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj")

        # Object 2: Pages
        objects.append("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj")

        # Object 3: Page
        objects.append(
            f"3 0 obj\n<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {width_pt:.1f} {height_pt:.1f}] "
            f"/Contents 4 0 R /Resources << >> >>\nendobj"
        )

        # Object 4: Content stream with drawing commands
        content_stream = self._svg_to_pdf_stream(svg_content, width_pt, height_pt)
        stream_len = len(content_stream.encode("utf-8"))
        objects.append(
            f"4 0 obj\n<< /Length {stream_len} >>\nstream\n"
            f"{content_stream}\nendstream\nendobj"
        )

        # Object 5: Info
        objects.append(
            f'5 0 obj\n<< /Title ({_pdf_escape(detail_id)}) '
            f'/Subject ({_pdf_escape(display_name)}) '
            f'/Producer (Construction_Runtime Artifact Renderer v18) >>\nendobj'
        )

        # Build PDF file structure
        lines = [f"%PDF-{PDF_VERSION}"]
        offsets = []
        current_offset = len(lines[0]) + 1

        for obj in objects:
            offsets.append(current_offset)
            lines.append(obj)
            current_offset += len(obj) + 1

        # Cross-reference table
        xref_offset = current_offset
        lines.append("xref")
        lines.append(f"0 {len(objects) + 1}")
        lines.append("0000000000 65535 f ")
        for off in offsets:
            lines.append(f"{off:010d} 00000 n ")

        lines.append("trailer")
        lines.append(
            f"<< /Size {len(objects) + 1} /Root 1 0 R /Info 5 0 R >>"
        )
        lines.append("startxref")
        lines.append(str(xref_offset))
        lines.append("%%EOF")

        return "\n".join(lines)

    def _svg_to_pdf_stream(
        self, svg_content: str, width_pt: float, height_pt: float
    ) -> str:
        """Convert SVG-derived geometry to PDF content stream operators.

        This produces basic PDF drawing commands from the SVG content.
        A production system would use Cairo for full fidelity.
        """
        commands: list[str] = []

        # Save graphics state
        commands.append("q")

        # Set default stroke
        commands.append("0 0 0 RG")
        commands.append("1 w")

        # Draw border
        commands.append(f"0 0 {width_pt:.1f} {height_pt:.1f} re S")

        # Parse SVG for basic geometry and emit PDF operators
        # This is a simplified pass — full fidelity requires Cairo
        import re

        # Extract lines
        for match in re.finditer(
            r'<line x1="([^"]*)" y1="([^"]*)" x2="([^"]*)" y2="([^"]*)"',
            svg_content,
        ):
            x1 = float(match.group(1)) * (72.0 / 30.0)
            y1 = height_pt - float(match.group(2)) * (72.0 / 30.0)
            x2 = float(match.group(3)) * (72.0 / 30.0)
            y2 = height_pt - float(match.group(4)) * (72.0 / 30.0)
            commands.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

        # Extract rectangles
        for match in re.finditer(
            r'<rect x="([^"]*)" y="([^"]*)" width="([^"]*)" height="([^"]*)"',
            svg_content,
        ):
            x = float(match.group(1)) * (72.0 / 30.0)
            y = height_pt - float(match.group(2)) * (72.0 / 30.0)
            w = float(match.group(3)) * (72.0 / 30.0)
            h = float(match.group(4)) * (72.0 / 30.0)
            commands.append(f"{x:.2f} {y - h:.2f} {w:.2f} {h:.2f} re S")

        # Extract circles
        for match in re.finditer(
            r'<circle cx="([^"]*)" cy="([^"]*)" r="([^"]*)"',
            svg_content,
        ):
            cx = float(match.group(1)) * (72.0 / 30.0)
            cy = height_pt - float(match.group(2)) * (72.0 / 30.0)
            r = float(match.group(3)) * (72.0 / 30.0)
            # Approximate circle with 4 Bezier curves
            k = 0.5523 * r
            commands.append(
                f"{cx + r:.2f} {cy:.2f} m "
                f"{cx + r:.2f} {cy + k:.2f} {cx + k:.2f} {cy + r:.2f} {cx:.2f} {cy + r:.2f} c "
                f"{cx - k:.2f} {cy + r:.2f} {cx - r:.2f} {cy + k:.2f} {cx - r:.2f} {cy:.2f} c "
                f"{cx - r:.2f} {cy - k:.2f} {cx - k:.2f} {cy - r:.2f} {cx:.2f} {cy - r:.2f} c "
                f"{cx + k:.2f} {cy - r:.2f} {cx + r:.2f} {cy - k:.2f} {cx + r:.2f} {cy:.2f} c S"
            )

        # Extract text
        for match in re.finditer(
            r'<text x="([^"]*)" y="([^"]*)"[^>]*>([^<]*)</text>',
            svg_content,
        ):
            x = float(match.group(1)) * (72.0 / 30.0)
            y = height_pt - float(match.group(2)) * (72.0 / 30.0)
            text = match.group(3)
            commands.append(f"BT /F1 10 Tf {x:.2f} {y:.2f} Td ({_pdf_escape(text)}) Tj ET")

        # Restore graphics state
        commands.append("Q")

        return "\n".join(commands)


def _pdf_escape(text: str) -> str:
    """Escape text for PDF string literals."""
    return (text
            .replace("\\", "\\\\")
            .replace("(", "\\(")
            .replace(")", "\\)"))
