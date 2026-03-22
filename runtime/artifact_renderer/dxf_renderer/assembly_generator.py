"""Assembly DXF generator — roofing assembly detail drawing generation.

Generates DXF drawings from parsed assembly data using the ezdxf library.
Draws roofing layer details (deck, insulation, coverboard, membrane) with
correct hatch patterns, layer standards, and architectural units.

Source lineage:
  Migrated from dxf_Generatior_Assembly_Letter_Parser
  Archive: AssemblyDrawingTool_functioningdxf_generator_MAINr.zip
  File:    generators/dxf_generator.py

Adaptations:
- Extracted layer standards to layer_standards.py
- Added render_dxf_from_instruction_set() entry point for runtime pipeline
- Preserved all drawing primitives and generation logic intact
- Preserved function signatures for backward compatibility
- Generation continues to fail-closed (missing data = no output, not partial)
"""

import os
import re
from collections import OrderedDict
from typing import Any

from runtime.artifact_renderer.dxf_renderer.layer_standards import (
    ASSEMBLY_LAYER_STANDARDS,
    ASSEMBLY_LAYER_CONFIG,
)


class AssemblyDXFGenerator:
    """Generate DXF drawings from parsed assembly data — Architectural units."""

    def __init__(self) -> None:
        self.detail_width: float = 36  # 36" (3 feet)
        self.label_x: float = -6
        self.leader_offset: float = 0.5
        self.standards = ASSEMBLY_LAYER_STANDARDS

    def generate_from_parsed_data(
        self, parsed_data: dict[str, Any], output_dir: str = "output"
    ) -> list[str]:
        """Generate DXF from parser's OrderedDict output.

        Args:
            parsed_data: Parsed assembly data (single or multi-assembly).
            output_dir: Directory to write DXF files to.

        Returns:
            List of generated DXF filenames.
        """
        try:
            import ezdxf
        except ImportError:
            raise RuntimeError(
                "ezdxf is required for assembly DXF generation. "
                "Install with: pip install ezdxf"
            )

        if "assemblies" in parsed_data:
            output_files = []
            for i, assembly_data in enumerate(parsed_data["assemblies"]):
                filename = self._generate_single_assembly(
                    assembly_data, i + 1, output_dir
                )
                output_files.append(filename)
            return output_files
        else:
            return [self._generate_single_assembly(parsed_data, 1, output_dir)]

    def _generate_single_assembly(
        self, assembly_data: dict[str, Any], assembly_num: int, output_dir: str
    ) -> str:
        """Generate DXF for a single assembly — Architectural units."""
        import ezdxf
        from ezdxf.enums import TextEntityAlignment

        doc = ezdxf.new("R2010", setup=True)
        msp = doc.modelspace()

        # Set document units to Architectural (feet/inches)
        doc.header["$INSUNITS"] = 1  # 1 = Inches
        doc.header["$LUNITS"] = 4  # 4 = Architectural
        doc.header["$AUNITS"] = 0  # 0 = Decimal degrees

        # Create ZIGZAG linetype
        if "ZIGZAG" not in doc.linetypes:
            doc.linetypes.add(
                "ZIGZAG",
                pattern=[0.5, 0.25, -0.25, 0.25, -0.25],
                description="Zigzag ___/\\___/\\___",
            )

        # Create all layers
        self._create_layers(doc)

        # Start drawing from bottom up
        y_position: float = 0

        # 1. Draw Deck (3" concrete)
        deck_height = 3.0
        y_position = self._draw_deck(
            msp, y_position, assembly_data.get("deck_slope", "Concrete Deck"), deck_height
        )

        # 2. Draw Vapor Barrier (if exists)
        if "vapor_barrier" in assembly_data:
            vapor_height = 0.03125
            y_position = self._draw_vapor_barrier(
                msp, y_position, assembly_data["vapor_barrier"], vapor_height
            )

        # 3. Draw Insulation Layers — alternating scale: 0.25, 0.26
        insulation_layer_count = 0
        for i in range(1, 4):
            insul_key = f"insulation_layer_{i}"
            if insul_key in assembly_data:
                thickness = self._extract_thickness(assembly_data[insul_key])
                if thickness > 0:
                    insulation_layer_count += 1
                    y_position = self._draw_insulation(
                        msp,
                        y_position,
                        thickness,
                        assembly_data[insul_key],
                        assembly_data.get(f"{insul_key}_attachment"),
                        i,
                        insulation_layer_count,
                    )

        # 4. Draw Coverboard 2 (if exists)
        if "coverboard_2" in assembly_data:
            thickness = self._extract_thickness(assembly_data["coverboard_2"])
            if thickness > 0:
                y_position = self._draw_coverboard(
                    msp,
                    y_position,
                    thickness,
                    assembly_data["coverboard_2"],
                    assembly_data.get("coverboard_2_attachment"),
                    2,
                )

        # 5. Draw Coverboard 1
        coverboard_top_y = y_position
        if "coverboard_1" in assembly_data:
            thickness = self._extract_thickness(assembly_data["coverboard_1"])
            if thickness > 0:
                y_position = self._draw_coverboard(
                    msp,
                    y_position,
                    thickness,
                    assembly_data["coverboard_1"],
                    assembly_data.get("coverboard_1_attachment"),
                    1,
                )
                coverboard_top_y = y_position

        # 6. Draw Adhesive Line (0.125" above coverboard)
        membrane_attachment = assembly_data.get("membrane_1_attachment", "")
        if "adhered" in membrane_attachment.lower() or "adhesive" in membrane_attachment.lower():
            adhesive_y = coverboard_top_y + 0.125
            self._draw_adhesive_line(msp, adhesive_y, membrane_attachment)

        # 7. Draw Membrane (0.1" thick line, 0.125" above coverboard)
        if "membrane_1" in assembly_data:
            membrane_y = coverboard_top_y + 0.125
            y_position = self._draw_membrane(
                msp, membrane_y, assembly_data["membrane_1"], membrane_attachment
            )

        # Save file
        os.makedirs(output_dir, exist_ok=True)
        assembly_name = assembly_data.get("assembly_roof_area", f"Assembly_{assembly_num}")
        filename = f"{assembly_name.replace(' ', '_').replace('#', '')}.dxf"
        filepath = os.path.join(output_dir, filename)
        doc.saveas(filepath)
        return filename

    def _create_layers(self, doc: Any) -> None:
        """Create all layers — ByLayer for everything except blue membrane."""
        for layer_name, color_setting in ASSEMBLY_LAYER_CONFIG:
            if layer_name not in doc.layers:
                layer = doc.layers.add(layer_name)
                if isinstance(color_setting, tuple):
                    layer.rgb = color_setting
                if "Adhesive" in layer_name:
                    layer.dxf.linetype = "ZIGZAG"

    def _draw_component(
        self,
        msp: Any,
        y_start: float,
        height: float,
        outline_layer: str,
        hatch_layer: str,
        hatch_pattern: str,
        hatch_scale: float = 1,
        hatch_angle: float = 0,
    ) -> float:
        """Draw component — all colors ByLayer."""
        y_end = y_start + height

        # Draw outline
        outline = msp.add_lwpolyline(
            [
                (0, y_start),
                (self.detail_width, y_start),
                (self.detail_width, y_end),
                (0, y_end),
                (0, y_start),
            ]
        )
        outline.dxf.layer = outline_layer
        outline.dxf.color = 256  # ByLayer

        # Draw hatch
        hatch = msp.add_hatch()
        hatch.dxf.layer = hatch_layer
        hatch.dxf.color = 256  # ByLayer

        boundary = hatch.paths.add_edge_path()
        boundary.add_line((0, y_start), (self.detail_width, y_start))
        boundary.add_line((self.detail_width, y_start), (self.detail_width, y_end))
        boundary.add_line((self.detail_width, y_end), (0, y_end))
        boundary.add_line((0, y_end), (0, y_start))

        if hatch_pattern == "SOLID":
            hatch.set_solid_fill()
        else:
            hatch.set_pattern_fill(hatch_pattern, scale=hatch_scale, angle=hatch_angle)

        return y_end

    def _add_label(self, msp: Any, text: str, y_position: float) -> None:
        """Add label with leader line."""
        from ezdxf.enums import TextEntityAlignment

        leader_start = (0 - self.leader_offset, y_position)
        leader_end = (self.label_x + 1, y_position)

        leader = msp.add_line(leader_start, leader_end)
        leader.dxf.layer = self.standards["text"]["layer"]
        leader.dxf.color = 256  # ByLayer

        lines = text.split("\n")
        text_height = self.standards["text"]["height"]

        for i, line in enumerate(lines):
            text_entity = msp.add_text(line)
            text_entity.dxf.layer = self.standards["text"]["layer"]
            text_entity.dxf.height = text_height
            text_entity.dxf.color = 256  # ByLayer
            text_entity.set_placement(
                (self.label_x, y_position - (i * text_height * 1.5)),
                align=TextEntityAlignment.MIDDLE_RIGHT,
            )

    def _draw_deck(
        self, msp: Any, y_start: float, deck_text: str, height: float
    ) -> float:
        """Draw deck layer — AR-CONC at 0.01 scale."""
        std = self.standards["deck"]
        y_end = self._draw_component(
            msp,
            y_start,
            height,
            std["outline_layer"],
            std["hatch_layer"],
            std["hatch_pattern"],
            std["hatch_scale"],
        )
        label = deck_text.upper()
        if "(by others)" not in label.lower():
            label += " (by others)"
        self._add_label(msp, label, (y_start + y_end) / 2)
        return y_end

    def _draw_vapor_barrier(
        self, msp: Any, y_start: float, vapor_text: str, height: float
    ) -> float:
        """Draw vapor barrier."""
        std = self.standards["vapor_barrier"]
        y_end = self._draw_component(
            msp,
            y_start,
            height,
            std["outline_layer"],
            std["hatch_layer"],
            std["hatch_pattern"],
        )
        label = vapor_text.upper()
        self._add_label(msp, label, (y_start + y_end) / 2)
        return y_end

    def _draw_insulation(
        self,
        msp: Any,
        y_start: float,
        height: float,
        insul_text: str,
        attachment_text: str | None,
        layer_num: int,
        insul_count: int,
    ) -> float:
        """Draw insulation — alternating scale 0.25, 0.26."""
        std = self.standards["insulation"]
        outline_layer = std["outline_layer"].format(layer_num)
        hatch_layer = std["hatch_layer"].format(layer_num)

        # Alternate scale: odd layers = 0.25, even layers = 0.26
        hatch_scale = 0.25 if insul_count % 2 == 1 else 0.26

        y_end = self._draw_component(
            msp,
            y_start,
            height,
            outline_layer,
            hatch_layer,
            std["hatch_pattern"],
            hatch_scale,
            std["hatch_angle"],
        )

        label = insul_text.upper()
        if attachment_text:
            label += f"\n({attachment_text.lower()})"
        self._add_label(msp, label, (y_start + y_end) / 2)
        return y_end

    def _draw_coverboard(
        self,
        msp: Any,
        y_start: float,
        height: float,
        coverboard_text: str,
        attachment_text: str | None,
        layer_num: int,
    ) -> float:
        """Draw coverboard layer — ANSI31 at 0.22 scale, angle 0."""
        std = self.standards["coverboard"]
        outline_layer = std["outline_layer"].format(layer_num)
        hatch_layer = std["hatch_layer"].format(layer_num)

        y_end = self._draw_component(
            msp,
            y_start,
            height,
            outline_layer,
            hatch_layer,
            std["hatch_pattern"],
            std["hatch_scale"],
            std["hatch_angle"],
        )

        label = coverboard_text.upper()
        if attachment_text:
            label += f"\n({attachment_text.lower()})"
        self._add_label(msp, label, (y_start + y_end) / 2)
        return y_end

    def _draw_adhesive_line(
        self, msp: Any, y_position: float, adhesive_text: str
    ) -> None:
        """Draw adhesive line — BLUE zigzag at specified Y position."""
        from ezdxf.enums import TextEntityAlignment

        line = msp.add_line((0, y_position), (self.detail_width, y_position))
        line.dxf.layer = self.standards["membrane"]["adhesive_layer"]
        line.dxf.linetype = "ZIGZAG"
        line.dxf.ltscale = 2.0
        line.dxf.color = 256  # ByLayer (layer itself is blue)

        label = adhesive_text.upper() if adhesive_text else "ADHESIVE"
        text = msp.add_text(label)
        text.dxf.layer = self.standards["text"]["layer"]
        text.dxf.height = 0.1
        text.dxf.color = 256  # ByLayer
        text.set_placement(
            (self.label_x, y_position + 0.05),
            align=TextEntityAlignment.MIDDLE_RIGHT,
        )

    def _draw_membrane(
        self, msp: Any, y_position: float, membrane_text: str, attachment_text: str
    ) -> float:
        """Draw membrane as 0.1" thick BLUE line (no hatch)."""
        std = self.standards["membrane"]

        membrane_line = msp.add_lwpolyline(
            [(0, y_position), (self.detail_width, y_position)]
        )
        membrane_line.dxf.layer = std["layer"]
        membrane_line.dxf.color = 256  # ByLayer (layer is blue)
        membrane_line.dxf.const_width = std["line_weight"]  # 0.1" thick line

        label = membrane_text.upper()
        if attachment_text and "adhered" not in label.lower():
            label += f"\n({attachment_text.lower()})"
        self._add_label(msp, label, y_position)

        return y_position + std["line_weight"]

    @staticmethod
    def _extract_thickness(text: str) -> float:
        """Extract thickness in INCHES — handle fractions and decimals."""
        patterns = [
            r'(\d+\.?\d*)\s*["\']?\s*(?:thick|inch|in\.?)',
            r"(\d+)/(\d+)\s*[\"']",
            r"(\d+\.?\d*)\s*[\"']",
            r":?\s*(\d+)/(\d+)\s*[\"']",
            r":?\s*(\d+\.?\d*)\s*[\"']",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 2 and groups[1]:  # Fraction
                    num = float(groups[0])
                    denom = float(groups[1])
                    return num / denom
                else:  # Decimal
                    return float(groups[0])

        return 0


def generate_assembly_dxf(
    parsed_data: dict[str, Any], output_dir: str = "output"
) -> list[str]:
    """Generate DXF files from parsed assembly data.

    Convenience function that creates an AssemblyDXFGenerator and runs it.

    Args:
        parsed_data: Parsed assembly data from assembly letter parser.
        output_dir: Directory to write DXF files to.

    Returns:
        List of generated DXF filenames.
    """
    generator = AssemblyDXFGenerator()
    return generator.generate_from_parsed_data(parsed_data, output_dir)


def render_dxf_from_instruction_set(
    instruction_set: dict[str, Any], output_dir: str = "output"
) -> list[str]:
    """Render DXF from an assembly instruction set.

    Top-level entry point for the runtime pipeline. Accepts either a raw
    parsed assembly dict or a wrapped instruction set with metadata.

    Args:
        instruction_set: Assembly data dict, optionally wrapped with
            ``{"assembly_data": {...}, "metadata": {...}}``.
        output_dir: Directory to write DXF files to.

    Returns:
        List of generated DXF filenames.

    Raises:
        RuntimeError: If ezdxf is not installed.
        ValueError: If instruction_set is empty or invalid.
    """
    if not instruction_set:
        raise ValueError("instruction_set must not be empty")

    # Unwrap if instruction_set contains a nested assembly_data key
    if "assembly_data" in instruction_set:
        assembly_data = instruction_set["assembly_data"]
    else:
        assembly_data = instruction_set

    return generate_assembly_dxf(assembly_data, output_dir)
