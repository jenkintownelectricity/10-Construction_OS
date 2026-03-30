"""Assembly input normalizer.

Cleans and standardizes raw assembly input before parsing.
Normalization runs before any extraction to ensure consistent downstream processing.
"""

import re


def normalize_assembly_input(raw_input: str) -> str:
    """Normalize raw assembly input text.

    Steps:
        1. Strip leading/trailing whitespace
        2. Collapse multiple whitespace to single spaces within lines
        3. Normalize line endings
        4. Remove null bytes and control characters (except newlines/tabs)
        5. Strip blank lines at start and end, preserve internal structure

    Args:
        raw_input: Raw assembly text input.

    Returns:
        Normalized assembly text ready for parsing.
    """
    if not raw_input or not raw_input.strip():
        return ""

    text = raw_input.replace("\r\n", "\n").replace("\r", "\n")

    # Remove control characters except newline and tab
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # Collapse multiple spaces/tabs within each line
    lines = text.split("\n")
    normalized_lines = []
    for line in lines:
        cleaned = re.sub(r"[ \t]+", " ", line.strip())
        normalized_lines.append(cleaned)

    # Strip leading/trailing blank lines but preserve internal blanks
    while normalized_lines and normalized_lines[0] == "":
        normalized_lines.pop(0)
    while normalized_lines and normalized_lines[-1] == "":
        normalized_lines.pop()

    return "\n".join(normalized_lines)
