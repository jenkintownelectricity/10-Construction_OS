"""Specification input normalizer.

Cleans and standardizes raw specification text before parsing.
"""

import re


def normalize_spec_input(raw_input: str) -> str:
    """Normalize raw specification input text.

    Steps:
        1. Strip leading/trailing whitespace
        2. Normalize line endings
        3. Remove control characters
        4. Collapse excessive blank lines (max two consecutive)
        5. Normalize section numbering whitespace

    Args:
        raw_input: Raw specification text.

    Returns:
        Normalized specification text ready for parsing.
    """
    if not raw_input or not raw_input.strip():
        return ""

    text = raw_input.replace("\r\n", "\n").replace("\r", "\n")

    # Remove control characters except newline and tab
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Collapse runs of 3+ blank lines to 2
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    # Normalize each line
    lines = text.split("\n")
    normalized_lines = []
    for line in lines:
        cleaned = re.sub(r"[ \t]+", " ", line.strip())
        normalized_lines.append(cleaned)

    # Strip leading/trailing blank lines
    while normalized_lines and normalized_lines[0] == "":
        normalized_lines.pop(0)
    while normalized_lines and normalized_lines[-1] == "":
        normalized_lines.pop()

    return "\n".join(normalized_lines)
