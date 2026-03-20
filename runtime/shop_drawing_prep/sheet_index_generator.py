"""
Sheet Index Generator — Wave 14 Subsystem 7.

Generates a sheet index for shop drawing packages.
No direct rendering — output is deterministic manifest data only.
"""

import hashlib
import json
from typing import Any

CONTRACT_VERSION = "14.7.0"


class SheetIndexError(Exception):
    """Raised when sheet index generation fails."""


def generate_sheet_index(
    resolved_details: list[dict[str, Any]],
    project_id: str = "project",
) -> dict[str, Any]:
    """
    Generate a sheet index from resolved detail items.
    Each resolved detail gets a sheet assignment.
    Deterministic ordering guaranteed.
    """
    sheets: list[dict[str, Any]] = []
    sheet_number = 1

    for item in sorted(resolved_details, key=lambda x: x.get("canonical_detail_id", "") or ""):
        detail_id = item.get("canonical_detail_id")
        status = item.get("resolution_status", "")

        if status != "RESOLVED" or not detail_id:
            continue

        sheets.append({
            "sheet_number": sheet_number,
            "sheet_id": f"SD-{project_id}-{sheet_number:03d}",
            "canonical_detail_id": detail_id,
            "condition_ref": item.get("condition_ref", ""),
            "title": f"Detail {sheet_number}: {detail_id}",
        })
        sheet_number += 1

    index = {
        "project_id": project_id,
        "contract_version": CONTRACT_VERSION,
        "total_sheets": len(sheets),
        "sheets": sheets,
    }

    content = json.dumps(sheets, sort_keys=True, separators=(",", ":"))
    index["checksum"] = hashlib.sha256(content.encode("utf-8")).hexdigest()

    return index
