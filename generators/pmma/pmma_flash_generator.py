#!/usr/bin/env python3
"""
pmma_flash_generator.py — Barrett PMMA Parametric Detail Generator

Generates normalized geometry payloads for 10 PMMA conditions
from calibration measurements and assembly DNA rules.

Usage:
    from generators.pmma.pmma_flash_generator import generate_condition
    result = generate_condition("equipment_curb", calibration, template)
"""

import json
from pathlib import Path

# Pixels per inch for SVG output (30px = 1 inch at screen scale)
PPI = 30

def _load_json(path):
    with open(path) as f:
        return json.load(f)


def _make_rect(x, y, w, h, layer="substrate", label=None):
    return {"type": "rect", "x": x, "y": y, "w": w, "h": h, "layer": layer, "label": label}


def _make_line(x1, y1, x2, y2, layer="membrane", style="solid"):
    return {"type": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "layer": layer, "style": style}


def _make_path(points, layer="membrane", style="solid", closed=False):
    return {"type": "path", "points": points, "layer": layer, "style": style, "closed": closed}


def _make_circle(cx, cy, r, layer="substrate"):
    return {"type": "circle", "cx": cx, "cy": cy, "r": r, "layer": layer}


def _make_dim(x1, y1, x2, y2, text, side="right"):
    return {"type": "dimension", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "text": text, "side": side}


def _make_callout(num, label, cx, cy):
    return {"number": num, "label": label, "cx": cx, "cy": cy}


def _base_geometry(condition_type, title, code):
    return {
        "condition_type": condition_type,
        "title": f"Barrett PMMA — {title}",
        "output_code": code,
        "system": "RamFlash PMMA",
        "family_id": "FAM-BARRETT-PMMA",
        "elements": [],
        "dimensions": [],
        "callouts": [],
        "notes": [],
        "layer_stack": []
    }


# === CONDITION GENERATORS ===

def generate_parapet(cal):
    g = cal.get("geometry", {})
    slab_t = (g.get("slab_thickness") or 6) * PPI
    ins_t = (g.get("insulation_thickness") or 3) * PPI
    wall_t = (g.get("wall_thickness") or 8) * PPI
    turnup = (g.get("turnup_height") or 8) * PPI
    cant = (g.get("cant_dimension") or 4) * PPI

    geo = _base_geometry("parapet_wall_termination", "Parapet Wall Termination", "LF-PW-01")
    bx, by = 100, 400  # base origin

    geo["elements"] = [
        _make_rect(bx, by, 400, slab_t, "substrate", "Structural Slab"),
        _make_rect(bx, by - ins_t, 400, ins_t, "insulation", "Insulation"),
        _make_rect(bx + 400, by - turnup - slab_t, wall_t, turnup + slab_t + ins_t, "substrate", "Parapet Wall"),
        _make_path([(bx + 400 - cant, by - ins_t), (bx + 400, by - ins_t), (bx + 400, by - ins_t - cant)], "context", "solid", True),
        _make_line(bx, by - ins_t - 3, bx + 400, by - ins_t - 3, "membrane"),
        _make_line(bx + 400 + 3, by - ins_t - cant, bx + 400 + 3, by - ins_t - turnup, "membrane"),
        _make_line(bx, by - ins_t - 6, bx + 400, by - ins_t - 6, "fleece", "dashed"),
        _make_rect(bx + 400 - 2, by - ins_t - turnup, wall_t + 4, 4, "metal", "Termination Bar"),
        _make_rect(bx + 395, by - ins_t - turnup - 15, wall_t + 10, 10, "metal", "Metal Coping"),
    ]
    geo["dimensions"] = [_make_dim(bx + 400 + wall_t + 10, by - ins_t, bx + 400 + wall_t + 10, by - ins_t - turnup, '8" MIN')]
    geo["callouts"] = [
        _make_callout(1, "Substrate", bx + 200, by + slab_t/2),
        _make_callout(2, "Insulation", bx + 200, by - ins_t/2),
        _make_callout(3, "Cant Strip", bx + 390, by - ins_t - cant/2),
        _make_callout(4, "PMMA Primer", bx + 150, by - ins_t - 2),
        _make_callout(5, "Fleece Reinforcement", bx + 150, by - ins_t - 5),
        _make_callout(6, "PMMA Membrane", bx + 150, by - ins_t - 8),
        _make_callout(7, "Termination Bar + Sealant", bx + 420, by - ins_t - turnup + 2),
        _make_callout(8, "Metal Coping", bx + 420, by - ins_t - turnup - 10),
    ]
    geo["layer_stack"] = ["substrate", "insulation", "cant_strip", "primer", "pmma_resin", "fleece", "seal_coat", "termination_bar", "coping"]
    return geo


