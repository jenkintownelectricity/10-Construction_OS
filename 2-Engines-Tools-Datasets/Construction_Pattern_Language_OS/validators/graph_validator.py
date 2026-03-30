"""
Graph Validator for Construction_Pattern_Language_OS

Validates the pattern relationship graph:
  - All source and target references point to existing entities
  - No dangling references
  - No self-referencing relationships
  - relationship_type must be one of: adjacency, conflict, dependency
  - Artifact intent pattern_refs must reference existing entities
  - Constraint profile applies_to references must reference existing entities
  - Dependency subgraph is acyclic (no circular dependencies)
  - Adjacency cycles are allowed (bidirectional adjacency is valid)
  - Conflict relationships are symmetric (A conflicts B implies B conflicts A)
  - Deprecation/index integrity (no deprecated IDs referenced)
  - Schema/version compatibility across entities

Fail-closed: any violation causes validation failure.
"""

import json
import sys
import os
import yaml
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, List, Set, Tuple


VALID_RELATIONSHIP_TYPES = {"adjacency", "conflict", "dependency"}


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


def gather_files_from(directory: str) -> List[str]:
    """Collect all YAML/JSON file paths under a directory."""
    root = Path(directory)
    files = []
    if not root.is_dir():
        return files
    for ext in ("*.yaml", "*.yml", "*.json"):
        for fpath in root.rglob(ext):
            if ".git" in str(fpath) or "schema" in fpath.name:
                continue
            files.append(str(fpath))
    return sorted(files)


def extract_records(filepath: str) -> List[dict]:
    """Load a file and return a list of dict records (handles single or list)."""
    data = load_data_file(filepath)
    records = []
    if isinstance(data, dict):
        data["_source_file"] = filepath
        records.append(data)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                item["_source_file"] = filepath
                records.append(item)
    return records


def collect_all_entity_ids(root_dir: str) -> Set[str]:
    """Collect every entity ID from pattern_language/ directory."""
    ids: Set[str] = set()
    pattern_lang_dir = os.path.join(root_dir, "pattern_language")
    for filepath in gather_files_from(pattern_lang_dir):
        for record in extract_records(filepath):
            rid = record.get("id", "")
            if rid and "CONSTR" in rid:
                ids.add(rid)
    return ids


def collect_relationships(root_dir: str) -> List[dict]:
    """Collect all relationship records from pattern_relationships/."""
    relationships = []
    rel_dir = os.path.join(root_dir, "pattern_relationships")
    for filepath in gather_files_from(rel_dir):
        for record in extract_records(filepath):
            rid = record.get("id", "")
            if "CONSTR" in rid and "REL" in rid:
                relationships.append(record)
    return relationships


def collect_artifact_intents(root_dir: str) -> List[dict]:
    """Collect all artifact intent records from artifact_intents/."""
    intents = []
    art_dir = os.path.join(root_dir, "artifact_intents")
    for filepath in gather_files_from(art_dir):
        for record in extract_records(filepath):
            rid = record.get("id", "")
            if rid and "CONSTR" in rid:
                intents.append(record)
    return intents


def collect_constraint_profiles(root_dir: str) -> List[dict]:
    """Collect all constraint profile records from constraint_profiles/."""
    profiles = []
    cns_dir = os.path.join(root_dir, "constraint_profiles")
    for filepath in gather_files_from(cns_dir):
        for record in extract_records(filepath):
            rid = record.get("id", "")
            if rid and "CONSTR" in rid:
                profiles.append(record)
    return profiles


def extract_ref_id(ref) -> str:
    """Extract an entity ID from a reference that may be a string or a dict with 'id' key."""
    if isinstance(ref, str):
        return ref
    if isinstance(ref, dict):
        return ref.get("id", "")
    return ""


def extract_source_target(rel: dict) -> Tuple[str, str]:
    """Extract source and target IDs from a relationship record.

    Handles both flat format (source_id, target_id) and nested format
    (source.id, target.id).
    """
    source = rel.get("source_id", "")
    if not source:
        source_obj = rel.get("source", {})
        if isinstance(source_obj, dict):
            source = source_obj.get("id", "")

    target = rel.get("target_id", "")
    if not target:
        target_obj = rel.get("target", {})
        if isinstance(target_obj, dict):
            target = target_obj.get("id", "")

    return source, target


def extract_rel_type(rel: dict) -> str:
    """Extract relationship type, handling both 'relationship_type' and 'type' keys."""
    return rel.get("relationship_type", "") or rel.get("type", "")


