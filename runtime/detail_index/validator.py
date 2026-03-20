"""
Detail Index Validator — Wave 15.

Validates a built detail index artifact for integrity.
Fail closed on any violation.
"""

import hashlib
import json
from typing import Any

from runtime.detail_index.contract import REQUIRED_DETAIL_FIELDS, VALID_CLASSES, VALID_SYSTEMS


class DetailIndexValidationError(Exception):
    """Raised when index validation fails."""


def validate_detail_index(
    index_artifact: dict[str, Any],
    kernel_detail_ids: set[str] | None = None,
) -> dict[str, Any]:
    """
    Validate a detail index artifact.

    Args:
        index_artifact: The built detail index.
        kernel_detail_ids: Optional set of known kernel detail IDs for cross-ref validation.

    Returns:
        Validation report dict.

    Raises:
        DetailIndexValidationError on critical failures.
    """
    checks: list[dict[str, Any]] = []

    # Check 1: Required top-level keys
    required_keys = {"version", "wave", "detail_count", "detail_lookup",
                     "family_index", "tag_index", "condition_index",
                     "system_index", "class_index", "checksum"}
    missing = required_keys - set(index_artifact.keys())
    checks.append({
        "check": "structure_completeness",
        "passed": len(missing) == 0,
        "detail": f"Missing keys: {sorted(missing)}" if missing else "All required keys present.",
    })
    if missing:
        raise DetailIndexValidationError(f"Index missing required keys: {sorted(missing)}")

    detail_lookup = index_artifact["detail_lookup"]

    # Check 2: No empty index
    checks.append({
        "check": "non_empty",
        "passed": len(detail_lookup) > 0,
        "detail": f"{len(detail_lookup)} details indexed.",
    })
    if len(detail_lookup) == 0:
        raise DetailIndexValidationError("Index is empty — no details indexed.")

    # Check 3: Detail count matches
    count_match = len(detail_lookup) == index_artifact["detail_count"]
    checks.append({
        "check": "count_consistency",
        "passed": count_match,
        "detail": "Detail count matches." if count_match else "Count mismatch.",
    })

    # Check 4: All details have required fields
    field_violations = []
    for detail_id, record in detail_lookup.items():
        missing_fields = REQUIRED_DETAIL_FIELDS - set(record.keys())
        if missing_fields:
            field_violations.append((detail_id, sorted(missing_fields)))
    checks.append({
        "check": "field_completeness",
        "passed": len(field_violations) == 0,
        "detail": f"Violations: {field_violations}" if field_violations else "All fields present.",
    })

    # Check 5: No orphan references in secondary indexes
    indexed_ids = set(detail_lookup.keys())
    orphan_refs = []
    for index_name in ("family_index", "tag_index", "condition_index", "system_index", "class_index"):
        idx = index_artifact.get(index_name, {})
        for key, ids in idx.items():
            for did in ids:
                if did not in indexed_ids:
                    orphan_refs.append((index_name, key, did))
    checks.append({
        "check": "no_orphan_references",
        "passed": len(orphan_refs) == 0,
        "detail": f"Orphans: {orphan_refs}" if orphan_refs else "No orphan references.",
    })

    # Check 6: Kernel cross-reference
    if kernel_detail_ids is not None:
        unknown_ids = indexed_ids - kernel_detail_ids
        checks.append({
            "check": "kernel_cross_reference",
            "passed": len(unknown_ids) == 0,
            "detail": f"Unknown IDs not in kernel: {sorted(unknown_ids)}" if unknown_ids else "All IDs map to kernel details.",
        })

    # Check 7: Checksum integrity
    content = json.dumps(
        {
            "detail_lookup": index_artifact["detail_lookup"],
            "family_index": index_artifact["family_index"],
            "tag_index": index_artifact["tag_index"],
            "condition_index": index_artifact["condition_index"],
            "system_index": index_artifact["system_index"],
            "class_index": index_artifact["class_index"],
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    computed = hashlib.sha256(content.encode("utf-8")).hexdigest()
    stored = index_artifact.get("checksum", "")
    checks.append({
        "check": "checksum_integrity",
        "passed": computed == stored,
        "detail": "Checksum verified." if computed == stored else f"Mismatch: computed={computed[:16]}..., stored={stored[:16]}...",
    })

    # Check 8: Deterministic ordering
    keys_sorted = list(detail_lookup.keys()) == sorted(detail_lookup.keys())
    checks.append({
        "check": "deterministic_ordering",
        "passed": keys_sorted,
        "detail": "Keys in sorted order." if keys_sorted else "Keys not sorted.",
    })

    all_passed = all(c["passed"] for c in checks)
    if not all_passed:
        failed = [c for c in checks if not c["passed"]]
        raise DetailIndexValidationError(
            f"Validation failed: {[c['check'] for c in failed]}"
        )

    return {
        "subsystem": "detail_index",
        "wave": "15",
        "status": "PASS" if all_passed else "FAIL",
        "checks": checks,
        "summary": {
            "total_checks": len(checks),
            "passed": sum(1 for c in checks if c["passed"]),
            "failed": sum(1 for c in checks if not c["passed"]),
        },
    }