def generate_edge(cal):
    g = cal.get("geometry", {})
    geo = _base_geometry("edge_drip_termination", "Edge / Drip Edge", "LF-ED-01")
    geo["elements"] = [
        _make_rect(100, 400, 400, (g.get("slab_thickness") or 6) * PPI, "substrate"),
        _make_rect(100, 400 - (g.get("insulation_thickness") or 3) * PPI, 400, (g.get("insulation_thickness") or 3) * PPI, "insulation"),
        _make_line(100, 400 - (g.get("insulation_thickness") or 3) * PPI - 3, 500, 400 - (g.get("insulation_thickness") or 3) * PPI - 3, "membrane"),
        _make_line(500, 400 - (g.get("insulation_thickness") or 3) * PPI - 3, 500, 400 + 20, "membrane"),
        _make_rect(497, 400 + 15, 60, 3, "metal", "Drip Edge"),
    ]
    geo["dimensions"] = [_make_dim(500, 400 + 18, 560, 400 + 18, '2" MIN OVERHANG')]
    geo["callouts"] = [
        _make_callout(1, "Substrate", 300, 430),
        _make_callout(2, "Insulation", 300, 380),
        _make_callout(3, "PMMA System", 300, 370),
        _make_callout(4, "Drip Edge Metal", 530, 418),
    ]
    geo["layer_stack"] = ["substrate", "insulation", "primer", "pmma_resin", "fleece", "seal_coat", "drip_edge"]
    return geo


def generate_primary_drain(cal):
    g = cal.get("geometry", {})
    geo = _base_geometry("primary_roof_drain", "Primary Roof Drain", "LF-DR-01")
    collar_r = (g.get("fleece_collar_radius") or 4) * PPI
    geo["elements"] = [
        _make_rect(100, 400, 500, (g.get("slab_thickness") or 6) * PPI, "substrate"),
        _make_rect(100, 340, 500, 60, "insulation"),
        _make_circle(350, 420, 30, "metal"),
        _make_circle(350, 340, collar_r, "fleece"),
        _make_rect(330, 320, 40, 10, "metal", "Clamping Ring"),
        _make_circle(350, 310, 15, "metal"),
    ]
    geo["dimensions"] = [_make_dim(350, 340, 350 + collar_r, 340, f'{g.get("fleece_collar_radius") or 4}" MIN COLLAR')]
    geo["callouts"] = [
        _make_callout(1, "Substrate", 200, 430),
        _make_callout(2, "Tapered Insulation", 200, 370),
        _make_callout(3, "Drain Body", 350, 420),
        _make_callout(4, "Fleece Collar", 350 + collar_r - 10, 345),
        _make_callout(5, "Clamping Ring", 375, 325),
        _make_callout(6, "Strainer Dome", 350, 305),
    ]
    geo["layer_stack"] = ["substrate", "insulation", "drain_body", "primer", "pmma_resin", "fleece_collar", "seal_coat", "clamping_ring", "strainer"]
    return geo


