#!/usr/bin/env python3
"""
svg_section_renderer.py — v3 with WLV-era composition transplant

Renders geometry JSON to PRINT_STANDARD SVG with:
- Concrete stipple pattern overlay on substrate
- Insulation diagonal hatch overlay
- Fleece diagonal pattern
- Non-crossing callout leader routing (vertical sort)
- Condition-specific note boxes
- Extension lines from dimensions to geometry
- Zone-based layout (drawing zone + callout zone + titleblock zone)
"""
import json, sys, math
from pathlib import Path

SHEET_W, SHEET_H = 1056, 816
MARGIN = 60
FONT = "Arial, Helvetica, sans-serif"
DRAW_ZONE_W = 620
CALLOUT_ZONE_X = 700
TITLE_Y = 90
TITLEBLOCK_Y = SHEET_H - 56

LAYER_STYLE = {
    "substrate":  {"fill": "#F0F0F0", "stroke": "#000000", "stroke-width": "1.5", "pattern": "concrete-stipple"},
    "insulation": {"fill": "#E8E8E8", "stroke": "#000000", "stroke-width": "1",   "pattern": "insulation-hatch"},
    "membrane":   {"fill": "#D8D8D8", "stroke": "#333333", "stroke-width": "2",   "pattern": None},
    "fleece":     {"fill": "none",    "stroke": "#333333", "stroke-width": "1.5", "pattern": "fleece-diagonal", "dasharray": "4 2"},
    "metal":      {"fill": "#E0E0E0", "stroke": "#000000", "stroke-width": "1",   "pattern": None},
    "context":    {"fill": "#FAFAFA", "stroke": "#000000", "stroke-width": "0.75","pattern": None},
    "primer":     {"fill": "none",    "stroke": "#333333", "stroke-width": "0.75","pattern": None, "dasharray": "2 1"},
}

def _patterns():
    return """  <defs>
    <pattern id="concrete-stipple" patternUnits="userSpaceOnUse" width="10" height="10">
      <circle cx="2" cy="3" r="0.5" fill="#CCCCCC"/>
      <circle cx="7" cy="8" r="0.5" fill="#CCCCCC"/>
      <circle cx="5" cy="1" r="0.5" fill="#CCCCCC"/>
    </pattern>
    <pattern id="insulation-hatch" patternUnits="userSpaceOnUse" width="8" height="8">
      <path d="M0,8 L8,0" stroke="#999999" stroke-width="0.5" fill="none"/>
    </pattern>
    <pattern id="fleece-diagonal" patternUnits="userSpaceOnUse" width="6" height="6">
      <path d="M0,6 L6,0" stroke="#333333" stroke-width="0.75" fill="none"/>
    </pattern>
  </defs>"""

def _bbox(elements):
    xs, ys = [], []
    for e in elements:
        t = e.get("type")
        if t == "rect":
            xs += [e["x"], e["x"] + e["w"]]
            ys += [e["y"], e["y"] + e["h"]]
        elif t == "line":
            xs += [e["x1"], e["x2"]]
            ys += [e["y1"], e["y2"]]
        elif t == "path":
            for p in e.get("points", []):
                xs.append(p[0]); ys.append(p[1])
        elif t == "circle":
            xs += [e["cx"] - e["r"], e["cx"] + e["r"]]
            ys += [e["cy"] - e["r"], e["cy"] + e["r"]]
    if not xs:
        return 0, 0, SHEET_W, SHEET_H
    return min(xs), min(ys), max(xs), max(ys)

def _transform(elements, dims, callouts):
    x0, y0, x1, y1 = _bbox(elements)
    geo_w, geo_h = x1 - x0, y1 - y0
    draw_x, draw_y = MARGIN, TITLE_Y
    draw_w = DRAW_ZONE_W
    draw_h = SHEET_H - TITLE_Y - 80
    scale = min(draw_w / max(geo_w, 1), draw_h / max(geo_h, 1), 1.0)
    tx = draw_x + (draw_w - geo_w * scale) / 2 - x0 * scale
    ty = draw_y + (draw_h - geo_h * scale) / 2 - y0 * scale
    return tx, ty, scale

def _style(layer):
    return LAYER_STYLE.get(layer, LAYER_STYLE["context"])

