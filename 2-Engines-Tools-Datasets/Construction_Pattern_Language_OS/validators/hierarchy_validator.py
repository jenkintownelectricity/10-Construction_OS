"""
Hierarchy Validator for Construction_Pattern_Language_OS

Validates the canonical entity hierarchy:
  PatternFamily -> Pattern -> PatternVariant

Rules enforced:
  - Every variant must reference an existing pattern_id
  - Every pattern must reference an existing family_id
  - Every pattern listed in a family's patterns array must exist
  - Every variant listed in a pattern's variants array must exist
  - No orphaned entities allowed

Fail-closed: any violation causes validation failure.
"""

import json
import sys
import os
import yaml
from pathlib import Path
from typing import Dict, List, Set


def load_yaml_file(filepath: str) -> object:
    """Safely load a YAML file."""
    try:
        with open(filepath, "r") as f:
            return yaml.safe_load(f)
    except (yaml.YAMLError, IOError):
        return None


def load_json_file(filepath: str) -> object:
    """Safely load a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def load_data_file(filepath: str) -> object:
    """Load a YAML or JSON file and return its contents."""
    if filepath.endswith((".yaml", ".yml")):
        return load_yaml_file(filepath)
    elif filepath.endswith(".json"):
        return load_json_file(filepath)
    return None


def gather_records(directory: str) -> List[dict]:
    """Load all records from YAML/JSON files in a directory tree.

    Each record gets a '_source_file' key injected for error reporting.
    Handles both single-object files and list-of-objects files.
    """
    results = []
    root = Path(directory)
    if not root.is_dir():
        return results
    for ext in ("*.yaml", "*.yml", "*.json"):
        for fpath in root.rglob(ext):
            if ".git" in str(fpath) or "schema" in fpath.name:
                continue
            data = load_data_file(str(fpath))
            if isinstance(data, dict):
                data["_source_file"] = str(fpath)
                results.append(data)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        item["_source_file"] = str(fpath)
                        results.append(item)
    return results


def classify_record(record: dict) -> str:
    """Return 'family', 'pattern', 'variant', or None based on the TYPE segment of the id."""
    rid = record.get("id", "")
    if not rid or "CONSTR" not in rid:
        return None
    parts = rid.split("-")
    # Format: <CLASS>-CONSTR-<TYPE>-<NAME>-<INDEX>-R<REV>
    # parts[2] is the TYPE segment
    if len(parts) >= 3:
        type_seg = parts[2]
        if type_seg == "FAM":
            return "family"
        elif type_seg == "PAT":
            return "pattern"
        elif type_seg == "VAR":
            return "variant"
    return None


def validate_hierarchy(root_dir: str) -> bool:
    """Validate the full pattern hierarchy. Fail-closed."""
    errors: List[str] = []

    pattern_lang_dir = os.path.join(root_dir, "pattern_language")
    records = gather_records(pattern_lang_dir)

    families: Dict[str, dict] = {}
    patterns: Dict[str, dict] = {}
    variants: Dict[str, dict] = {}

    for record in records:
        kind = classify_record(record)
        rid = record.get("id", "")
        src = record.get("_source_file", "<unknown>")
        if kind == "family":
            families[rid] = record
        elif kind == "pattern":
            patterns[rid] = record
        elif kind == "variant":
            variants[rid] = record

    # ---- Every pattern must reference an existing family_id ----
    for pat_id, pat in patterns.items():
        fam_id = pat.get("family_id", "")
        src = pat.get("_source_file", "<unknown>")
        if not fam_id:
            errors.append(
                f"Pattern '{pat_id}' has no family_id  [{src}]"
            )
        elif fam_id not in families:
            errors.append(
                f"Pattern '{pat_id}' references non-existent family '{fam_id}'  [{src}]"
            )

    # ---- Every variant must reference an existing pattern_id ----
    for var_id, var in variants.items():
        pat_id = var.get("pattern_id", "")
        src = var.get("_source_file", "<unknown>")
        if not pat_id:
            errors.append(
                f"Variant '{var_id}' has no pattern_id  [{src}]"
            )
        elif pat_id not in patterns:
            errors.append(
                f"Variant '{var_id}' references non-existent pattern '{pat_id}'  [{src}]"
            )

    # ---- Every entry in a family's patterns array must exist ----
    for fam_id, fam in families.items():
        src = fam.get("_source_file", "<unknown>")
        for pat_ref in fam.get("patterns", []):
            if pat_ref not in patterns:
                errors.append(
                    f"Family '{fam_id}' lists non-existent pattern '{pat_ref}'  [{src}]"
                )

    # ---- Every entry in a pattern's variants array must exist ----
    for pat_id, pat in patterns.items():
        src = pat.get("_source_file", "<unknown>")
        for var_ref in pat.get("variants", []):
            if var_ref not in variants:
                errors.append(
                    f"Pattern '{pat_id}' lists non-existent variant '{var_ref}'  [{src}]"
                )

    # ---- No orphaned patterns (not claimed by any family) ----
    claimed_patterns: Set[str] = set()
    for fam in families.values():
        for pat_ref in fam.get("patterns", []):
            claimed_patterns.add(pat_ref)
    for pat_id in patterns:
        if pat_id not in claimed_patterns:
            src = patterns[pat_id].get("_source_file", "<unknown>")
            errors.append(
                f"Orphaned pattern '{pat_id}' is not listed in any family's patterns array  [{src}]"
            )

    # ---- No orphaned variants (not claimed by any pattern) ----
    claimed_variants: Set[str] = set()
    for pat in patterns.values():
        for var_ref in pat.get("variants", []):
            claimed_variants.add(var_ref)
    for var_id in variants:
        if var_id not in claimed_variants:
            src = variants[var_id].get("_source_file", "<unknown>")
            errors.append(
                f"Orphaned variant '{var_id}' is not listed in any pattern's variants array  [{src}]"
            )

    # ---- Report ----
    print("Hierarchy Validation Report")
    print("=" * 60)
    print(f"Families found:  {len(families)}")
    print(f"Patterns found:  {len(patterns)}")
    print(f"Variants found:  {len(variants)}")
    print(f"Errors:          {len(errors)}")

    if errors:
        print("\nFAILURES:")
        for err in errors:
            print(f"  {err}")
        print("\nRESULT: FAIL (fail-closed)")
        return False

    print("\nRESULT: PASS")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            f"Usage: python {sys.argv[0]} <path_to_repo_root>",
            file=sys.stderr,
        )
        sys.exit(1)
    repo_root = sys.argv[1]
    if not os.path.isdir(repo_root):
        print(f"ERROR: '{repo_root}' is not a directory", file=sys.stderr)
        sys.exit(1)
    success = validate_hierarchy(repo_root)
    sys.exit(0 if success else 1)