def generate_pipe_penetration(cal):
    g = cal.get("geometry", {})
    turnup = (g.get("turnup_height") or 4) * PPI
    geo = _base_geometry("pipe_penetration", "Pipe Penetration", "LF-PP-01")
    geo["elements"] = [
        _make_rect(100, 400, 500, (g.get("slab_thickness") or 6) * PPI, "substrate"),
        _make_rect(100, 340, 500, 60, "insulation"),
        _make_rect(340, 250, 20, 190, "metal", "Pipe Sleeve"),
        _make_line(320, 340, 320, 340 - turnup, "membrane"),
        _make_line(380, 340, 380, 340 - turnup, "membrane"),
        _make_rect(335, 340 - turnup - 5, 30, 5, "metal", "Storm Collar"),
    ]
    geo["dimensions"] = [_make_dim(390, 340, 390, 340 - turnup, f'{g.get("turnup_height") or 4}" MIN')]
    geo["callouts"] = [
        _make_callout(1, "Substrate", 200, 430),
        _make_callout(2, "Pipe Sleeve", 350, 290),
        _make_callout(3, "PMMA Fleece Boot", 340, 330),
        _make_callout(4, "Storm Collar", 365, 340 - turnup - 2),
    ]
    geo["layer_stack"] = ["substrate", "insulation", "pipe_sleeve", "primer", "fleece_boot", "pmma_resin", "seal_coat", "storm_collar", "sealant"]
    return geo


def generate_equipment_curb(cal):
    g = cal.get("geometry", {})
    curb_h = (g.get("curb_height") or 8) * PPI
    curb_w = (g.get("curb_width") or 6) * PPI
    cant = (g.get("cant_dimension") or 4) * PPI
    ext = (g.get("horizontal_extension") or 3) * PPI

    geo = _base_geometry("equipment_curb", "Equipment Curb", "LF-CU-01")
    bx, by = 200, 450

    geo["elements"] = [
        _make_rect(100, by, 500, (g.get("slab_thickness") or 6) * PPI, "substrate"),
        _make_rect(100, by - 60, 500, 60, "insulation"),
        _make_rect(bx, by - 60 - curb_h, curb_w, curb_h, "substrate", "Curb Frame"),
        _make_path([(bx - cant, by - 60), (bx, by - 60), (bx, by - 60 - cant)], "context", "solid", True),
        _make_line(bx - ext, by - 63, bx, by - 63, "membrane"),
        _make_line(bx + 3, by - 60 - cant, bx + 3, by - 60 - curb_h, "membrane"),
        _make_line(bx - ext, by - 66, bx, by - 66, "fleece", "dashed"),
        _make_rect(bx - 5, by - 60 - curb_h - 8, curb_w + 10, 8, "metal", "Counter-Flashing"),
    ]
    geo["dimensions"] = [_make_dim(bx + curb_w + 15, by - 60, bx + curb_w + 15, by - 60 - curb_h, f'{g.get("curb_height") or 8}" MIN')]
    geo["callouts"] = [
        _make_callout(1, "Substrate / Deck", 400, by + 30),
        _make_callout(2, "Insulation", 400, by - 30),
        _make_callout(3, "Curb Frame", bx + curb_w/2, by - 60 - curb_h/2),
        _make_callout(4, "Cant Strip", bx - cant/2, by - 60 - cant/2),
        _make_callout(5, "PMMA System", bx - ext/2, by - 64),
        _make_callout(6, "Fleece", bx - ext/2, by - 67),
        _make_callout(7, "Counter-Flashing", bx + curb_w/2, by - 60 - curb_h - 4),
    ]
    geo["layer_stack"] = ["substrate", "insulation", "curb_frame", "nailer", "cant_strip", "primer", "pmma_resin", "fleece", "seal_coat", "counter_flashing"]
    return geo


