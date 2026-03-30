"""
Detail Packager — Wave 14 Subsystem 7.

Packages resolved details and variants into drawing package entries.
No rendering — produces structured manifest data for downstream renderers.
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


class DetailPackagingError(Exception):
    """Raised when packaging fails."""


def package_detail(
    canonical_detail_id: str,
    variant_id: str | None = None,
    parameters: dict[str, Any] | None = None,
    condition_ref: str = "",
) -> dict[str, Any]:
    """
    Package a single detail for the drawing manifest.
    Validates that detail ID is canonical.
    """
    if canonical_detail_id not in CANONICAL_DETAIL_FAMILIES:
        raise DetailPackagingError(
            f"Cannot package unsupported detail '{canonical_detail_id}'. "
            f"Not in canonical families."
        )

    entry: dict[str, Any] = {
        "canonical_detail_id": canonical_detail_id,
        "condition_ref": condition_ref,
        "render_type": "canonical",
    }

    if variant_id:
        entry["variant_id"] = variant_id
        entry["render_type"] = "variant"
        if parameters:
            entry["parameters"] = parameters

    return entry


def package_details_batch(
    items: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Package a batch of detail items. Returns (packaged, rejected) tuples.
    Unsupported details are rejected — never silently included.
    """
    packaged: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for item in sorted(items, key=lambda x: x.get("canonical_detail_id", "") or ""):
        detail_id = item.get("canonical_detail_id")
        if not detail_id or detail_id not in CANONICAL_DETAIL_FAMILIES:
            rejected.append({
                "item": item,
                "reason": f"Detail ID '{detail_id}' not in canonical families.",
            })
            continue

        try:
            entry = package_detail(
                canonical_detail_id=detail_id,
                variant_id=item.get("variant_id"),
                parameters=item.get("parameters"),
                condition_ref=item.get("condition_ref", ""),
            )
            packaged.append(entry)
        except DetailPackagingError as e:
            rejected.append({"item": item, "reason": str(e)})

    return packaged, rejected
