"""
Detail Resolution Validator — Wave 14 Subsystem 2.

Validates a resolved detail manifest for correctness and contract compliance.
"""

from typing import Any

from runtime.detail_resolver.detail_selector import CANONICAL_DETAIL_FAMILIES

VALID_STATUSES = frozenset(["RESOLVED", "UNRESOLVED", "UNKNOWN", "UNSUPPORTED"])


def validate_resolution_manifest(manifest: dict[str, Any]) -> list[str]:
    """
    Validate a resolved detail manifest.
    Returns list of validation errors. Empty list means valid.
    """
    errors: list[str] = []

    for field in ("manifest_id", "source_graph_id", "contract_version", "resolved_items", "checksum"):
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    items = manifest.get("resolved_items", [])
    if not isinstance(items, list):
        errors.append("'resolved_items' must be an array.")
        return errors

    seen_refs: set[str] = set()
    for i, item in enumerate(items):
        ref = item.get("condition_ref", "")
        if not ref:
            errors.append(f"Item {i}: missing 'condition_ref'.")
        if ref in seen_refs:
            errors.append(f"Item {i}: duplicate condition_ref '{ref}'.")
        seen_refs.add(ref)

        status = item.get("resolution_status", "")
        if status not in VALID_STATUSES:
            errors.append(f"Item {i} ({ref}): invalid resolution_status '{status}'.")

        detail_id = item.get("canonical_detail_id")
        if status == "RESOLVED":
            if not detail_id:
                errors.append(f"Item {i} ({ref}): RESOLVED but no canonical_detail_id.")
            elif detail_id not in CANONICAL_DETAIL_FAMILIES:
                errors.append(
                    f"Item {i} ({ref}): canonical_detail_id '{detail_id}' "
                    f"not found in frozen kernel families."
                )
        elif status in ("UNRESOLVED", "UNKNOWN", "UNSUPPORTED"):
            if detail_id is not None:
                errors.append(
                    f"Item {i} ({ref}): status is '{status}' but "
                    f"canonical_detail_id is set to '{detail_id}'. Must be null."
                )

        if not item.get("resolution_reason"):
            errors.append(f"Item {i} ({ref}): missing resolution_reason.")

    # Deterministic ordering check
    refs = [item.get("condition_ref", "") for item in items]
    if refs != sorted(refs):
        errors.append("Resolved items are not in deterministic sorted order by condition_ref.")

    return errors