def generate_inside_corner(cal):
    g = cal.get("geometry", {})
    ext = (g.get("corner_reinforcement_extension") or 4) * PPI
    geo = _base_geometry("inside_corner_reinforcement", "Inside Corner Reinforcement", "LF-IC-01")
    geo["elements"] = [
        _make_rect(200, 200, 20, 250, "substrate", "Vertical Surface"),
        _make_rect(220, 430, 250, 20, "substrate", "Horizontal Surface"),
        _make_line(220, 430 - ext, 220, 430, "membrane"),
        _make_line(220, 430, 220 + ext, 430, "membrane"),
        _make_line(223, 430 - ext, 223, 430, "fleece", "dashed"),
        _make_line(220, 427, 220 + ext, 427, "fleece", "dashed"),
    ]
    geo["dimensions"] = [
        _make_dim(190, 430 - ext, 190, 430, f'{g.get("corner_reinforcement_extension") or 4}" MIN'),
        _make_dim(220, 460, 220 + ext, 460, f'{g.get("corner_reinforcement_extension") or 4}" MIN'),
    ]
    geo["notes"] = ["3-STEP REINFORCEMENT: 1) Primer  2) Embed fleece in wet resin  3) Seal coat"]
    geo["layer_stack"] = ["primer", "pmma_resin", "fleece", "seal_coat"]
    return geo


def generate_outside_corner(cal):
    g = cal.get("geometry", {})
    ext = (g.get("corner_reinforcement_extension") or 4) * PPI
    geo = _base_geometry("outside_corner_reinforcement", "Outside Corner Reinforcement", "LF-OC-01")
    geo["elements"] = [
        _make_rect(200, 200, 20, 250, "substrate"),
        _make_rect(100, 430, 120, 20, "substrate"),
        _make_line(197, 430 - ext, 197, 430, "membrane"),
        _make_line(100, 427, 200, 427, "membrane"),
        _make_line(194, 430 - ext, 194, 427, "fleece", "dashed"),
        _make_line(100, 424, 197, 424, "fleece", "dashed"),
    ]
    geo["dimensions"] = [
        _make_dim(180, 430 - ext, 180, 430, f'{ext/PPI:.0f}" MIN'),
        _make_dim(200 - ext, 460, 200, 460, f'{ext/PPI:.0f}" MIN'),
    ]
    geo["notes"] = ["3-STEP REINFORCEMENT + RELIEF CUTS at outside wrap"]
    geo["layer_stack"] = ["primer", "pmma_resin", "fleece", "seal_coat"]
    return geo


def generate_crack_control_joint(cal):
    g = cal.get("geometry", {})
    rw = (g.get("reinforcement_width") or 6) * PPI
    geo = _base_geometry("crack_control_joint", "Crack / Control Joint", "LF-CJ-01")
    cx = 350
    geo["elements"] = [
        _make_rect(100, 400, 230, 100, "substrate"),
        _make_rect(360, 400, 230, 100, "substrate"),
        _make_rect(330, 400, 30, 100, "context"),
        _make_circle(345, 420, 5, "context"),
        _make_rect(cx - rw/2, 390, rw, 8, "membrane"),
        _make_rect(cx - rw/2 + 15, 392, rw - 30, 4, "fleece"),
    ]
    geo["dimensions"] = [_make_dim(cx - rw/2, 375, cx + rw/2, 375, f'{g.get("reinforcement_width") or 6}" TOTAL')]
    geo["callouts"] = [
        _make_callout(1, "Substrate", 200, 450),
        _make_callout(2, "Backer Rod", 345, 420),
        _make_callout(3, "PMMA Membrane", cx, 394),
        _make_callout(4, "Fleece Strip", cx, 394),
    ]
    geo["layer_stack"] = ["substrate", "backer_rod", "primer", "pmma_resin", "fleece", "seal_coat"]
    return geo


def generate_tile_overburden(cal):
    g = cal.get("geometry", {})
    geo = _base_geometry("tile_overburden_assembly", "Tile / Overburden Assembly", "LF-TO-01")
    by = 500
    geo["elements"] = [
        _make_rect(100, by, 500, (g.get("slab_thickness") or 6) * PPI, "substrate", "Structural Slab"),
        _make_rect(100, by - 10, 500, 10, "membrane", "PMMA System"),
        _make_rect(100, by - 25, 500, 15, "context", "Protection Board"),
        _make_rect(100, by - 55, 500, 30, "insulation", "Drainage / Insulation"),
        _make_rect(100, by - 75, 500, 20, "context", "Mortar Bed"),
        _make_rect(100, by - 95, 500, 20, "context", "Tile / Pavers"),
    ]
    geo["notes"] = ["HYPPOCOAT 250 for parking deck variant", "SLOPE TO DRAIN: 1/4 IN. PER FT MIN"]
    geo["layer_stack"] = ["substrate", "primer", "pmma_resin", "fleece", "seal_coat", "protection_board", "drainage", "mortar_bed", "tile"]
    return geo


