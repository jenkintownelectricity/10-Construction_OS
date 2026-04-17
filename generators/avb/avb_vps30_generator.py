#!/usr/bin/env python3
"""
avb_vps30_generator.py — GCP Perm-A-Barrier VPS30 AVB Parametric Generator

Generates normalized geometry payloads for 18 AVB conditions.
"""
import json, sys
from pathlib import Path

PPI = 30

def _g(condition_type, title, code):
    return {"condition_type":condition_type,"title":f"GCP VPS30 — {title}","output_code":code,
            "system":"Perm-A-Barrier VPS30","family_id":"FAM-GCP-AVB","manufacturer":"GCP Applied Technologies",
            "project":"Beaver Stadium West Side Renovation",
            "elements":[],"dimensions":[],"callouts":[],"notes":[],"layer_stack":[]}

def _r(x,y,w,h,layer="substrate",label=None):
    return {"type":"rect","x":x,"y":y,"w":w,"h":h,"layer":layer,"label":label}
def _l(x1,y1,x2,y2,layer="membrane",style="solid"):
    return {"type":"line","x1":x1,"y1":y1,"x2":x2,"y2":y2,"layer":layer,"style":style}
def _p(pts,layer="membrane",style="solid",closed=False):
    return {"type":"path","points":pts,"layer":layer,"style":style,"closed":closed}
def _d(x1,y1,x2,y2,text,side="right"):
    return {"type":"dimension","x1":x1,"y1":y1,"x2":x2,"y2":y2,"text":text,"side":side}
def _c(n,label,cx,cy):
    return {"number":n,"label":label,"cx":cx,"cy":cy}

def gen_wall_field(cal):
    g=_g("wall_field","Wall Field Application","AVB-WF-01")
    g["elements"]=[
        _r(100,200,60,400,"substrate","Steel Stud Wall"),
        _r(160,200,30,400,"insulation","Sheathing"),
        _r(190,200,8,400,"membrane","VPS30 Membrane"),
        _r(198,200,60,400,"context","Cladding Cavity"),
        _r(258,200,40,400,"context","Cladding"),
    ]
    g["dimensions"]=[_d(300,200,300,600,"FULL HEIGHT")]
    g["callouts"]=[_c(1,"Steel Studs",130,400),_c(2,"Sheathing",175,400),_c(3,"VPS30 AVB",194,400),_c(4,"Cavity",228,400),_c(5,"Cladding",278,400)]
    g["layer_stack"]=["steel_stud","sheathing","vps30_avb","cavity","cladding"]
    g["notes"]=["Self-adhered vapor permeable air barrier","Lap joints min 2 in. shingle fashion"]
    return g

def gen_window_head(cal):
    g=_g("window_head","Window Head","AVB-WH-01")
    g["elements"]=[
        _r(100,300,200,40,"substrate","Header/Lintel"),
        _r(100,250,200,50,"substrate","Sheathing Above"),
        _r(100,340,200,60,"context","Window Frame"),
        _r(95,250,10,150,"membrane","VPS30 Turn-in"),
        _l(105,250,105,300,"membrane"),_l(105,300,300,300,"membrane"),
        _r(100,295,200,10,"fleece","Head Flashing"),
    ]
    g["dimensions"]=[_d(310,295,310,340,"4 IN. MIN LAP")]
    g["callouts"]=[_c(1,"Header",200,320),_c(2,"Sheathing",200,275),_c(3,"Window Frame",200,370),_c(4,"VPS30 Turn-in",92,320),_c(5,"Head Flashing",200,300)]
    g["layer_stack"]=["sheathing","vps30_field","head_flashing","window_frame"]
    return g

def gen_window_sill(cal):
    g=_g("window_sill","Window Sill","AVB-WS-01")
    g["elements"]=[
        _r(100,300,200,40,"context","Window Frame"),
        _r(100,340,200,60,"substrate","Sheathing Below"),
        _r(95,300,10,100,"membrane","VPS30 Turn-out"),
        _l(105,340,300,340,"membrane"),_l(105,340,105,400,"membrane"),
        _r(100,335,200,10,"fleece","Sill Pan Flashing"),
        _r(100,345,200,8,"membrane","VPS30 Lap Over Pan"),
    ]
    g["dimensions"]=[_d(310,300,310,340,"SILL PAN")]
    g["callouts"]=[_c(1,"Window Frame",200,320),_c(2,"Sill Pan",200,340),_c(3,"VPS30 Overlap",200,349),_c(4,"Sheathing",200,370)]
    g["notes"]=["Sill pan must slope to exterior","End dams required at jambs"]
    g["layer_stack"]=["sheathing","sill_pan","vps30_overlap","window_frame"]
    return g

