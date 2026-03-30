"""Multi-layer validation coordinator for Construction Runtime v0.2.

Orchestrates structural, domain, and generation validation stages.
Returns unified structured validation results with canonical error codes.
"""

from typing import Any

from validators.structural_validator import validate_structural
from validators.domain_validator import validate_domain
from validators.generation_validator import validate_generation


def run_full_validation(
    parsed_data: dict[str, Any],
    input_type: str,
    instruction_set_dict: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run all validation stages in sequence.

    Stages:
        1. Structural validation
        2. Domain validation (only if structural passes)
        3. Generation validation (only if domain passes and instruction_set provided)

    Returns combined result with all warnings/errors from all stages.
    """
    all_warnings: list[str] = []
    all_errors: list[dict[str, str]] = []
    stages_run: list[str] = []
    failed_stage: str | None = None

    # Stage 1: Structural
    structural = validate_structural(parsed_data, input_type)
    stages_run.append("structural")
    all_warnings.extend(structural["warnings"])
    all_errors.extend(structural["errors"])

    if not structural["is_valid"]:
        failed_stage = "structural"
        return _build_result(False, failed_stage, stages_run, all_warnings, all_errors)

    # Stage 2: Domain
    domain = validate_domain(parsed_data, input_type)
    stages_run.append("domain")
    all_warnings.extend(domain["warnings"])
    all_errors.extend(domain["errors"])

    if not domain["is_valid"]:
        failed_stage = "domain"
        return _build_result(False, failed_stage, stages_run, all_warnings, all_errors)

    # Stage 3: Generation (optional, only when instruction set is available)
    if instruction_set_dict is not None:
        gen = validate_generation(instruction_set_dict)
        stages_run.append("generation")
        all_warnings.extend(gen["warnings"])
        all_errors.extend(gen["errors"])

        if not gen["is_valid"]:
            failed_stage = "generation"
            return _build_result(False, failed_stage, stages_run, all_warnings, all_errors)

    return _build_result(True, None, stages_run, all_warnings, all_errors)


def _build_result(
    is_valid: bool,
    failed_stage: str | None,
    stages_run: list[str],
    warnings: list[str],
    errors: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "is_valid": is_valid,
        "stage": failed_stage or stages_run[-1] if stages_run else "none",
        "stages_run": stages_run,
        "warnings": warnings,
        "errors": errors,
    }