def detect_dependency_cycles(relationships: List[dict]) -> List[str]:
    """Check that the dependency subgraph is acyclic (DAG). Returns error strings."""
    adj: Dict[str, Set[str]] = defaultdict(set)
    for rel in relationships:
        rel_type = extract_rel_type(rel)
        if rel_type != "dependency":
            continue
        source, target = extract_source_target(rel)
        if source and target:
            adj[source].add(target)

    # Topological sort via Kahn's algorithm
    in_degree: Dict[str, int] = defaultdict(int)
    all_nodes: Set[str] = set()
    for src, targets in adj.items():
        all_nodes.add(src)
        for tgt in targets:
            all_nodes.add(tgt)
            in_degree[tgt] += 1

    queue = deque(n for n in all_nodes if in_degree[n] == 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for neighbor in adj.get(node, set()):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    errors = []
    if visited < len(all_nodes):
        cycle_nodes = [n for n in all_nodes if in_degree[n] > 0]
        errors.append(
            f"Dependency cycle detected involving: {sorted(cycle_nodes)}"
        )
    return errors


def check_conflict_symmetry(relationships: List[dict]) -> List[str]:
    """Check that conflict relationships are symmetric.

    If A conflicts with B, there must be a corresponding B conflicts with A
    relationship (or the same relationship is understood as bidirectional).
    Returns warnings for missing symmetric pairs.
    """
    conflict_pairs: Set[Tuple[str, str]] = set()
    for rel in relationships:
        rel_type = extract_rel_type(rel)
        if rel_type != "conflict":
            continue
        source, target = extract_source_target(rel)
        if source and target:
            conflict_pairs.add((source, target))

    errors = []
    for source, target in conflict_pairs:
        if (target, source) not in conflict_pairs:
            errors.append(
                f"Conflict asymmetry: '{source}' conflicts with '{target}' "
                f"but no reverse conflict '{target}' → '{source}' exists"
            )
    return errors


def check_schema_version_compatibility(
    relationships: List[dict],
    artifact_intents: List[dict],
    constraint_profiles: List[dict],
    all_records: List[dict],
) -> List[str]:
    """Check that all entities use compatible schema_version and pattern_language_version."""
    errors = []
    all_entities = relationships + artifact_intents + constraint_profiles + all_records
    versions_seen: Dict[str, Set[str]] = {
        "schema_version": set(),
        "pattern_language_version": set(),
    }

    for entity in all_entities:
        for key in ("schema_version", "pattern_language_version"):
            val = entity.get(key, "")
            if val:
                versions_seen[key].add(val)

    for key, vals in versions_seen.items():
        if len(vals) > 1:
            errors.append(
                f"Mixed {key} values detected: {sorted(vals)}. "
                f"All entities must use compatible versions."
            )

    return errors


def check_deprecation_integrity(all_ids: Set[str], root_dir: str) -> List[str]:
    """Check that no entity references a deprecated ID.

    Deprecated entities (if any exist) are identified by a 'deprecated: true'
    field or 'status: deprecated'. Any reference to a deprecated ID from a
    non-deprecated entity is an error.
    """
    deprecated_ids: Set[str] = set()
    errors = []

    for subdir in ("pattern_language", "pattern_relationships",
                    "artifact_intents", "constraint_profiles"):
        dirpath = os.path.join(root_dir, subdir)
        for filepath in gather_files_from(dirpath):
            for record in extract_records(filepath):
                rid = record.get("id", "")
                if not rid:
                    continue
                is_deprecated = (
                    record.get("deprecated", False) is True
                    or record.get("status", "").lower() == "deprecated"
                )
                if is_deprecated:
                    deprecated_ids.add(rid)

    if not deprecated_ids:
        return errors

    # Scan all references for deprecated IDs
    rel_dir = os.path.join(root_dir, "pattern_relationships")
    for filepath in gather_files_from(rel_dir):
        for record in extract_records(filepath):
            rid = record.get("id", "")
            if rid in deprecated_ids:
                continue
            source, target = extract_source_target(record)
            src_file = record.get("_source_file", "<unknown>")
            if source in deprecated_ids:
                errors.append(
                    f"Reference to deprecated ID '{source}' in "
                    f"relationship '{rid}'  [{src_file}]"
                )
            if target in deprecated_ids:
                errors.append(
                    f"Reference to deprecated ID '{target}' in "
                    f"relationship '{rid}'  [{src_file}]"
                )

    return errors


def validate_graph(root_dir: str) -> bool:
    """Validate the relationship graph and cross-references. Fail-closed."""
    errors: List[str] = []

    # Collect all known entity IDs from pattern_language/
    all_ids = collect_all_entity_ids(root_dir)

    # Also include IDs from artifact_intents and constraint_profiles themselves
    # so relationships can reference them
    artifact_intents = collect_artifact_intents(root_dir)
    constraint_profiles = collect_constraint_profiles(root_dir)
    relationships = collect_relationships(root_dir)

    for art in artifact_intents:
        rid = art.get("id", "")
        if rid:
            all_ids.add(rid)
    for cns in constraint_profiles:
        rid = cns.get("id", "")
        if rid:
            all_ids.add(rid)
    for rel in relationships:
        rid = rel.get("id", "")
        if rid:
            all_ids.add(rid)

    # ---- Validate relationships ----
    for rel in relationships:
        rel_id = rel.get("id", "UNKNOWN")
        source, target = extract_source_target(rel)
        rel_type = extract_rel_type(rel)
        src_file = rel.get("_source_file", "<unknown>")

        # Validate relationship type
        if rel_type not in VALID_RELATIONSHIP_TYPES:
            errors.append(
                f"Relationship '{rel_id}': invalid relationship_type '{rel_type}' "
                f"(must be one of {sorted(VALID_RELATIONSHIP_TYPES)})  [{src_file}]"
            )

        # Validate source exists
        if not source:
            errors.append(
                f"Relationship '{rel_id}': missing source  [{src_file}]"
            )
        elif source not in all_ids:
            errors.append(
                f"Relationship '{rel_id}': dangling source '{source}'  [{src_file}]"
            )

        # Validate target exists
        if not target:
            errors.append(
                f"Relationship '{rel_id}': missing target  [{src_file}]"
            )
        elif target not in all_ids:
            errors.append(
                f"Relationship '{rel_id}': dangling target '{target}'  [{src_file}]"
            )

        # No self-referencing
        if source and target and source == target:
            errors.append(
                f"Relationship '{rel_id}': self-referencing "
                f"(source == target == '{source}')  [{src_file}]"
            )

    # ---- Validate artifact intent pattern_refs ----
    for art in artifact_intents:
        art_id = art.get("id", "UNKNOWN")
        src_file = art.get("_source_file", "<unknown>")
        pattern_refs = art.get("pattern_refs", []) or art.get("applicable_patterns", [])
        if pattern_refs is None:
            pattern_refs = []
        for ref in pattern_refs:
            ref_id = extract_ref_id(ref)
            if ref_id and ref_id not in all_ids:
                errors.append(
                    f"ArtifactIntent '{art_id}': dangling pattern_refs reference '{ref_id}'  [{src_file}]"
                )

    # ---- Validate constraint profile applies_to references ----
    for cns in constraint_profiles:
        cns_id = cns.get("id", "UNKNOWN")
        src_file = cns.get("_source_file", "<unknown>")
        applies_to = cns.get("applies_to", []) or cns.get("applicable_patterns", [])
        if applies_to is None:
            applies_to = []
        for ref in applies_to:
            ref_id = extract_ref_id(ref)
            if ref_id and ref_id not in all_ids:
                errors.append(
                    f"ConstraintProfile '{cns_id}': dangling applies_to reference '{ref_id}'  [{src_file}]"
                )

    # ---- Check for duplicate relationship IDs ----
    seen_rel_ids: Dict[str, str] = {}
    for rel in relationships:
        rid = rel.get("id", "")
        src_file = rel.get("_source_file", "<unknown>")
        if rid in seen_rel_ids:
            errors.append(
                f"Duplicate relationship ID '{rid}' in [{src_file}] "
                f"(first seen in [{seen_rel_ids[rid]}])"
            )
        else:
            seen_rel_ids[rid] = src_file

    # ---- Dependency acyclicity (DAG check) ----
    cycle_errors = detect_dependency_cycles(relationships)
    errors.extend(cycle_errors)

    # ---- Adjacency cycles are allowed ----
    # Adjacency relationships are permitted to form cycles (bidirectional
    # adjacency is architecturally valid — A adjacent to B and B adjacent to A).
    # No validation error is raised for adjacency cycles.

    # ---- Conflict symmetry ----
    symmetry_errors = check_conflict_symmetry(relationships)
    errors.extend(symmetry_errors)

    # ---- Schema/version compatibility ----
    all_pattern_records = []
    pattern_lang_dir = os.path.join(root_dir, "pattern_language")
    for filepath in gather_files_from(pattern_lang_dir):
        all_pattern_records.extend(extract_records(filepath))
    version_errors = check_schema_version_compatibility(
        relationships, artifact_intents, constraint_profiles, all_pattern_records
    )
    errors.extend(version_errors)

    # ---- Deprecation/index integrity ----
    dep_errors = check_deprecation_integrity(all_ids, root_dir)
    errors.extend(dep_errors)

    # ---- Report ----
    print("Graph Validation Report")
    print("=" * 60)
    print(f"Total entity IDs:       {len(all_ids)}")
    print(f"Relationships found:    {len(relationships)}")
    print(f"Artifact intents found: {len(artifact_intents)}")
    print(f"Constraint profiles:    {len(constraint_profiles)}")
    print(f"Checks performed:")
    print(f"  - Reference integrity (source/target/applies_to)")
    print(f"  - Relationship type validation")
    print(f"  - Self-reference detection")
    print(f"  - Duplicate ID detection")
    print(f"  - Dependency acyclicity (DAG)")
    print(f"  - Adjacency cycles (allowed)")
    print(f"  - Conflict symmetry")
    print(f"  - Schema/version compatibility")
    print(f"  - Deprecation/index integrity")
    print(f"Errors:                 {len(errors)}")

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
    success = validate_graph(repo_root)
    sys.exit(0 if success else 1)
