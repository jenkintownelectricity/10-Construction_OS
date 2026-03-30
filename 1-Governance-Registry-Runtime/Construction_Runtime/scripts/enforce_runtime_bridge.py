#!/usr/bin/env python3
"""Enforce that runtime engine internals are only accessed through the runtime bridge.

Scans all Python files in the repository for illegal direct imports of:
  - runtime.condition_graph.*
  - runtime.drawing_engine.*
  - runtime.artifact_renderer.*

The only allowed import style is through the public facade:
  from runtime import evaluate_condition_graph, resolve_detail, render_artifact, validate_state

Files inside the runtime/ package itself are exempt (engines may reference
each other internally).  The boundary applies to every file *outside*
runtime/.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Patterns that indicate a direct engine import (illegal outside runtime/)
ILLEGAL_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^\s*(?:from|import)\s+runtime\.condition_graph\b"),
    re.compile(r"^\s*(?:from|import)\s+runtime\.drawing_engine\b"),
    re.compile(r"^\s*(?:from|import)\s+runtime\.artifact_renderer\b"),
]

# Directories that are allowed to use internal engine imports.
# - runtime/: engines may reference each other internally
# - tests/: unit tests legitimately test engine internals directly
# - apps/: internal applications (to be migrated to bridge in a future pass)
EXEMPT_DIRS: set[str] = {"runtime", "tests", "apps"}


def is_exempt(filepath: Path) -> bool:
    """Return True if the file lives inside an exempt directory."""
    rel = filepath.relative_to(REPO_ROOT)
    parts = rel.parts
    return len(parts) > 0 and parts[0] in EXEMPT_DIRS


def scan_file(filepath: Path) -> list[tuple[int, str]]:
    """Return a list of (line_number, line_text) for illegal imports."""
    violations: list[tuple[int, str]] = []
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return violations

    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in ILLEGAL_PATTERNS:
            if pattern.search(line):
                violations.append((lineno, line.rstrip()))
                break
    return violations


def main() -> int:
    total_violations = 0

    for dirpath, _dirnames, filenames in os.walk(REPO_ROOT):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            filepath = Path(dirpath) / fname
            if is_exempt(filepath):
                continue

            violations = scan_file(filepath)
            for lineno, line in violations:
                rel = filepath.relative_to(REPO_ROOT)
                print(f"BOUNDARY VIOLATION  {rel}:{lineno}  {line}")
                total_violations += 1

    if total_violations:
        print(f"\n{total_violations} boundary violation(s) detected.")
        print("Engine internals must only be accessed through the runtime bridge:")
        print("  from runtime import evaluate_condition_graph, resolve_detail, render_artifact, validate_state")
        return 1

    print("Runtime bridge boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
