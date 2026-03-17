"""Spec engine.

Processes parsed specification data to identify system/product opportunities
and emit structured intelligence payloads.
"""

from typing import Any


def run_spec_engine(parsed_spec: dict[str, Any]) -> dict[str, Any]:
    """Process parsed specification data into structured intelligence.

    Identifies likely system/product opportunities based on requirements
    and product references found in the specification.

    Args:
        parsed_spec: Output from the spec parser.

    Returns:
        Dictionary with:
            - opportunities: list of identified system/product opportunities
            - requirement_summary: summary of requirements by type
            - reference_summary: summary of product references
            - intelligence_status: 'complete' or 'partial'
    """
    requirements = parsed_spec.get("requirements", [])
    references = parsed_spec.get("product_references", [])
    sections = parsed_spec.get("sections", [])

    # Summarize requirements by type
    req_by_type: dict[str, int] = {}
    for req in requirements:
        rtype = req.get("type", "unknown")
        req_by_type[rtype] = req_by_type.get(rtype, 0) + 1

    # Summarize references by type
    ref_by_type: dict[str, list[str]] = {}
    for ref in references:
        rtype = ref.get("type", "unknown")
        ref_by_type.setdefault(rtype, []).append(ref.get("value", ""))

    # Identify opportunities: sections with requirements + product references
    opportunities = []
    if references:
        for ref in references:
            opportunities.append({
                "type": "product_opportunity",
                "reference": ref.get("value", ""),
                "reference_type": ref.get("type", ""),
                "related_requirements": len(requirements),
            })

    has_requirements = len(requirements) > 0
    has_references = len(references) > 0
    intelligence_status = "complete" if (has_requirements or has_references) else "partial"

    return {
        "opportunities": opportunities,
        "requirement_summary": req_by_type,
        "reference_summary": ref_by_type,
        "section_count": len(sections),
        "intelligence_status": intelligence_status,
    }
