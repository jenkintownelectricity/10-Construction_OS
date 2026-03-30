"""
Variant Validator — Wave 14 Subsystem 3.

Validates variant payloads and manifests for schema compliance,
canonical ID preservation, and prohibited combination enforcement.
"""

from typing import Any

from runtime.detail_variants.variant_generator import (
    CANONICAL_DETAIL_FAMILIES,
    CONDITION_PARAMETERS,
    DETAIL_CONDITION_MAP,
    PARAMETER_DEFINITIONS,
    PROHIBITED_COMBINATIONS,
)


def validate_variant(variant: dict[str, Any]) -> list[str]:
    """Validate a single variant payload. Returns list of errors."""
    errors: list[str] = []

    for field in ("variant_id", "canonical_detail_id", "parameters", "provenance"):
        if field not in variant:
            errors.append(f"Missing required field: {field}")

    canonical_id = variant.get("canonical_detail_id", "")
    if canonical_id and canonical_id not in CANONICAL_DETAIL_FAMILIES:
        errors.append(f"canonical_detail_id '{canonical_id}' not in frozen kernel families.")

    variant_id = variant.get("variant_id", "")
    if variant_id and canonical_id:
        if not variant_id.startswith(canonical_id):
            errors.append(
                f"variant_id '{variant_id}' does not derive from "
                f"canonical_detail_id '{canonical_id}'."
            )

    # Validate parameters
    parameters = variant.get("parameters", {})
    condition = DETAIL_CONDITION_MAP.get(canonical_id, "")
    allowed = set(CONDITION_PARAMETERS.get(condition, []))

    for param_name, value in parameters.items():
        if param_name not in PARAMETER_DEFINITIONS:
            errors.append(f"Unknown parameter '{param_name}'.")
            continue
        if param_name not in allowed:
            errors.append(f"Parameter '{param_name}' not applicable to condition '{condition}'.")
        pdef = PARAMETER_DEFINITIONS[param_name]
        if not isinstance(value, (int, float)):
            errors.append(f"Parameter '{param_name}' must be numeric.")
        elif value < pdef["min"] or value > pdef["max"]:
            errors.append(
                f"Parameter '{param_name}' value {value} outside range [{pdef['min']}, {pdef['max']}]."
            )

    # Check prohibited combinations
    for prohibition in PROHIBITED_COMBINATIONS:
        if prohibition["condition"] == condition and prohibition["rule"](parameters):
            errors.append(f"Prohibited combination: {prohibition['description']}")

    # Validate provenance
    provenance = variant.get("provenance", {})
    if provenance.get("canonical_detail_id") != canonical_id:
        errors.append("Provenance canonical_detail_id does not match variant canonical_detail_id.")
    if provenance.get("generation_source") != "variant_generator":
        errors.append("Provenance generation_source must be 'variant_generator'.")

    return errors


def validate_variant_manifest(manifest: dict[str, Any]) -> list[str]:
    """Validate a variant manifest. Returns list of errors."""
    errors: list[str] = []

    for field in ("manifest_id", "contract_version", "variants", "checksum"):
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    variants = manifest.get("variants", [])
    if not isinstance(variants, list):
        errors.append("'variants' must be an array.")
        return errors

    seen_ids: set[str] = set()
    for i, variant in enumerate(variants):
        vid = variant.get("variant_id", "")
        if vid in seen_ids:
            errors.append(f"Duplicate variant_id: {vid}")
        seen_ids.add(vid)

        v_errors = validate_variant(variant)
        for err in v_errors:
            errors.append(f"Variant {i} ({vid}): {err}")

    # Deterministic ordering
    ids = [v.get("variant_id", "") for v in variants]
    if ids != sorted(ids):
        errors.append("Variants are not in deterministic sorted order.")

    return errors
