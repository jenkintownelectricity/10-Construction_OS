"""Specification parser.

Parses normalized specification text into structured spec intelligence payloads.
Identifies sections, product/system requirements, and manufacturer references.
"""

import re
from typing import Any

from .normalizer import normalize_spec_input


def parse_spec(raw_input: str) -> dict[str, Any]:
    """Parse raw specification input into a structured spec intelligence payload.

    Flow:
        1. Ingest raw specification text
        2. Normalize input
        3. Identify relevant sections
        4. Detect product/system requirements
        5. Detect manufacturer or product references
        6. Emit structured spec intelligence payload

    Args:
        raw_input: Raw specification text.

    Returns:
        Structured spec intelligence payload with keys:
            - sections: list of identified sections
            - requirements: list of detected requirements
            - product_references: list of manufacturer/product references
            - source_text: the normalized input text
            - metadata: additional parsed metadata
    """
    normalized = normalize_spec_input(raw_input)

    if not normalized:
        return {
            "sections": [],
            "requirements": [],
            "product_references": [],
            "source_text": "",
            "metadata": {"parse_status": "empty_input"},
        }

    sections = _identify_sections(normalized)
    requirements = _detect_requirements(normalized)
    product_references = _detect_product_references(normalized)

    return {
        "sections": sections,
        "requirements": requirements,
        "product_references": product_references,
        "source_text": normalized,
        "metadata": {
            "parse_status": "success",
            "line_count": len(normalized.split("\n")),
            "section_count": len(sections),
            "requirement_count": len(requirements),
            "reference_count": len(product_references),
        },
    }


def _identify_sections(text: str) -> list[dict[str, Any]]:
    """Identify specification sections from text.

    Looks for numbered sections (e.g., '1.0', '2.1', 'Section 3')
    and common specification headings.
    """
    sections = []
    section_pattern = re.compile(
        r"^(?:section\s+)?(\d+(?:\.\d+)*)\s*[-:.]\s*(.+)", re.IGNORECASE
    )

    lines = text.split("\n")
    for i, line in enumerate(lines):
        stripped = line.strip()
        match = section_pattern.match(stripped)
        if match:
            sections.append({
                "number": match.group(1),
                "title": match.group(2).strip(),
                "line": i + 1,
            })

    return sections


def _detect_requirements(text: str) -> list[dict[str, str]]:
    """Detect product/system requirements from specification text.

    Identifies lines containing requirement keywords like 'shall', 'must',
    'required', and categorizes them.
    """
    requirements = []
    req_keywords = re.compile(
        r"\b(shall|must|required|mandatory|minimum)\b", re.IGNORECASE
    )

    for line in text.split("\n"):
        stripped = line.strip()
        if req_keywords.search(stripped):
            req_type = "mandatory" if re.search(
                r"\b(shall|must|mandatory)\b", stripped, re.IGNORECASE
            ) else "recommended"
            requirements.append({
                "text": stripped,
                "type": req_type,
            })

    return requirements


def _detect_product_references(text: str) -> list[dict[str, str]]:
    """Detect manufacturer or product references in specification text.

    Looks for patterns like:
        - 'manufacturer: <name>'
        - 'product: <name>'
        - 'basis of design: <name>'
        - quoted product names following 'or equal'
    """
    references = []
    ref_patterns = [
        (r"manufacturer\s*[:=]\s*(.+)", "manufacturer"),
        (r"product\s*[:=]\s*(.+)", "product"),
        (r"basis\s+of\s+design\s*[:=]\s*(.+)", "basis_of_design"),
        (r"model\s*(?:no\.?|number)?\s*[:=]\s*(.+)", "model"),
    ]

    for line in text.split("\n"):
        stripped = line.strip()
        for pattern, ref_type in ref_patterns:
            match = re.match(pattern, stripped, re.IGNORECASE)
            if match:
                references.append({
                    "value": match.group(1).strip(),
                    "type": ref_type,
                })
                break

    return references
