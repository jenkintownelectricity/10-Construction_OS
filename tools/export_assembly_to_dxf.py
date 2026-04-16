#!/usr/bin/env python3
"""
export_assembly_to_dxf.py — Barrett PMMA / Fireproofing Assembly-to-DXF Export

Reads assembly JSON records and generates DXF detail drawings using ezdxf.
Each condition generates a DXF file with proper layering for CAD consumption.

Usage:
    python3 tools/export_assembly_to_dxf.py --input output/barrett_pmma_packet/json/ \
                                             --output output/barrett_pmma_packet/dxf/

    python3 tools/export_assembly_to_dxf.py --input output/fireproofing_packet/json/ \
                                             --output output/fireproofing_packet/dxf/

Requirements:
    pip install ezdxf
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import ezdxf
    from ezdxf.enums import TextEntityAlignment
    EZDXF_AVAILABLE = True
except ImportError:
    EZDXF_AVAILABLE = False


# Layer definitions for construction details
LAYERS = {
    "SUBSTRATE":        {"color": 8,  "linetype": "Continuous", "description": "Structural substrate / deck"},
    "INSULATION":       {"color": 31, "linetype": "Continuous", "description": "Insulation layers"},
    "MEMBRANE":         {"color": 5,  "linetype": "Continuous", "description": "PMMA membrane / waterproofing"},
    "REINFORCEMENT":    {"color": 1,  "linetype": "DASHED",     "description": "Fleece reinforcement"},
    "PRIMER":           {"color": 3,  "linetype": "Continuous", "description": "Primer layer"},
    "METAL":            {"color": 7,  "linetype": "Continuous", "description": "Sheet metal / flashing"},
    "SEALANT":          {"color": 6,  "linetype": "Continuous", "description": "Sealant / adhesive"},
    "DIMENSIONS":       {"color": 2,  "linetype": "Continuous", "description": "Dimension lines"},
    "TEXT":             {"color": 7,  "linetype": "Continuous", "description": "Text and callouts"},
    "TITLEBLOCK":       {"color": 7,  "linetype": "Continuous", "description": "Title block border and text"},
    "FIREPROOFING":     {"color": 30, "linetype": "Continuous", "description": "SFRM / fireproofing coating"},
    "STEEL":            {"color": 4,  "linetype": "Continuous", "description": "Structural steel members"},
    "GYPSUM":           {"color": 9,  "linetype": "Continuous", "description": "Gypsum board enclosure"},
    "HIDDEN":           {"color": 8,  "linetype": "HIDDEN",     "description": "Hidden / obscured lines"},
}

# Geometry templates for each condition family
CONDITION_GEOMETRY = {
    "parapet_wall_termination": {
        "type": "section",
        "elements": [
            {"layer": "SUBSTRATE",    "type": "rect", "x": 0, "y": 0,   "w": 400, "h": 30,  "desc": "Concrete Deck"},
            {"layer": "INSULATION",   "type": "rect", "x": 0, "y": 30,  "w": 400, "h": 40,  "desc": "Insulation"},
            {"layer": "SUBSTRATE",    "type": "rect", "x": 400,"y": 0,  "w": 80,  "h": 350, "desc": "Parapet Wall"},
            {"layer": "INSULATION",   "type": "tri",  "x": 360,"y": 70, "w": 40,  "h": 40,  "desc": "Cant Strip"},
            {"layer": "MEMBRANE",     "type": "path", "points": [[0,70],[360,70],[360,110],[400,110],[400,300]], "desc": "PMMA System"},
            {"layer": "REINFORCEMENT","type": "path", "points": [[0,73],[360,73],[363,113],[403,113],[403,297]], "desc": "Fleece"},
            {"layer": "METAL",        "type": "rect", "x": 397,"y": 300,"w": 10,  "h": 5,   "desc": "Term Bar"},
            {"layer": "METAL",        "type": "path", "points": [[390,345],[390,350],[490,350],[490,345],[495,340],[385,340]], "desc": "Coping"},
        ],
        "dimensions": [{"x1": 490, "y1": 110, "x2": 490, "y2": 300, "text": "8\" MIN"}],
    },
    "edge_drip_termination": {"type": "section", "elements": [], "dimensions": []},
    "primary_roof_drain": {"type": "section", "elements": [], "dimensions": []},
    "pipe_penetration": {"type": "section", "elements": [], "dimensions": []},
    "equipment_curb": {"type": "section", "elements": [], "dimensions": []},
    "inside_corner_reinforcement": {"type": "section", "elements": [], "dimensions": []},
    "outside_corner_reinforcement": {"type": "section", "elements": [], "dimensions": []},
    "crack_control_joint": {"type": "section", "elements": [], "dimensions": []},
    "tile_overburden_assembly": {"type": "section", "elements": [], "dimensions": []},
    "expansion_joint": {"type": "section", "elements": [], "dimensions": []},
}


def setup_layers(doc):
    """Add all standard layers to the DXF document."""
    for name, props in LAYERS.items():
        doc.layers.add(name, color=props["color"], linetype=props.get("linetype", "Continuous"))


def add_titleblock(msp, title, subtitle, condition_id, sheet_width=1056, sheet_height=816):
    """Add a standard titleblock to the drawing."""
    # Border
    msp.add_line((20, 20), (sheet_width - 20, 20), dxfattribs={"layer": "TITLEBLOCK"})
    msp.add_line((sheet_width - 20, 20), (sheet_width - 20, sheet_height - 20), dxfattribs={"layer": "TITLEBLOCK"})
    msp.add_line((sheet_width - 20, sheet_height - 20), (20, sheet_height - 20), dxfattribs={"layer": "TITLEBLOCK"})
    msp.add_line((20, sheet_height - 20), (20, 20), dxfattribs={"layer": "TITLEBLOCK"})

    # Title block area
    msp.add_line((20, 80), (sheet_width - 20, 80), dxfattribs={"layer": "TITLEBLOCK"})

    # Title text
    msp.add_text(title, height=12, dxfattribs={"layer": "TEXT"}).set_placement((40, 55))
    msp.add_text(subtitle, height=8, dxfattribs={"layer": "TEXT"}).set_placement((40, 38))
    msp.add_text(f"ID: {condition_id} | DRAFT | 2026-04-16", height=6,
                 dxfattribs={"layer": "TEXT"}).set_placement((40, 26))

    # Branding
    msp.add_text("DETAIL ATLAS — CONSTRUCTION INTELLIGENCE", height=6,
                 dxfattribs={"layer": "TEXT"}).set_placement((sheet_width - 350, 55))
    msp.add_text("CSI 07 62 00 | FAM-BARRETT-PMMA", height=5,
                 dxfattribs={"layer": "TEXT"}).set_placement((sheet_width - 350, 38))


def add_component_callouts(msp, components, start_x=700, start_y=700):
    """Add numbered callout legend from assembly components."""
    y = start_y
    msp.add_text("CALLOUT KEY", height=8, dxfattribs={"layer": "TEXT"}).set_placement((start_x, y))
    y -= 15

    for i, comp in enumerate(components, 1):
        name = comp.get("name", f"Component {i}")
        text = f"{i}. {name}"
        if len(text) > 50:
            text = text[:47] + "..."
        msp.add_text(text, height=5, dxfattribs={"layer": "TEXT"}).set_placement((start_x, y))
        y -= 10


def draw_geometry(msp, geo_template, offset_x=100, offset_y=150):
    """Draw geometry elements from a condition template."""
    for elem in geo_template.get("elements", []):
        layer = elem.get("layer", "SUBSTRATE")
        etype = elem.get("type", "rect")

        if etype == "rect":
            x, y, w, h = elem["x"] + offset_x, elem["y"] + offset_y, elem["w"], elem["h"]
            msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
                               dxfattribs={"layer": layer})
        elif etype == "path":
            points = [(p[0] + offset_x, p[1] + offset_y) for p in elem["points"]]
            msp.add_lwpolyline(points, dxfattribs={"layer": layer})
        elif etype == "tri":
            x, y, w, h = elem["x"] + offset_x, elem["y"] + offset_y, elem["w"], elem["h"]
            msp.add_lwpolyline([(x, y), (x + w, y), (x + w, y + h), (x, y)],
                               dxfattribs={"layer": layer})

    # Add dimensions
    for dim in geo_template.get("dimensions", []):
        x1, y1 = dim["x1"] + offset_x, dim["y1"] + offset_y
        x2, y2 = dim["x2"] + offset_x, dim["y2"] + offset_y
        msp.add_line((x1, y1), (x2, y2), dxfattribs={"layer": "DIMENSIONS", "linetype": "DASHED"})
        mid_y = (y1 + y2) / 2
        msp.add_text(dim["text"], height=6, dxfattribs={"layer": "DIMENSIONS"}).set_placement((x1 + 10, mid_y))


def generate_dxf_for_assembly(assembly_data, output_path):
    """Generate a DXF file from an assembly JSON record."""
    doc = ezdxf.new('R2010')
    setup_layers(doc)
    msp = doc.modelspace()

    assembly_id = assembly_data.get("assembly_id", "unknown")
    condition_type = assembly_data.get("condition_type", "unknown")
    system_type = assembly_data.get("system_type", "")
    components = assembly_data.get("components", [])

    # Title
    title = f"Barrett PMMA — {condition_type.replace('_', ' ').title()}"
    if "fireproofing" in condition_type.lower() or "fp_" in assembly_id:
        title = f"Fireproofing — {condition_type.replace('_', ' ').title()}"

    add_titleblock(msp, title, system_type, assembly_id)

    # Draw geometry if template exists
    geo = CONDITION_GEOMETRY.get(condition_type, {"type": "section", "elements": [], "dimensions": []})
    if geo["elements"]:
        draw_geometry(msp, geo)
    else:
        # Generic placeholder — draw component stack
        y = 600
        for i, comp in enumerate(components):
            seq = comp.get("sequence")
            if seq is None:
                continue
            name = comp.get("name", f"Component {i+1}")
            layer = "MEMBRANE" if "pmma" in name.lower() or "membrane" in name.lower() else \
                    "REINFORCEMENT" if "fleece" in name.lower() or "reinforcement" in name.lower() else \
                    "PRIMER" if "primer" in name.lower() else \
                    "METAL" if "metal" in name.lower() or "coping" in name.lower() else \
                    "FIREPROOFING" if "sfrm" in name.lower() or "fireproof" in name.lower() else \
                    "SUBSTRATE"

            msp.add_lwpolyline(
                [(100, y), (550, y), (550, y - 20), (100, y - 20), (100, y)],
                dxfattribs={"layer": layer}
            )
            msp.add_text(f"{seq}. {name}", height=5,
                         dxfattribs={"layer": "TEXT"}).set_placement((110, y - 14))
            y -= 25

    # Add callout legend
    add_component_callouts(msp, components)

    # Save
    doc.saveas(output_path)
    return True


def main():
    parser = argparse.ArgumentParser(description='Convert assembly JSON records to DXF files')
    parser.add_argument('--input', '-i', required=True, help='Directory containing assembly JSON files')
    parser.add_argument('--output', '-o', required=True, help='Output directory for DXF files')
    args = parser.parse_args()

    if not EZDXF_AVAILABLE:
        print("ERROR: ezdxf library not installed. Run: pip install ezdxf")
        sys.exit(1)

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.is_dir():
        print(f"ERROR: Input directory not found: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(input_dir.glob('*.json'))
    if not json_files:
        print(f"ERROR: No JSON files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(json_files)} assembly JSON files")
    success_count = 0
    fail_count = 0

    for json_path in json_files:
        try:
            with open(json_path) as f:
                assembly = json.load(f)

            assembly_id = assembly.get("assembly_id", json_path.stem)
            dxf_name = assembly_id + ".dxf"
            dxf_path = output_dir / dxf_name

            print(f"  Generating: {dxf_name}")
            generate_dxf_for_assembly(assembly, str(dxf_path))
            success_count += 1

        except Exception as e:
            print(f"  ERROR generating DXF for {json_path.name}: {e}")
            fail_count += 1

    print(f"\nComplete: {success_count} DXF files generated, {fail_count} failures")
    if fail_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