def gen_window_jamb(cal):
    g=_g("window_jamb","Window Jamb","AVB-WJ-01")
    g["elements"]=[
        _r(100,200,30,300,"substrate","Sheathing"),
        _r(130,200,10,300,"membrane","VPS30 Field"),
        _r(140,250,60,200,"context","Window Frame"),
        _r(135,250,10,200,"membrane","VPS30 Turn-in"),
    ]
    g["callouts"]=[_c(1,"Sheathing",115,350),_c(2,"VPS30 Field",135,350),_c(3,"Window Frame",170,350),_c(4,"VPS30 Jamb Return",137,350)]
    g["layer_stack"]=["sheathing","vps30_field","jamb_return","window_frame"]
    return g

def gen_door_head(cal):
    g=_g("door_head","Door Head","AVB-DH-01")
    g["elements"]=[_r(100,300,200,40,"substrate","Header"),_r(100,250,200,50,"substrate","Sheathing"),
        _r(100,340,200,80,"context","Door Frame"),_r(100,295,200,10,"fleece","Head Flashing"),
        _l(105,250,105,300,"membrane"),_l(105,300,300,300,"membrane")]
    g["callouts"]=[_c(1,"Header",200,320),_c(2,"Head Flashing",200,300),_c(3,"Door Frame",200,380)]
    g["layer_stack"]=["sheathing","vps30_field","head_flashing","door_frame"]
    return g

def gen_door_jamb(cal):
    g=_g("door_jamb","Door Jamb","AVB-DJ-01")
    g["elements"]=[_r(100,200,30,300,"substrate","Sheathing"),_r(130,200,10,300,"membrane","VPS30 Field"),
        _r(140,250,60,250,"context","Door Frame"),_r(135,250,10,250,"membrane","VPS30 Return")]
    g["callouts"]=[_c(1,"Sheathing",115,350),_c(2,"VPS30",135,350),_c(3,"Door Frame",170,375)]
    g["layer_stack"]=["sheathing","vps30_field","return","door_frame"]
    return g

def gen_door_threshold(cal):
    g=_g("door_threshold","Door Threshold","AVB-DT-01")
    g["elements"]=[_r(100,350,300,50,"substrate","Slab/Foundation"),_r(100,300,300,50,"context","Wall Assembly"),
        _r(200,340,100,10,"membrane","Threshold Flashing"),_r(200,310,100,30,"context","Door Sill")]
    g["callouts"]=[_c(1,"Slab",250,375),_c(2,"Threshold Flash",250,345),_c(3,"Door Sill",250,325)]
    g["notes"]=["Threshold flashing must slope to exterior"]
    g["layer_stack"]=["slab","threshold_flashing","door_sill"]
    return g

def gen_pipe_pen(cal):
    g=_g("pipe_penetration","Pipe Penetration","AVB-PP-01")
    g["elements"]=[_r(100,200,300,200,"substrate","Sheathing"),_r(100,195,300,8,"membrane","VPS30 Field"),
        _r(230,250,40,100,"metal","Pipe Sleeve"),_r(220,195,60,8,"membrane","VPS30 Collar")]
    g["dimensions"]=[_d(285,195,285,250,"4 IN. MIN")]
    g["callouts"]=[_c(1,"Sheathing",200,300),_c(2,"VPS30",200,199),_c(3,"Pipe",250,300),_c(4,"VPS30 Collar",250,199)]
    g["notes"]=["VPS30 collar min 4 in. from penetration edge","Seal with compatible sealant at pipe interface"]
    g["layer_stack"]=["sheathing","vps30_field","pipe_sleeve","vps30_collar","sealant"]
    return g

def gen_duct_pen(cal):
    g=_g("duct_penetration","Duct Penetration","AVB-DP-01")
    g["elements"]=[_r(100,200,300,200,"substrate","Sheathing"),_r(100,195,300,8,"membrane","VPS30 Field"),
        _r(200,250,100,80,"metal","Duct Sleeve"),_r(190,195,120,8,"membrane","VPS30 Collar")]
    g["callouts"]=[_c(1,"Sheathing",150,300),_c(2,"VPS30",150,199),_c(3,"Duct",250,290),_c(4,"VPS30 Collar",250,199)]
    g["layer_stack"]=["sheathing","vps30_field","duct_sleeve","vps30_collar"]
    return g

