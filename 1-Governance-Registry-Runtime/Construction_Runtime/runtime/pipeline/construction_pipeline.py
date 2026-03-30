"""Construction pipeline v0.2.

Orchestrates the full runtime flow with multi-layer validation,
geometry engine, drawing instruction generation, and audit logging.

Pipeline stages:
    INPUT → Parse → Normalize → Structural Validation → Domain Validation →
    Geometry Engine → DrawingInstructionSet → Generation Validation →
    DXF Writer → SVG Writer → DeliverableModel → Audit Log
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
from contracts import validate_contract
from validators.structural_validator import validate_structural
from validators.domain_validator import validate_domain


def run_assembly_pipeline(raw_input: str) -> tuple[RuntimeReportModel, dict[str, Any]]:
    """Run the full assembly pipeline.

    v0.2 flow:
        1. Ingest input
        2. Normalize input
        3. Parse structure
        4. Structural validation (with contract check)
        5. Domain validation
        6. Build runtime models
        7. Run engines (constraint + assembly)
        8. Geometry engine → DrawingInstructionSet → Generation validation
        9. DXF + SVG generation
        10. Emit runtime report + audit log

    Args:
        raw_input: Raw assembly text input.

    Returns:
        Tuple of (RuntimeReportModel, outputs dict).
    """
    logger = RuntimeLogger("assembly_pipeline")
    report = RuntimeReportModel(input_type="assembly")
    outputs: dict[str, Any] = {}

    # 1-2. Ingest and normalize
    logger.log_pipeline_started("assembly", raw_input)
    report.actions_taken.append("ingest_input")
    report.actions_taken.append("normalize_input")

    # 3. Parse
    parsed = parse_assembly(raw_input)
    logger.log_parse_completed("assembly_parser", parsed)
    report.actions_taken.append("parse_structure")
    outputs["parsed"] = parsed

    # 4. Structural validation
    structural = validate_structural(parsed, "assembly")
    logger.log_validation_result("structural", structural["is_valid"], structural.get("errors", []))
    report.actions_taken.append("structural_validation")

    if not structural["is_valid"]:
        report.validation_status = "failed"
        for e in structural["errors"]:
            report.errors.append(e["message"] if isinstance(e, dict) else str(e))
        report.warnings.extend(structural["warnings"])
        logger.log_pipeline_aborted("Structural validation failed")
        return report, outputs

    report.warnings.extend(structural["warnings"])

    # Contract validation on parsed output
    contract_result = validate_contract(parsed, "assembly_input")
    if not contract_result["is_valid"]:
        report.warnings.append(f"Contract warning: {contract_result['errors']}")

    # 5. Domain validation
    domain = validate_domain(parsed, "assembly")
    logger.log_validation_result("domain", domain["is_valid"], domain.get("errors", []))
    report.actions_taken.append("domain_validation")

    if not domain["is_valid"]:
        report.validation_status = "failed"
        for e in domain["errors"]:
            report.errors.append(e["message"] if isinstance(e, dict) else str(e))
        report.warnings.extend(domain["warnings"])
        logger.log_pipeline_aborted("Domain validation failed")
        return report, outputs

    report.warnings.extend(domain["warnings"])
    report.validation_status = "passed"

    # 6. Build runtime models
    assembly_model = adapt_assembly(parsed)
    report.actions_taken.append("build_runtime_models")
    outputs["assembly_model"] = assembly_model

    # 7. Run engines
    # Constraint engine
    constraint_result = run_constraint_engine(assembly_model)
    logger.log_engine_action("constraint_engine", "validate", f"valid={constraint_result['is_valid']}")
    report.warnings.extend(constraint_result["warnings"])
    outputs["constraint_result"] = constraint_result

    if not constraint_result["is_valid"]:
        report.validation_status = "failed_constraints"
        report.errors.extend(constraint_result["errors"])
        logger.log_pipeline_aborted("Constraint validation failed")
        return report, outputs

    # Assembly engine
    engine_result = run_assembly_engine(assembly_model)
    logger.log_engine_action("assembly_engine", "build", f"status={engine_result['build_status']}")
    report.actions_taken.append("run_engines")
    outputs["engine_result"] = engine_result

    # 8-9. Generate deliverables (geometry → instructions → DXF + SVG)
    deliverable = generate_shop_drawing(engine_result)
    logger.log_generation_completed("shop_drawing", deliverable.to_dict())
    logger.log_deliverable_emitted(deliverable.deliverable_id, list(deliverable.formats.keys()))
    report.actions_taken.append("generate_deliverables")
    report.outputs_generated.append("shop_drawing")

    # Track format statuses
    for fmt_name, fmt in deliverable.formats.items():
        if fmt.status == "generated":
            report.outputs_generated.append(f"{fmt_name}:{fmt.status}")

    outputs["deliverable"] = deliverable

    # 10. Emit report
    logger.log_pipeline_completed()
    report.actions_taken.append("emit_runtime_report")
    outputs["audit_log"] = logger.get_events()

    return report, outputs


def run_spec_pipeline(raw_input: str) -> tuple[RuntimeReportModel, dict[str, Any]]:
    """Run the full spec intelligence pipeline.

    v0.2 flow:
        1. Ingest input
        2. Normalize input
        3. Parse structure
        4. Structural validation (with contract check)
        5. Domain validation
        6. Run spec engine
        7. Emit runtime report + audit log

    Args:
        raw_input: Raw specification text input.

    Returns:
        Tuple of (RuntimeReportModel, outputs dict).
    """
    logger = RuntimeLogger("spec_pipeline")
    report = RuntimeReportModel(input_type="spec")
    outputs: dict[str, Any] = {}

    # 1-2. Ingest and normalize
    logger.log_pipeline_started("spec", raw_input)
    report.actions_taken.append("ingest_input")
    report.actions_taken.append("normalize_input")

    # 3. Parse
    parsed = parse_spec(raw_input)
    logger.log_parse_completed("spec_parser", parsed)
    report.actions_taken.append("parse_structure")
    outputs["parsed"] = parsed

    # 4. Structural validation
    structural = validate_structural(parsed, "spec")
    logger.log_validation_result("structural", structural["is_valid"], structural.get("errors", []))
    report.actions_taken.append("structural_validation")

    if not structural["is_valid"]:
        report.validation_status = "failed"
        for e in structural["errors"]:
            report.errors.append(e["message"] if isinstance(e, dict) else str(e))
        report.warnings.extend(structural["warnings"])
        logger.log_pipeline_aborted("Structural validation failed")
        return report, outputs

    report.warnings.extend(structural["warnings"])

    # Contract validation
    contract_result = validate_contract(parsed, "spec_input")
    if not contract_result["is_valid"]:
        report.warnings.append(f"Contract warning: {contract_result['errors']}")

    # 5. Domain validation
    domain = validate_domain(parsed, "spec")
    logger.log_validation_result("domain", domain["is_valid"], domain.get("errors", []))
    report.actions_taken.append("domain_validation")

    if not domain["is_valid"]:
        report.validation_status = "failed"
        for e in domain["errors"]:
            report.errors.append(e["message"] if isinstance(e, dict) else str(e))
        report.warnings.extend(domain["warnings"])
        logger.log_pipeline_aborted("Domain validation failed")
        return report, outputs

    report.warnings.extend(domain["warnings"])
    report.validation_status = "passed"

    # 6. Run spec engine
    intelligence = run_spec_engine(parsed)
    logger.log_engine_action("spec_engine", "analyze", f"status={intelligence['intelligence_status']}")
    report.actions_taken.append("run_engines")
    outputs["intelligence"] = intelligence

    # Contract validation on engine output
    contract_result = validate_contract(intelligence, "runtime_spec")
    if not contract_result["is_valid"]:
        report.warnings.append(f"Spec output contract warning: {contract_result['errors']}")

    # 7. Package as deliverable output
    report.actions_taken.append("generate_deliverables")
    report.outputs_generated.append("spec_intelligence")
    outputs["spec_intelligence"] = intelligence

    # Emit report
    logger.log_pipeline_completed()
    report.actions_taken.append("emit_runtime_report")
    outputs["audit_log"] = logger.get_events()

    return report, outputs
