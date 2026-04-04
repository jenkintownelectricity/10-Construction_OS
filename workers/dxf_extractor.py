"""
DXF Extractor — Wave 1 Guaranteed Detail Engine
Extracts geometry entities from a DXF file using ezdxf.
Returns a dict matching extraction_result.schema.json.
"""

import uuid
from datetime import datetime, timezone

import ezdxf


# Entity types we care about in modelspace
SUPPORTED_ENTITY_TYPES = frozenset([
    "LINE", "LWPOLYLINE", "POLYLINE", "CIRCLE", "ARC",
    "TEXT", "MTEXT", "INSERT", "HATCH", "MULTILEADER",
])


def _extract_entity(e):
    """Extract a single DXF entity into a schema-conformant dict."""
    entity_type = e.dxftype()
    data = {
        "entity_id": str(e.dxf.handle) if hasattr(e.dxf, "handle") else str(uuid.uuid4()),
        "entity_type": entity_type,
        "layer": getattr(e.dxf, "layer", "0"),
    }

    try:
        if entity_type == "LINE":
            data["coordinates"] = {
                "start": list(e.dxf.start),
                "end": list(e.dxf.end),
            }

        elif entity_type == "LWPOLYLINE":
            data["coordinates"] = {
                "points": [list(p) for p in e.get_points()],
            }

        elif entity_type == "POLYLINE":
            data["coordinates"] = {
                "points": [list(v.dxf.location) for v in e.vertices],
            }

        elif entity_type == "CIRCLE":
            data["coordinates"] = {"center": list(e.dxf.center)}
            data["radius"] = float(e.dxf.radius)

        elif entity_type == "ARC":
            data["coordinates"] = {"center": list(e.dxf.center)}
            data["radius"] = float(e.dxf.radius)
            data["angle"] = float(e.dxf.start_angle)
            data["coordinates"]["start_angle"] = float(e.dxf.start_angle)
            data["coordinates"]["end_angle"] = float(e.dxf.end_angle)

        elif entity_type == "TEXT":
            data["text"] = str(e.dxf.text)
            data["coordinates"] = {"insert": list(e.dxf.insert)}

        elif entity_type == "MTEXT":
            data["text"] = str(e.text)
            data["coordinates"] = {"insert": list(e.dxf.insert)}

        elif entity_type == "INSERT":
            data["coordinates"] = {"insert": list(e.dxf.insert)}
            data["raw_ref"] = str(e.dxf.name)

        elif entity_type == "HATCH":
            # Hatch paths can be complex; capture layer and pattern name
            pattern = getattr(e, "pattern_name", None)
            if pattern:
                data["raw_ref"] = str(pattern)
            data["coordinates"] = {}

        elif entity_type == "MULTILEADER":
            data["coordinates"] = {}

    except Exception as ex:
        data["raw_ref"] = f"parse_error: {ex}"

    return data


def extract_dxf(file_path, ingest_job_id=None):
    """
    Parse a DXF file and return an extraction_result envelope.

    Parameters
    ----------
    file_path : str
        Absolute path to the .dxf file on disk.
    ingest_job_id : str or None
        UUID of the ingest_job row. If None, a random UUID is used.

    Returns
    -------
    dict  matching extraction_result.schema.json
    """
    extraction_id = str(uuid.uuid4())
    job_id = ingest_job_id or str(uuid.uuid4())
    now_utc = datetime.now(timezone.utc).isoformat()

    try:
        doc = ezdxf.readfile(str(file_path))
    except Exception as ex:
        return {
            "extraction_id": extraction_id,
            "ingest_job_id": job_id,
            "file_type": "dxf",
            "extraction_status": "halted",
            "entity_count": 0,
            "entities": [],
            "source_file": str(file_path),
            "halt_reason": f"ezdxf read failed: {ex}",
            "extracted_at_utc": now_utc,
        }

    msp = doc.modelspace()
    entities = []
    for e in msp:
        if e.dxftype() in SUPPORTED_ENTITY_TYPES:
            entities.append(_extract_entity(e))

    status = "extracted" if entities else "extracted"
    # Even zero entities is a valid extraction (empty drawing)

    return {
        "extraction_id": extraction_id,
        "ingest_job_id": job_id,
        "file_type": "dxf",
        "extraction_status": status,
        "entity_count": len(entities),
        "entities": entities,
        "source_file": str(file_path),
        "extracted_at_utc": now_utc,
    }
