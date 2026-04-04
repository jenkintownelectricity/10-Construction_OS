"""
File Dispatcher — Wave 1 Guaranteed Detail Engine
Routes ingest jobs to the correct extractor based on file extension.
Returns a dict matching extraction_result.schema.json.
"""

import os
import uuid
from datetime import datetime, timezone

from workers.dxf_extractor import extract_dxf


# Extensions normalised to lower-case without leading dot
_EVIDENCE_ONLY_EXTENSIONS = frozenset(["pdf", "png", "jpg", "jpeg"])
_FILE_TYPE_MAP = {
    "pdf": "pdf",
    "png": "png",
    "jpg": "jpg",
    "jpeg": "jpg",
}


def dispatch(file_path, ingest_job_id=None):
    """
    Route a file to the appropriate extractor.

    Parameters
    ----------
    file_path : str
        Local path to the downloaded file.
    ingest_job_id : str or None
        UUID of the ingest_job row.

    Returns
    -------
    dict  matching extraction_result.schema.json
    """
    job_id = ingest_job_id or str(uuid.uuid4())
    now_utc = datetime.now(timezone.utc).isoformat()
    ext = os.path.splitext(file_path)[1].lstrip(".").lower()

    # --- DXF: full extraction ---
    if ext == "dxf":
        return extract_dxf(file_path, ingest_job_id=job_id)

    # --- DWG: not yet supported ---
    if ext == "dwg":
        return {
            "extraction_id": str(uuid.uuid4()),
            "ingest_job_id": job_id,
            "file_type": "dwg",
            "extraction_status": "halted",
            "entity_count": 0,
            "entities": [],
            "source_file": str(file_path),
            "halt_reason": "DWG conversion not implemented",
            "extracted_at_utc": now_utc,
        }

    # --- PDF / image: evidence-only passthrough ---
    if ext in _EVIDENCE_ONLY_EXTENSIONS:
        file_type = _FILE_TYPE_MAP.get(ext, "unknown")
        return {
            "extraction_id": str(uuid.uuid4()),
            "ingest_job_id": job_id,
            "file_type": file_type,
            "extraction_status": "evidence_only",
            "entity_count": 0,
            "entities": [],
            "source_file": str(file_path),
            "extracted_at_utc": now_utc,
        }

    # --- Unknown extension: halt ---
    return {
        "extraction_id": str(uuid.uuid4()),
        "ingest_job_id": job_id,
        "file_type": "unknown",
        "extraction_status": "halted",
        "entity_count": 0,
        "entities": [],
        "source_file": str(file_path),
        "halt_reason": f"Unsupported file type: .{ext}" if ext else "Unsupported file type: (no extension)",
        "extracted_at_utc": now_utc,
    }
