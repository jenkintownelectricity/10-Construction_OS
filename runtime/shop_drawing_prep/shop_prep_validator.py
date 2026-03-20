"""
Shop Prep Validator — Wave 14 Subsystem 7.

Validates shop drawing preparation manifests for contract compliance.
Ensures no unsupported detail enters package silently.
"""

from typing import Any

CANONICAL_DETAIL_FAMILIES = frozenset([
    "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
    "LOW_SLOPE-TERMINATION-VERTICAL_WALL-TERMINATION_BAR-TPO-01",
    "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01",
    "LOW_SLOPE-EDGE-ROOF_TO_EDGE-METAL_EDGE-TPO-01",
    "LOW_SLOPE-PENETRATION-PIPE-PIPE_BOOT-EPDM-01",
    "LOW_SLOPE-PENETRATION-CURB-COUNTERFLASHING-TPO-01",
    "LOW_SLOPE-DRAINAGE-DRAIN-COPING-TPO-01",
    "LOW_SLOPE-DRAINAGE-SCUPPER-METAL_EDGE-SBS-01",
    "LOW_SLOPE-JOINT-EXPANSION_JOINT-SELF_ADHERED-EPDM-01",
])


def validate_shop_drawing_manifest(manifest: dict[str, Any]) -> list[str]:
    """
    Validate a shop drawing manifest.
    Returns list of errors. Empty means valid.
    """
    errors: list[str] = []

    for field in ("manifest_id", "project_id", "contract_version", "drawing_entries", "checksum"):
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    entries = manifest.get("drawing_entries", [])
    if not isinstance(entries, list):
        errors.append("'drawing_entries' must be an array.")
        return errors

    seen_sheets: set[str] = set()
    for i, entry in enumerate(entries):
        sheet_id = entry.get("sheet_id", "")
        if sheet_id in seen_sheets:
            errors.append(f"Entry {i}: duplicate sheet_id '{sheet_id}'.")
        seen_sheets.add(sheet_id)

        detail_id = entry.get("canonical_detail_id", "")
        if not detail_id:
            errors.append(f"Entry {i}: missing canonical_detail_id.")
        elif detail_id not in CANONICAL_DETAIL_FAMILIES:
            errors.append(
                f"Entry {i}: unsupported detail '{detail_id}' — "
                f"cannot silently enter package."
            )

        if entry.get("render_type") == "variant" and not entry.get("variant_id"):
            errors.append(f"Entry {i}: render_type is 'variant' but no variant_id.")

    return errors


def validate_sheet_index(index: dict[str, Any]) -> list[str]:
    """Validate a sheet index for correctness."""
    errors: list[str] = []

    sheets = index.get("sheets", [])
    seen_numbers: set[int] = set()
    for i, sheet in enumerate(sheets):
        sn = sheet.get("sheet_number", 0)
        if sn in seen_numbers:
            errors.append(f"Sheet {i}: duplicate sheet_number {sn}.")
        seen_numbers.add(sn)

        detail_id = sheet.get("canonical_detail_id", "")
        if detail_id and detail_id not in CANONICAL_DETAIL_FAMILIES:
            errors.append(f"Sheet {i}: unsupported detail '{detail_id}'.")

    return errors