def gen_beam_pen(cal):
    g=_g("beam_penetration","Beam Penetration","AVB-BP-01")
    g["elements"]=[_r(100,200,300,200,"substrate","Sheathing"),_r(100,195,300,8,"membrane","VPS30 Field"),
        _r(200,220,100,60,"substrate","Steel Beam"),_r(190,195,120,8,"membrane","VPS30 Wrap")]
    g["callouts"]=[_c(1,"Sheathing",150,300),_c(2,"VPS30",150,199),_c(3,"Beam",250,250),_c(4,"VPS30 Wrap",250,199)]
    g["notes"]=["VPS30 must wrap beam penetration continuously","Seal at steel interface with compatible sealant"]
    g["layer_stack"]=["sheathing","vps30_field","beam","vps30_wrap","sealant"]
    return g

def gen_roof_trans(cal):
    g=_g("roof_transition","Roof-to-Wall Transition","AVB-RT-01")
    g["elements"]=[_r(100,300,200,60,"substrate","Wall Sheathing"),_r(100,360,300,30,"substrate","Roof Deck"),
        _r(95,300,10,90,"membrane","VPS30 Wall"),_l(100,355,400,355,"membrane"),
        _r(100,350,300,10,"fleece","Transition Flashing")]
    g["callouts"]=[_c(1,"Wall Sheathing",200,330),_c(2,"Roof Deck",250,375),_c(3,"VPS30 Wall",92,345),_c(4,"Transition Flash",250,355)]
    g["notes"]=["AVB must be continuous through roof-wall transition"]
    g["layer_stack"]=["wall_sheathing","vps30_wall","transition_flashing","roof_deck"]
    return g

def gen_foundation_trans(cal):
    g=_g("foundation_transition","Foundation-to-Wall Transition","AVB-FT-01")
    g["elements"]=[_r(100,200,60,200,"substrate","Wall Sheathing"),_r(80,400,100,100,"substrate","Foundation"),
        _r(160,200,8,200,"membrane","VPS30 Wall Field"),_r(155,390,15,20,"membrane","VPS30 Lap to Foundation")]
    g["dimensions"]=[_d(180,390,180,410,"4 IN. MIN LAP")]
    g["callouts"]=[_c(1,"Sheathing",130,300),_c(2,"Foundation",130,450),_c(3,"VPS30 Field",164,300),_c(4,"VPS30 Lap",162,400)]
    g["layer_stack"]=["foundation","sheathing","vps30_field","foundation_lap"]
    return g

def gen_control_joint(cal):
    g=_g("control_joint","Control Joint","AVB-CJ-01")
    g["elements"]=[_r(100,200,120,300,"substrate","Sheathing Left"),_r(230,200,120,300,"substrate","Sheathing Right"),
        _r(220,200,10,300,"context","Joint"),_r(100,195,250,8,"membrane","VPS30 Continuous"),
        _r(180,195,90,8,"fleece","Reinforcement Strip")]
    g["dimensions"]=[_d(180,180,270,180,"6 IN. MIN")]
    g["callouts"]=[_c(1,"Sheathing",160,350),_c(2,"Joint",225,350),_c(3,"VPS30",225,199),_c(4,"Reinforcement",225,199)]
    g["notes"]=["VPS30 must bridge control joint continuously","Reinforcement strip centered on joint"]
    g["layer_stack"]=["sheathing","joint","vps30_continuous","reinforcement"]
    return g

def gen_expansion_joint(cal):
    g=_g("expansion_joint","Expansion Joint","AVB-EJ-01")
    g["elements"]=[_r(100,200,110,300,"substrate","Sheathing Left"),_r(240,200,110,300,"substrate","Sheathing Right"),
        _r(210,200,30,300,"context","Expansion Gap"),_r(100,195,110,8,"membrane","VPS30 Left"),
        _r(240,195,110,8,"membrane","VPS30 Right"),
        _p([[210,197],[225,202],[240,197]],"fleece","dashed")]
    g["callouts"]=[_c(1,"Sheathing",155,350),_c(2,"Gap",225,350),_c(3,"VPS30 Each Side",170,199)]
    g["notes"]=["VPS30 terminates each side of expansion joint","Flexible transition detail required at gap"]
    g["layer_stack"]=["sheathing","expansion_gap","vps30_each_side","flexible_transition"]
    return g

