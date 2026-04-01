"""Runtime Resolution Validator.

Fail-closed validation for ConditionSignature inputs and ResolutionResult outputs.
All validation checks reference the authoritative schema constants defined in
runtime_resolution_types.py (which mirror the JSON schemas exactly).

Boundary rules:
- Validation only — no mutation, no execution
- Fail-closed: any invalid data returns errors, never passes silently
- No probabilistic logic
"""

from __future__ import annotations

import re
from typing import Any

from runtime_adapter.runtime_resolution_types import (
    CONDITION_TYPES,
    CONDITION_SIGNATURE_REQUIRED_FIELDS,
    INTERFACE_CONDITIONS,
    WIND_ZONES,
    MOISTURE_EXPOSURES,
    RESOLUTION_STATUSES,
    STAGE_STATUSES,
    RESOLUTION_STAGES_REQUIRED,
    RESOLUTION_RESULT_REQUIRED_FIELDS,
    RESOLUTION_RESULT_SCHEMA_VERSION,
    RuntimeAdapterError,
)

_SCHEMA_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def validate_condition_signature(condition: Any) -> list[RuntimeAdapterError]:
    """Validate a ConditionSignature dict against the authoritative schema.

    Returns a list of RuntimeAdapterError. Empty list means valid.
    Fail-closed: non-dict input returns an error immediately.
    """
    errors: list[RuntimeAdapterError] = []

    if not isinstance(condition, dict):
        return [RuntimeAdapterError(
            code="INVALID_INPUT_TYPE",
            message=f"ConditionSignature must be a dict, got {type(condition).__name__}",
            stage="input_validation",
        )]

    # Required fields
    for field_name in CONDITION_SIGNATURE_REQUIRED_FIELDS:
        if field_name not in condition:
            errors.append(RuntimeAdapterError(
                code="MISSING_REQUIRED_FIELD",
                message=f"Missing required field: '{field_name}'",
                stage="input_validation",
                details={"field": field_name},
            ))

    # condition_id must be non-empty string
    cid = condition.get("condition_id")
    if cid is not None and (not isinstance(cid, str) or len(cid) == 0):
        errors.append(RuntimeAdapterError(
            code="INVALID_FIELD_VALUE",
            message="condition_id must be a non-empty string",
            stage="input_validation",
            details={"field": "condition_id"},
        ))

    # schema_version must match pattern
    sv = condition.get("schema_version")
    if sv is not None:
        if not isinstance(sv, str) or not _SCHEMA_VERSION_PATTERN.match(sv):
            errors.append(RuntimeAdapterError(
                code="INVALID_FIELD_VALUE",
                message="schema_version must match pattern '^\\d+\\.\\d+\\.\\d+$'",
                stage="input_validation",
                details={"field": "schema_version", "value": sv},
            ))

    # condition_type must be in authoritative enum
    ct = condition.get("condition_type")
    if ct is not None and ct not in CONDITION_TYPES:
        errors.append(RuntimeAdapterError(
            code="INVALID_ENUM_VALUE",
            message=f"condition_type '{ct}' not in {sorted(CONDITION_TYPES)}",
            stage="input_validation",
            details={"field": "condition_type", "value": ct},
        ))

    # location_context validation
    loc = condition.get("location_context")
    if loc is not None:
        if not isinstance(loc, dict):
            errors.append(RuntimeAdapterError(
                code="INVALID_FIELD_VALUE",
                message="location_context must be a dict",
                stage="input_validation",
                details={"field": "location_context"},
            ))
        else:
            # zone_id is required within location_context
            zone_id = loc.get("zone_id")
            if zone_id is None or not isinstance(zone_id, str) or len(zone_id) == 0:
                errors.append(RuntimeAdapterError(
                    code="MISSING_REQUIRED_FIELD",
                    message="location_context.zone_id is required and must be non-empty",
                    stage="input_validation",
                    details={"field": "location_context.zone_id"},
                ))

            # interface_condition enum check
            ic = loc.get("interface_condition")
            if ic is not None and ic not in INTERFACE_CONDITIONS:
                errors.append(RuntimeAdapterError(
                    code="INVALID_ENUM_VALUE",
                    message=f"interface_condition '{ic}' not in {sorted(INTERFACE_CONDITIONS)}",
                    stage="input_validation",
                    details={"field": "location_context.interface_condition", "value": ic},
                ))

    # climate_context validation
    cc = condition.get("climate_context")
    if cc is not None and isinstance(cc, dict):
        wz = cc.get("wind_zone")
        if wz is not None and wz not in WIND_ZONES:
            errors.append(RuntimeAdapterError(
                code="INVALID_ENUM_VALUE",
                message=f"wind_zone '{wz}' not in {sorted(WIND_ZONES)}",
                stage="input_validation",
                details={"field": "climate_context.wind_zone", "value": wz},
            ))
        me = cc.get("moisture_exposure")
        if me is not None and me not in MOISTURE_EXPOSURES:
            errors.append(RuntimeAdapterError(
                code="INVALID_ENUM_VALUE",
                message=f"moisture_exposure '{me}' not in {sorted(MOISTURE_EXPOSURES)}",
                stage="input_validation",
                details={"field": "climate_context.moisture_exposure", "value": me},
            ))

    return errors


