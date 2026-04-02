import os
import json
from pathlib import Path
import ezdxf

INPUT_DIR = Path("source/barrett/renamed_dxf")
OUTPUT_DIR = Path("source/barrett/json")

print("DXF parser starting...")
print("Working directory:", os.getcwd())
print("Input root:", INPUT_DIR.resolve())

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_entities(doc):
    msp = doc.modelspace()
    entities = []

    for e in msp:
        data = {
            "type": e.dxftype(),
            "layer": getattr(e.dxf, "layer", None),
            "handle": getattr(e.dxf, "handle", None),
            "linetype": getattr(e.dxf, "linetype", None),
            "color": getattr(e.dxf, "color", None),
        }

        try:
            if e.dxftype() == "LINE":
                data["start"] = list(e.dxf.start)
                data["end"] = list(e.dxf.end)

            elif e.dxftype() == "LWPOLYLINE":
                data["points"] = [list(p) for p in e.get_points()]

            elif e.dxftype() == "POLYLINE":
                data["points"] = [list(v.dxf.location) for v in e.vertices]

            elif e.dxftype() == "CIRCLE":
                data["center"] = list(e.dxf.center)
                data["radius"] = e.dxf.radius

            elif e.dxftype() == "ARC":
                data["center"] = list(e.dxf.center)
                data["radius"] = e.dxf.radius
                data["start_angle"] = e.dxf.start_angle
                data["end_angle"] = e.dxf.end_angle

            elif e.dxftype() == "TEXT":
                data["text"] = e.dxf.text
                data["position"] = list(e.dxf.insert)

            elif e.dxftype() == "MTEXT":
                data["text"] = e.text
                data["position"] = list(e.dxf.insert)

            elif e.dxftype() == "INSERT":
                data["block_name"] = e.dxf.name
                data["position"] = list(e.dxf.insert)
        except Exception as ex:
            data["entity_parse_error"] = str(ex)

        entities.append(data)

    return entities

dxf_files = sorted(INPUT_DIR.rglob("*.dxf"))
print(f"DXF files discovered: {len(dxf_files)}")

if not dxf_files:
    print("No DXF files found.")
    raise SystemExit(0)

for path in dxf_files:
    relative_path = path.relative_to(INPUT_DIR)
    out_path = OUTPUT_DIR / relative_path.with_suffix(".json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Processing {relative_path}")

    try:
        doc = ezdxf.readfile(path)
        entities = extract_entities(doc)

        output = {
            "source_file": str(path),
            "relative_source_file": str(relative_path),
            "output_file": str(out_path),
            "basename": path.stem,
            "parse_status": "success",
            "parse_errors": [],
            "total_entity_count": len(entities),
            "entities": entities,
        }

    except Exception as ex:
        output = {
            "source_file": str(path),
            "relative_source_file": str(relative_path),
            "output_file": str(out_path),
            "basename": path.stem,
            "parse_status": "failed",
            "parse_errors": [str(ex)],
            "total_entity_count": 0,
            "entities": [],
        }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

print("Done.")