def gen_term_top(cal):
    g=_g("termination_top","Top Termination","AVB-TT-01")
    g["elements"]=[_r(100,200,60,300,"substrate","Wall Sheathing"),_r(160,200,8,300,"membrane","VPS30"),
        _r(155,195,20,10,"metal","Termination Bar"),_r(100,180,80,20,"context","Parapet/Roof")]
    g["callouts"]=[_c(1,"Sheathing",130,350),_c(2,"VPS30",164,350),_c(3,"Term Bar",165,200)]
    g["notes"]=["Mechanically fasten termination bar","Seal top edge with sealant"]
    g["layer_stack"]=["sheathing","vps30","termination_bar","sealant"]
    return g

def gen_term_bottom(cal):
    g=_g("termination_bottom","Bottom Termination","AVB-TB-01")
    g["elements"]=[_r(100,200,60,300,"substrate","Wall Sheathing"),_r(160,200,8,300,"membrane","VPS30"),
        _r(155,495,20,10,"metal","Termination Bar"),_r(80,500,120,40,"substrate","Foundation")]
    g["callouts"]=[_c(1,"Sheathing",130,350),_c(2,"VPS30",164,350),_c(3,"Term Bar",165,500),_c(4,"Foundation",140,520)]
    g["layer_stack"]=["foundation","sheathing","vps30","termination_bar"]
    return g

def gen_inside_corner(cal):
    g=_g("inside_corner","Inside Corner","AVB-IC-01")
    g["elements"]=[_r(200,200,20,250,"substrate","Wall A"),_r(220,430,200,20,"substrate","Wall B"),
        _r(220,200,8,230,"membrane","VPS30 Wall A"),_r(220,425,200,8,"membrane","VPS30 Wall B"),
        _r(220,420,30,15,"fleece","Corner Patch")]
    g["dimensions"]=[_d(190,420,190,450,"4 IN. MIN")]
    g["callouts"]=[_c(1,"Wall A",210,320),_c(2,"Wall B",320,440),_c(3,"VPS30",224,320),_c(4,"Corner Patch",235,427)]
    g["notes"]=["Corner patch min 4 in. each direction","Install patch over field membrane"]
    g["layer_stack"]=["wall_a","wall_b","vps30_field","corner_patch"]
    return g

def gen_outside_corner(cal):
    g=_g("outside_corner","Outside Corner","AVB-OC-01")
    g["elements"]=[_r(200,200,20,250,"substrate","Wall A"),_r(100,430,120,20,"substrate","Wall B"),
        _r(197,200,8,230,"membrane","VPS30 Wall A"),_r(100,425,120,8,"membrane","VPS30 Wall B"),
        _r(190,420,20,15,"fleece","Corner Wrap")]
    g["dimensions"]=[_d(180,420,180,450,"4 IN. MIN")]
    g["callouts"]=[_c(1,"Wall A",210,320),_c(2,"Wall B",160,440),_c(3,"VPS30",201,320),_c(4,"Corner Wrap",200,427)]
    g["notes"]=["Wrap corner patch around outside corner","Min 4 in. each direction"]
    g["layer_stack"]=["wall_a","wall_b","vps30_field","corner_wrap"]
    return g

GENERATORS = {
    "wall_field": gen_wall_field, "window_head": gen_window_head, "window_sill": gen_window_sill,
    "window_jamb": gen_window_jamb, "door_head": gen_door_head, "door_jamb": gen_door_jamb,
    "door_threshold": gen_door_threshold, "pipe_penetration": gen_pipe_pen, "duct_penetration": gen_duct_pen,
    "beam_penetration": gen_beam_pen, "roof_transition": gen_roof_trans, "foundation_transition": gen_foundation_trans,
    "control_joint": gen_control_joint, "expansion_joint": gen_expansion_joint,
    "termination_top": gen_term_top, "termination_bottom": gen_term_bottom,
    "inside_corner": gen_inside_corner, "outside_corner": gen_outside_corner,
}

def generate_all(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for i, (ctype, gen_fn) in enumerate(GENERATORS.items(), 1):
        cid = f"gcp_vps30_{ctype}_001"
        print(f"  [{i:02d}/18] {cid}")
        try:
            geo = gen_fn({})
            geo["condition_id"] = cid
            out = output_dir / f"{cid}_geometry.json"
            with open(out, "w") as f:
                json.dump(geo, f, indent=2)
            results.append({"id": cid, "status": "OK"})
        except Exception as e:
            results.append({"id": cid, "status": "FAIL", "error": str(e)})
    return results

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/beaver_stadium_avb/json"
    results = generate_all(out)
    ok = sum(1 for r in results if r["status"] == "OK")
    print(f"\n{ok}/18 conditions generated")
