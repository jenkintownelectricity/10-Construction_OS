"""Construction pipeline.

Orchestrates the full runtime flow from input ingestion to runtime report.
Provides callable paths for assembly and spec processing.
"""

from typing import Any

from runtime.parsers.assembly_parser import normalize_assembly_input, parse_assembly
from runtime.parsers.spec_parser import normalize_spec_input, parse_spec
from runtime.validators.kernel_validator import validate_kernel_alignment
from runtime.engines.assembly_engine import run_assembly_engine
from runtime.engines.spec_engine import run_spec_engine
from runtime.engines.constraint_engine import run_constraint_engine
from runtime.generators.shop_drawing_generator import generate_shop_drawing
from runtime.logging import RuntimeLogger
from runtime.models import (
    AssemblyModel,
    DeliverableModel,
    RuntimeReportModel,
)
from adapters.assembly_adapter import adapt_assembly


def run_assembly_pipeline(raw_input: str) -> tuple[RuntimeReportModel, dict[str, Any]]:
    """Run the full assembly pipeline.

    Flow:
        1. ingest_input
        2. normalize_input
        3. parse_structure
        4. validate_kernel_alignment
        5. build_runtime_models
        6. run_engines
        7. generate_deliverables
        8. emit_runtime_report

    Args:
        raw_input: Raw assembly text input.

    Returns:
        Tuple of (RuntimeReportModel, outputs dict).
    """
    logger = RuntimeLogger("assembly_pipeline")
    report = RuntimeReportModel(input_type="assembly")
    outputs: dict[str, Any] = {}

    # 1-2. Ingest and normalize
    logger.log_pipeline("ingest_input", "start")
    logger.log_pipeline("normalize_input", "start")
    report.actions_taken.append("ingest_input")
    report.actions_taken.append("normalize_input")

    # 3. Parse
    logger.log_pipeline("parse_structure", "start")
    parsed = parse_assembly(raw_input)
    logger.log_parser_event("assembly_parser", parsed["metadata"].get("parse_status", "unknown"))
    report.actions_taken.append("parse_structure")
    outputs["parsed"] = parsed

    # 4. Validate
    logger.log_pipeline("validate_kernel_alignment", "start")
    validation = validate_kernel_alignment(parsed, "assembly")
    logger.log_validation(validation["is_valid"], validation["warnings"], validation["errors"])
    report.actions_taken.append("validate_kernel_alignment")
    report.warnings.extend(validation["warnings"])
    report.errors.extend(validation["errors"])

    if not validation["is_valid"]:
        report.validation_status = "failed"
        logger.log_pipeline("pipeline", "aborted", "Validation failed")
        return report, outputs

    report.validation_status = "passed"

    # 5. Build runtime models
    logger.log_pipeline("build_runtime_models", "start")
    assembly_model = adapt_assembly(parsed)
    report.actions_taken.append("build_runtime_models")
    outputs["assembly_model"] = assembly_model

    # 6. Run engines
    logger.log_pipeline("run_engines", "start")

    # Constraint engine
    constraint_result = run_constraint_engine(assembly_model)
    logger.log_engine_action("constraint_engine", "validate", f"valid={constraint_result['is_valid']}")
    report.warnings.extend(constraint_result["warnings"])
    report.errors.extend(constraint_result["errors"])
    outputs["constraint_result"] = constraint_result

    if not constraint_result["is_valid"]:
        report.validation_status = "failed_constraints"
        logger.log_pipeline("pipeline", "aborted", "Constraint validation failed")
        return report, outputs

    # Assembly engine
    engine_result = run_assembly_engine(assembly_model)
    logger.log_engine_action("assembly_engine", "build", f"status={engine_result['build_status']}")
    report.actions_taken.append("run_engines")
    outputs["engine_result"] = engine_result

    # 7. Generate deliverables
    logger.log_pipeline("generate_deliverables", "start")
    deliverable = generate_shop_drawing(engine_result)
    logger.log_generation("shop_drawing", "complete")
    report.actions_taken.append("generate_deliverables")
    report.outputs_generated.append("shop_drawing")
    outputs["deliverable"] = deliverable

    # 8. Emit report
    logger.log_pipeline("emit_runtime_report", "complete")
    report.actions_taken.append("emit_runtime_report")

    return report, outputs


def run_spec_pipeline(raw_input: str) -> tuple[RuntimeReportModel, dict[str, Any]]:
    """Run the full spec intelligence pipeline.

    Flow:
        1. ingest_input
        2. normalize_input
        3. parse_structure
        4. validate_kernel_alignment
        5. build_runtime_models
        6. run_engines
        7. generate_deliverables (spec intelligence output)
        8. emit_runtime_report

    Args:
        raw_input: Raw specification text input.

    Returns:
        Tuple of (RuntimeReportModel, outputs dict).
    """
    logger = RuntimeLogger("spec_pipeline")
    report = RuntimeReportModel(input_type="spec")
    outputs: dict[str, Any] = {}

    # 1-2. Ingest and normalize
    logger.log_pipeline("ingest_input", "start")
    logger.log_pipeline("normalize_input", "start")
    report.actions_taken.append("ingest_input")
    report.actions_taken.append("normalize_input")

    # 3. Parse
    logger.log_pipeline("parse_structure", "start")
    parsed = parse_spec(raw_input)
    logger.log_parser_event("spec_parser", parsed["metadata"].get("parse_status", "unknown"))
    report.actions_taken.append("parse_structure")
    outputs["parsed"] = parsed

    # 4. Validate
    logger.log_pipeline("validate_kernel_alignment", "start")
    validation = validate_kernel_alignment(parsed, "spec")
    logger.log_validation(validation["is_valid"], validation["warnings"], validation["errors"])
    report.actions_taken.append("validate_kernel_alignment")
    report.warnings.extend(validation["warnings"])
    report.errors.extend(validation["errors"])

    if not validation["is_valid"]:
        report.validation_status = "failed"
        logger.log_pipeline("pipeline", "aborted", "Validation failed")
        return report, outputs

    report.validation_status = "passed"

    # 5-6. Run spec engine
    logger.log_pipeline("run_engines", "start")
    intelligence = run_spec_engine(parsed)
    logger.log_engine_action("spec_engine", "analyze", f"status={intelligence['intelligence_status']}")
    report.actions_taken.append("run_engines")
    outputs["intelligence"] = intelligence

    # 7. Package as deliverable output
    logger.log_pipeline("generate_deliverables", "start")
    report.actions_taken.append("generate_deliverables")
    report.outputs_generated.append("spec_intelligence")
    outputs["spec_intelligence"] = intelligence

    # 8. Emit report
    logger.log_pipeline("emit_runtime_report", "complete")
    report.actions_taken.append("emit_runtime_report")

    return report, outputs