def render_element(e, tx, ty, sc):
    t = e.get("type")
    layer = e.get("layer", "context")
    st = _style(layer)
    dash = f' stroke-dasharray="{st.get("dasharray", "")}"' if st.get("dasharray") else ""
    if e.get("style") == "dashed":
        dash = ' stroke-dasharray="4 2"'

    def sx(v): return v * sc + tx
    def sy(v): return v * sc + ty
    def sw(v): return v * sc

    lines = []
    if t == "rect":
        x, y, w, h = sx(e["x"]), sy(e["y"]), sw(e["w"]), sw(e["h"])
        lines.append(f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{st["fill"]}" stroke="{st["stroke"]}" stroke-width="{st["stroke-width"]}"/>')
        if st.get("pattern"):
            lines.append(f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="url(#{st["pattern"]})" opacity="0.4"/>')
        if e.get("label"):
            lx, ly = x + w/2, y + h/2 + 3
            lines.append(f'  <text x="{lx:.1f}" y="{ly:.1f}" font-family="{FONT}" font-size="8" fill="#555" text-anchor="middle">{e["label"]}</text>')

    elif t == "line":
        x1, y1, x2, y2 = sx(e["x1"]), sy(e["y1"]), sx(e["x2"]), sy(e["y2"])
        lines.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{st["stroke"]}" stroke-width="{st["stroke-width"]}"{dash}/>')

    elif t == "path":
        pts = e.get("points", [])
        if not pts:
            return ""
        d = f'M{sx(pts[0][0]):.1f},{sy(pts[0][1]):.1f}'
        for p in pts[1:]:
            d += f' L{sx(p[0]):.1f},{sy(p[1]):.1f}'
        if e.get("closed"):
            d += " Z"
        fill = st["fill"] if e.get("closed") else "none"
        lines.append(f'  <path d="{d}" fill="{fill}" stroke="{st["stroke"]}" stroke-width="{st["stroke-width"]}"{dash}/>')

    elif t == "circle":
        cx, cy, r = sx(e["cx"]), sy(e["cy"]), sw(e["r"])
        lines.append(f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{st["fill"]}" stroke="{st["stroke"]}" stroke-width="{st["stroke-width"]}"/>')

    return "\n".join(lines)

def render_dimension(d, tx, ty, sc):
    def sx(v): return v * sc + tx
    def sy(v): return v * sc + ty
    x1, y1, x2, y2 = sx(d["x1"]), sy(d["y1"]), sx(d["x2"]), sy(d["y2"])
    txt = d.get("text", "")
    side = d.get("side", "right")
    off = 25 if side == "right" else -25
    mx, my = (x1+x2)/2, (y1+y2)/2
    lines = [
        f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x1+off*0.6:.1f}" y2="{y1:.1f}" stroke="#666" stroke-width="0.3" stroke-dasharray="2 2"/>',
        f'  <line x1="{x2:.1f}" y1="{y2:.1f}" x2="{x2+off*0.6:.1f}" y2="{y2:.1f}" stroke="#666" stroke-width="0.3" stroke-dasharray="2 2"/>',
        f'  <line x1="{x1+off:.1f}" y1="{y1:.1f}" x2="{x2+off:.1f}" y2="{y2:.1f}" stroke="#666" stroke-width="0.5" stroke-dasharray="3 2"/>',
        f'  <line x1="{x1+off-4:.1f}" y1="{y1:.1f}" x2="{x1+off+4:.1f}" y2="{y1:.1f}" stroke="#666" stroke-width="0.75"/>',
        f'  <line x1="{x2+off-4:.1f}" y1="{y2:.1f}" x2="{x2+off+4:.1f}" y2="{y2:.1f}" stroke="#666" stroke-width="0.75"/>',
        f'  <text x="{mx+off+8:.1f}" y="{my+3:.1f}" font-family="{FONT}" font-size="9" fill="#000">{txt}</text>',
    ]
    return "\n".join(lines)

def render_callouts(callouts, tx, ty, sc):
    lines = []
    key_x = CALLOUT_ZONE_X
    key_y = 130
    lines.append(f'  <text x="{key_x}" y="{key_y}" font-family="{FONT}" font-size="10" font-weight="bold" fill="#000">CALLOUT KEY</text>')
    lines.append(f'  <line x1="{key_x}" y1="{key_y+5}" x2="{key_x+220}" y2="{key_y+5}" stroke="#000" stroke-width="0.5"/>')

    sorted_c = sorted(callouts, key=lambda c: c.get("cy", 0))
    slot_y = key_y + 25
    slot_spacing = min(22, max(16, (TITLEBLOCK_Y - 100 - key_y - 25) / max(len(sorted_c), 1)))

    for i, c in enumerate(sorted_c):
        cx = c["cx"] * sc + tx
        cy = c["cy"] * sc + ty
        n = c["number"]
        label = c.get("label", "")

        ky = slot_y + i * slot_spacing
        lx = key_x - 10

        lines.append(f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="#000"/>')
        lines.append(f'  <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{lx:.1f}" y2="{ky:.1f}" stroke="#000" stroke-width="0.5"/>')
        lines.append(f'  <circle cx="{key_x+6}" cy="{ky-3}" r="4" fill="#000"/>')
        lines.append(f'  <text x="{key_x+6}" y="{ky}" font-family="{FONT}" font-size="7" fill="#FFF" text-anchor="middle" font-weight="bold">{n}</text>')
        lines.append(f'  <text x="{key_x+16}" y="{ky}" font-family="{FONT}" font-size="9" fill="#000">{label}</text>')

    return "\n".join(lines)

def render_notes(notes, geo):
    if not notes:
        return ""
    lines = []
    ny = TITLEBLOCK_Y - 60
    for note in notes:
        box_w = 400
        lines.append(f'  <rect x="{MARGIN}" y="{ny}" width="{box_w}" height="22" rx="3" fill="#FAFAFA" stroke="#000" stroke-width="0.75"/>')
        lines.append(f'  <text x="{MARGIN+8}" y="{ny+15}" font-family="{FONT}" font-size="8" fill="#000"><tspan font-weight="bold">NOTE: </tspan>{note}</text>')
        ny -= 28
    return "\n".join(lines)

def render_titleblock(geo):
    y = TITLEBLOCK_Y
    title = geo.get("title", "Untitled")
    code = geo.get("output_code", "")
    system = geo.get("system", "")
    fam = geo.get("family_id", "")
    cid = geo.get("condition_id", "")
    return f"""  <line x1="{MARGIN}" y1="{y}" x2="{SHEET_W-MARGIN}" y2="{y}" stroke="#000" stroke-width="0.75"/>
  <text x="{MARGIN}" y="{y+18}" font-family="{FONT}" font-size="11" font-weight="bold" fill="#000">DETAIL ATLAS</text>
  <text x="{MARGIN+130}" y="{y+18}" font-family="{FONT}" font-size="9" fill="#333">CONSTRUCTION INTELLIGENCE</text>
  <text x="450" y="{y+18}" font-family="{FONT}" font-size="9" fill="#333">{system} | {code}</text>
  <text x="{SHEET_W-MARGIN-120}" y="{y+18}" font-family="{FONT}" font-size="9" fill="#333">DRAFT | 2026-04-16</text>
  <text x="{MARGIN}" y="{y+34}" font-family="{FONT}" font-size="8" fill="#666">{fam} | {cid} | v3 Parametric Renderer</text>"""

def render(geo_path, svg_path):
    with open(geo_path) as f:
        geo = json.load(f)

    elements = geo.get("elements", [])
    dimensions = geo.get("dimensions", [])
    callouts = geo.get("callouts", [])
    title = geo.get("title", "Untitled")
    notes = geo.get("notes", [])
    ctype = geo.get("condition_type", "")

    tx, ty, sc = _transform(elements, dimensions, callouts)

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SHEET_W} {SHEET_H}" width="{SHEET_W}" height="{SHEET_H}">',
        _patterns(),
        f'  <rect width="{SHEET_W}" height="{SHEET_H}" fill="#FFFFFF"/>',
        f'  <text x="{SHEET_W//2}" y="{SHEET_H//2}" font-family="{FONT}" font-size="48" fill="#CCC" opacity="0.3" text-anchor="middle" transform="rotate(-25 {SHEET_W//2} {SHEET_H//2})">DRAFT FOR REVIEW</text>',
        f'  <text x="{MARGIN}" y="40" font-family="{FONT}" font-size="16" font-weight="bold" fill="#000">{title}</text>',
        f'  <text x="{MARGIN}" y="58" font-family="{FONT}" font-size="11" fill="#333">Section Detail — Rendered from parametric geometry (v3)</text>',
        f'  <line x1="{MARGIN}" y1="66" x2="{DRAW_ZONE_W}" y2="66" stroke="#000" stroke-width="0.5"/>',
    ]

    for e in elements:
        svg_lines.append(render_element(e, tx, ty, sc))
    for d in dimensions:
        svg_lines.append(render_dimension(d, tx, ty, sc))
    svg_lines.append(render_callouts(callouts, tx, ty, sc))
    svg_lines.append(render_notes(notes, geo))
    svg_lines.append(render_titleblock(geo))
    svg_lines.append("</svg>")

    Path(svg_path).parent.mkdir(parents=True, exist_ok=True)
    with open(svg_path, "w") as f:
        f.write("\n".join(svg_lines))
    return svg_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 svg_section_renderer.py input.json output.svg")
        sys.exit(1)
    result = render(sys.argv[1], sys.argv[2])
    print(f"Rendered: {result}")