def generate_expansion_joint(cal):
    g = cal.get("geometry", {})
    mem_side = (g.get("membrane_each_side") or 6) * PPI
    geo = _base_geometry("expansion_joint", "Expansion Joint", "LF-EJ-01")
    cx = 350
    geo["elements"] = [
        _make_rect(100, 400, 220, 100, "substrate"),
        _make_rect(380, 400, 220, 100, "substrate"),
        _make_rect(320, 400, 60, 100, "context"),
        _make_rect(cx - mem_side, 390, mem_side - 30, 6, "membrane"),
        _make_rect(cx + 30, 390, mem_side - 30, 6, "membrane"),
        _make_path([(cx - 30, 392), (cx - 15, 395), (cx, 398), (cx + 15, 395), (cx + 30, 392)], "fleece", "dashed"),
        _make_rect(cx - 40, 378, 80, 12, "metal", "Bellows / Cover Plate"),
    ]
    geo["dimensions"] = [
        _make_dim(cx - mem_side, 370, cx - 30, 370, f'{g.get("membrane_each_side") or 6}" MIN'),
        _make_dim(cx + 30, 370, cx + mem_side, 370, f'{g.get("membrane_each_side") or 6}" MIN'),
    ]
    geo["notes"] = ["CRITICAL: FLEECE LOOSE-LAID — DO NOT BRIDGE JOINT"]
    geo["layer_stack"] = ["substrate", "insulation", "filler", "primer", "pmma_resin", "fleece_loose_laid", "seal_coat", "bellows"]
    return geo


# === DISPATCHER ===

GENERATORS = {
    "parapet_wall_termination": generate_parapet,
    "edge_drip_termination": generate_edge,
    "primary_roof_drain": generate_primary_drain,
    "pipe_penetration": generate_pipe_penetration,
    "equipment_curb": generate_equipment_curb,
    "inside_corner_reinforcement": generate_inside_corner,
    "outside_corner_reinforcement": generate_outside_corner,
    "crack_control_joint": generate_crack_control_joint,
    "tile_overburden_assembly": generate_tile_overburden,
    "expansion_joint": generate_expansion_joint,
}


def generate_condition(condition_type, calibration_record):
    """Generate normalized geometry for a PMMA condition."""
    gen_fn = GENERATORS.get(condition_type)
    if not gen_fn:
        raise ValueError(f"Unknown condition: {condition_type}")
    return gen_fn(calibration_record)


def generate_all(calibration_path, output_dir):
    """Generate all 10 conditions from a calibration file."""
    cal_data = _load_json(calibration_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for cond in cal_data.get("conditions", []):
        ctype = cond["condition_type"]
        cid = cond["condition_id"]
        print(f"  Generating: {cid} ({ctype})")
        try:
            geo = generate_condition(ctype, cond)
            geo["condition_id"] = cid
            out_path = output_dir / f"{cid}_geometry.json"
            with open(out_path, "w") as f:
                json.dump(geo, f, indent=2)
            results.append({"id": cid, "status": "OK", "path": str(out_path)})
        except Exception as e:
            results.append({"id": cid, "status": "FAIL", "error": str(e)})

    return results


if __name__ == "__main__":
    import sys
    cal = sys.argv[1] if len(sys.argv) > 1 else "source/barrett/calibration/barrett_pmma_calibration_specimen_001.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "output/barrett_pmma_parametric_test/json"
    results = generate_all(cal, out)
    for r in results:
        print(f"  {r['id']}: {r['status']}")
