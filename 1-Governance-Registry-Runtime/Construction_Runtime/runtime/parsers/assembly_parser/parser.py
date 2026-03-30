"""Assembly parser.

Parses normalized assembly input into structured assembly payloads.
Extracts components, constraints, and assembly structure from text input.
"""

import re
from typing import Any

from .normalizer import normalize_assembly_input


def parse_assembly(raw_input: str) -> dict[str, Any]:
    """Parse raw assembly input into a structured assembly payload.

    Flow:
        1. Ingest raw input
        2. Normalize input
        3. Parse assembly structure
        4. Extract components
        5. Extract constraints
        6. Emit structured assembly payload

    Args:
        raw_input: Raw assembly text.

    Returns:
        Structured assembly payload dictionary with keys:
            - name: assembly name (if detected)
            - components: list of extracted components
            - constraints: list of extracted constraints
            - source_text: the normalized input text
            - metadata: additional parsed metadata
    """
    normalized = normalize_assembly_input(raw_input)

    if not normalized:
        return {
            "name": "",
            "components": [],
            "constraints": [],
            "source_text": "",
            "metadata": {"parse_status": "empty_input"},
        }

    name = _extract_assembly_name(normalized)
    components = _extract_components(normalized)
    constraints = _extract_constraints(normalized)

    return {
        "name": name,
        "components": components,
        "constraints": constraints,
        "source_text": normalized,
        "metadata": {
            "parse_status": "success",
            "line_count": len(normalized.split("\n")),
            "component_count": len(components),
            "constraint_count": len(constraints),
        },
    }


def _extract_assembly_name(text: str) -> str:
    """Extract assembly name from the first non-empty line or explicit label."""
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Check for explicit name patterns
        match = re.match(r"(?:assembly|name|title)\s*[:=]\s*(.+)", line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        # Fall back to first non-empty line
        return line
    return ""


def _extract_components(text: str) -> list[dict[str, str]]:
    """Extract components from assembly text.

    Looks for lines that describe parts, members, or components.
    Recognizes patterns like:
        - 'component: <name>'
        - 'part: <name>'
        - 'member: <name>'
        - bulleted or numbered list items under a components heading
    """
    components = []
    in_components_section = False

    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            in_components_section = False
            continue

        # Check for section header
        if re.match(r"(?:components|parts|members)\s*:", stripped, re.IGNORECASE):
            in_components_section = True
            # Check if value is on same line after colon
            after_colon = stripped.split(":", 1)[1].strip()
            if after_colon:
                components.append({"name": after_colon, "type": "component"})
            continue

        # Explicit component/part/member line
        match = re.match(
            r"(?:component|part|member)\s*[:=]\s*(.+)", stripped, re.IGNORECASE
        )
        if match:
            components.append({"name": match.group(1).strip(), "type": "component"})
            continue

        # List items inside a components section
        if in_components_section:
            item_match = re.match(r"[-*\d.]+\s*(.+)", stripped)
            if item_match:
                components.append(
                    {"name": item_match.group(1).strip(), "type": "component"}
                )

    return components


def _extract_constraints(text: str) -> list[dict[str, str]]:
    """Extract constraints from assembly text.

    Recognizes patterns like:
        - 'constraint: <description>'
        - 'clearance: <value>'
        - 'spacing: <value>'
        - 'interface: <description>'
    """
    constraints = []
    constraint_patterns = [
        (r"constraint\s*[:=]\s*(.+)", "constraint"),
        (r"clearance\s*[:=]\s*(.+)", "clearance"),
        (r"spacing\s*[:=]\s*(.+)", "spacing"),
        (r"interface\s*[:=]\s*(.+)", "interface"),
        (r"tolerance\s*[:=]\s*(.+)", "tolerance"),
    ]

    for line in text.split("\n"):
        stripped = line.strip()
        for pattern, ctype in constraint_patterns:
            match = re.match(pattern, stripped, re.IGNORECASE)
            if match:
                constraints.append(
                    {"description": match.group(1).strip(), "type": ctype}
                )
                break

    return constraints