def validate_resolution_result(result: Any) -> list[RuntimeAdapterError]:
    """Validate a ResolutionResult dict against the authoritative schema.

    Returns a list of RuntimeAdapterError. Empty list means valid.
    Fail-closed: non-dict input returns an error immediately.
    """
    errors: list[RuntimeAdapterError] = []

    if not isinstance(result, dict):
        return [RuntimeAdapterError(
            code="INVALID_OUTPUT_TYPE",
            message=f"ResolutionResult must be a dict, got {type(result).__name__}",
            stage="output_validation",
        )]

    # Required fields
    for field_name in RESOLUTION_RESULT_REQUIRED_FIELDS:
        if field_name not in result:
            errors.append(RuntimeAdapterError(
                code="MISSING_REQUIRED_FIELD",
                message=f"Missing required field: '{field_name}'",
                stage="output_validation",
                details={"field": field_name},
            ))

    # schema_version must be exactly "1.0.0" (const in schema)
    sv = result.get("schema_version")
    if sv is not None and sv != RESOLUTION_RESULT_SCHEMA_VERSION:
        errors.append(RuntimeAdapterError(
            code="SCHEMA_VERSION_MISMATCH",
            message=f"schema_version must be '{RESOLUTION_RESULT_SCHEMA_VERSION}', got '{sv}'",
            stage="output_validation",
            details={"field": "schema_version", "expected": RESOLUTION_RESULT_SCHEMA_VERSION, "actual": sv},
        ))

    # status must be in authoritative enum
    status = result.get("status")
    if status is not None and status not in RESOLUTION_STATUSES:
        errors.append(RuntimeAdapterError(
            code="INVALID_ENUM_VALUE",
            message=f"status '{status}' not in {sorted(RESOLUTION_STATUSES)}",
            stage="output_validation",
            details={"field": "status", "value": status},
        ))

    # resolution_stages must contain all required stage keys
    stages = result.get("resolution_stages")
    if stages is not None:
        if not isinstance(stages, dict):
            errors.append(RuntimeAdapterError(
                code="INVALID_FIELD_VALUE",
                message="resolution_stages must be a dict",
                stage="output_validation",
                details={"field": "resolution_stages"},
            ))
        else:
            for stage_name in RESOLUTION_STAGES_REQUIRED:
                if stage_name not in stages:
                    errors.append(RuntimeAdapterError(
                        code="MISSING_REQUIRED_FIELD",
                        message=f"Missing required stage: '{stage_name}'",
                        stage="output_validation",
                        details={"field": f"resolution_stages.{stage_name}"},
                    ))
                else:
                    stage_obj = stages[stage_name]
                    if isinstance(stage_obj, dict):
                        ss = stage_obj.get("status")
                        if ss is not None and ss not in STAGE_STATUSES:
                            errors.append(RuntimeAdapterError(
                                code="INVALID_ENUM_VALUE",
                                message=f"Stage '{stage_name}' status '{ss}' not in {sorted(STAGE_STATUSES)}",
                                stage="output_validation",
                                details={"field": f"resolution_stages.{stage_name}.status", "value": ss},
                            ))

    # source_repo must be "Construction_ALEXANDER_Engine" if present
    sr = result.get("source_repo")
    if sr is not None and sr != "Construction_ALEXANDER_Engine":
        errors.append(RuntimeAdapterError(
            code="INVALID_SOURCE_REPO",
            message=f"source_repo must be 'Construction_ALEXANDER_Engine', got '{sr}'",
            stage="output_validation",
            details={"field": "source_repo", "value": sr},
        ))

    return errors
