#!/usr/bin/env python3
"""
Wave 13A Acceptance Tests — Detail DNA Taxonomy + Resolution Contracts

Validates:
1. All detail families have canonical IDs matching the [SYS]-[CLASS]-[COND]-[VAR]-[ASM]-[NN] format
2. Schema validates all records
3. Tag index resolves correctly
4. Route graph contains no circular dependencies
5. Training subsystem remains read-only (structural check)
"""

import json
import os
import re
import sys
from pathlib import Path
from collections import defaultdict

KERNEL_ROOT = Path(__file__).parent.parent
DETAIL_DNA_DIR = KERNEL_ROOT / "data" / "detail_dna"
SCHEMA_PATH = KERNEL_ROOT / "schemas" / "detail_dna_schema.json"
TAGS_PATH = KERNEL_ROOT / "data" / "detail_tags.json"
TAG_INDEX_PATH = KERNEL_ROOT / "data" / "detail_tag_index.json"
ROUTE_INDEX_PATH = KERNEL_ROOT / "data" / "detail_route_index.json"
RELATIONSHIP_SCHEMA_PATH = KERNEL_ROOT / "schemas" / "detail_relationship_schema.json"
TRAINING_DIR = KERNEL_ROOT / "detail_training_corpus"
TRAINING_PAIRS_PATH = TRAINING_DIR / "training_pairs.jsonl"

CANONICAL_ID_PATTERN = re.compile(r"^[A-Z_]+-[A-Z_]+-[A-Z_]+-[A-Z_]+-[A-Z_]+-[0-9]{2}$")

# Load schema enums for validation
VALID_SYSTEMS = ["LOW_SLOPE", "STEEP_SLOPE", "BELOW_GRADE", "PLAZA_DECK", "AIR_BARRIER", "FACADE", "JOINT_PROTECTION"]
VALID_CLASSES = ["TERMINATION", "EDGE", "PENETRATION", "TRANSITION", "DRAINAGE", "JOINT", "OPENING", "ANCHORAGE"]
VALID_CONDITIONS = ["PARAPET", "VERTICAL_WALL", "CURB", "PIPE", "DRAIN", "SCUPPER", "EXPANSION_JOINT", "THRESHOLD", "INSIDE_CORNER", "OUTSIDE_CORNER", "ROOF_TO_WALL", "ROOF_TO_EDGE"]
VALID_VARIANTS = ["REGLET", "COUNTERFLASHING", "COPING", "TERMINATION_BAR", "PITCH_POCKET", "PIPE_BOOT", "METAL_EDGE", "SELF_ADHERED", "LIQUID_APPLIED"]
VALID_ASSEMBLY_FAMILIES = ["EPDM", "TPO", "PVC", "SBS", "BUR", "PMR", "AIR_BARRIER_SA", "AIR_BARRIER_FLUID"]
VALID_MATERIAL_CLASSES = ["SBS", "APP", "TPO", "PVC", "EPDM", "KEE", "HDPE", "LDPE", "PIB", "PU", "Acrylic", "Silicone", "Bitumen", "PMMA", "Epoxy", "Hybrid"]

ACYCLIC_TYPES = {"depends_on", "precedes", "blocks", "follows"}

errors = []
warnings = []


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def test_detail_families_have_canonical_ids():
    """TEST 1: All detail families have canonical IDs."""
    print("TEST 1: Canonical ID validation...")
    families = list(DETAIL_DNA_DIR.glob("*.json"))
    assert len(families) > 0, "No detail family files found"

    for family_path in families:
        family = load_json(family_path)
        detail_id = family.get("detail_id", "")

        if not CANONICAL_ID_PATTERN.match(detail_id):
            errors.append(f"  FAIL: {family_path.name} has invalid canonical ID: {detail_id}")
        else:
            # Verify ID components match field values
            parts = detail_id.split("-")
            # The ID has 6 segments but system/class/condition/variant/assembly could have underscores
            # Re-parse using the known field values
            expected_id = f"{family['system']}-{family['class']}-{family['condition']}-{family['variant']}-{family['assembly_family']}-{parts[-1]}"
            if detail_id != expected_id:
                errors.append(f"  FAIL: {family_path.name} ID {detail_id} does not match fields (expected {expected_id})")

        # Verify filename matches detail_id
        expected_filename = f"{detail_id}.json"
        if family_path.name != expected_filename:
            errors.append(f"  FAIL: Filename {family_path.name} does not match detail_id {detail_id}")

    print(f"  Found {len(families)} detail families")


def test_schema_validates_all_records():
    """TEST 2: Schema validates all records."""
    print("TEST 2: Schema validation...")
    schema = load_json(SCHEMA_PATH)
    required_fields = schema.get("required", [])
    families = list(DETAIL_DNA_DIR.glob("*.json"))

    for family_path in families:
        family = load_json(family_path)

        # Check required fields
        for field in required_fields:
            if field not in family:
                errors.append(f"  FAIL: {family_path.name} missing required field: {field}")

        # Check enum values
        if family.get("system") not in VALID_SYSTEMS:
            errors.append(f"  FAIL: {family_path.name} has invalid system: {family.get('system')}")
        if family.get("class") not in VALID_CLASSES:
            errors.append(f"  FAIL: {family_path.name} has invalid class: {family.get('class')}")
        if family.get("condition") not in VALID_CONDITIONS:
            errors.append(f"  FAIL: {family_path.name} has invalid condition: {family.get('condition')}")
        if family.get("variant") not in VALID_VARIANTS:
            errors.append(f"  FAIL: {family_path.name} has invalid variant: {family.get('variant')}")
        if family.get("assembly_family") not in VALID_ASSEMBLY_FAMILIES:
            errors.append(f"  FAIL: {family_path.name} has invalid assembly_family: {family.get('assembly_family')}")

        # Check material classes
        for mat in family.get("compatible_material_classes", []):
            if mat not in VALID_MATERIAL_CLASSES:
                errors.append(f"  FAIL: {family_path.name} has invalid material class: {mat}")

        # Check tags are non-empty
        if len(family.get("tags", [])) == 0:
            errors.append(f"  FAIL: {family_path.name} has no tags")

        # Check synonyms is a list
        if not isinstance(family.get("synonyms", []), list):
            errors.append(f"  FAIL: {family_path.name} synonyms is not a list")


def test_tag_index_resolves_correctly():
    """TEST 3: Tag index resolves correctly."""
    print("TEST 3: Tag index validation...")
    tag_index = load_json(TAG_INDEX_PATH)["tag_index"]
    tags_def = load_json(TAGS_PATH)

    # Build set of all valid tag_ids
    valid_tags = set()
    for group in tags_def["tag_groups"].values():
        for tag in group["tags"]:
            valid_tags.add(tag["tag_id"])

    # Build set of all detail IDs
    families = list(DETAIL_DNA_DIR.glob("*.json"))
    all_detail_ids = set()
    detail_tags_map = {}
    for family_path in families:
        family = load_json(family_path)
        did = family["detail_id"]
        all_detail_ids.add(did)
        detail_tags_map[did] = set(family.get("tags", []))

    # Validate tag index entries reference valid tags and valid detail IDs
    for tag, detail_ids in tag_index.items():
        if tag not in valid_tags:
            errors.append(f"  FAIL: Tag index contains unknown tag: {tag}")
        for did in detail_ids:
            if did not in all_detail_ids:
                errors.append(f"  FAIL: Tag index references unknown detail_id: {did} under tag {tag}")

    # Validate that every tag on every detail family appears in the index
    for did, tags in detail_tags_map.items():
        for tag in tags:
            if tag in tag_index:
                if did not in tag_index[tag]:
                    errors.append(f"  FAIL: Detail {did} has tag {tag} but is not in tag_index[{tag}]")
            else:
                # Tag might be valid but not indexed (if no details use it) — only error if detail uses it
                if tag in valid_tags:
                    errors.append(f"  FAIL: Tag {tag} used by {did} has no entry in tag_index")

    print(f"  Validated {len(tag_index)} tag entries against {len(all_detail_ids)} detail families")


def test_route_graph_no_cycles():
    """TEST 4: Route graph contains no circular dependencies."""
    print("TEST 4: Route graph cycle detection...")
    route_data = load_json(ROUTE_INDEX_PATH)
    routes = route_data.get("routes", [])

    # Build adjacency lists for acyclic relationship types
    for rel_type in ACYCLIC_TYPES:
        graph = defaultdict(list)
        nodes = set()
        for route in routes:
            if route["relationship_type"] == rel_type:
                src = route["source_detail_id"]
                tgt = route["target_detail_id"]
                graph[src].append(tgt)
                nodes.add(src)
                nodes.add(tgt)

        if not nodes:
            continue

        # DFS cycle detection
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {n: WHITE for n in nodes}

        def dfs(node):
            color[node] = GRAY
            for neighbor in graph.get(node, []):
                if neighbor not in color:
                    color[neighbor] = WHITE
                if color[neighbor] == GRAY:
                    return True  # Cycle found
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[node] = BLACK
            return False

        has_cycle = False
        for node in nodes:
            if color[node] == WHITE:
                if dfs(node):
                    has_cycle = True
                    break

        if has_cycle:
            errors.append(f"  FAIL: Cycle detected in '{rel_type}' relationships")
        else:
            print(f"  '{rel_type}' — DAG validated (no cycles)")

    # Validate all referenced detail IDs exist
    families = list(DETAIL_DNA_DIR.glob("*.json"))
    all_detail_ids = set()
    for family_path in families:
        family = load_json(family_path)
        all_detail_ids.add(family["detail_id"])

    for route in routes:
        if route["source_detail_id"] not in all_detail_ids:
            errors.append(f"  FAIL: Route references unknown source: {route['source_detail_id']}")
        if route["target_detail_id"] not in all_detail_ids:
            errors.append(f"  FAIL: Route references unknown target: {route['target_detail_id']}")

    # Validate no self-references
    for route in routes:
        if route["source_detail_id"] == route["target_detail_id"]:
            errors.append(f"  FAIL: Self-referencing route: {route['source_detail_id']}")

    print(f"  Validated {len(routes)} routes")


def test_training_subsystem_readonly():
    """TEST 5: Training subsystem remains read-only."""
    print("TEST 5: Training subsystem isolation...")

    # Verify training directory exists
    assert TRAINING_DIR.exists(), "Training corpus directory does not exist"

    # Verify training_pairs.jsonl exists and is valid JSONL
    assert TRAINING_PAIRS_PATH.exists(), "training_pairs.jsonl does not exist"

    with open(TRAINING_PAIRS_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"  FAIL: training_pairs.jsonl line {i+1} is not valid JSON")
            continue

        # Verify structure
        if "input" not in record:
            errors.append(f"  FAIL: training_pairs.jsonl line {i+1} missing 'input'")
        if "output" not in record:
            errors.append(f"  FAIL: training_pairs.jsonl line {i+1} missing 'output'")
        if "metadata" not in record:
            errors.append(f"  FAIL: training_pairs.jsonl line {i+1} missing 'metadata'")

        # Verify metadata source is Construction_Kernel (read-only proof)
        meta = record.get("metadata", {})
        if meta.get("source") != "Construction_Kernel":
            errors.append(f"  FAIL: training_pairs.jsonl line {i+1} source is not Construction_Kernel")

    # Verify no kernel data files exist inside training corpus
    kernel_artifacts = list(TRAINING_DIR.glob("**/detail_dna_schema.json")) + \
                       list(TRAINING_DIR.glob("**/detail_tags.json")) + \
                       list(TRAINING_DIR.glob("**/detail_route_index.json"))
    if kernel_artifacts:
        errors.append(f"  FAIL: Training corpus contains kernel artifacts: {kernel_artifacts}")

    print(f"  Validated {len(lines)} training pairs")


def main():
    print("=" * 60)
    print("WAVE 13A ACCEPTANCE TESTS")
    print("Detail DNA Taxonomy + Resolution Contracts")
    print("=" * 60)
    print()

    test_detail_families_have_canonical_ids()
    test_schema_validates_all_records()
    test_tag_index_resolves_correctly()
    test_route_graph_no_cycles()
    test_training_subsystem_readonly()

    print()
    print("=" * 60)

    if warnings:
        print(f"WARNINGS: {len(warnings)}")
        for w in warnings:
            print(w)

    if errors:
        print(f"FAILURES: {len(errors)}")
        for e in errors:
            print(e)
        print()
        print("WAVE 13A: FAILED")
        sys.exit(1)
    else:
        print("WAVE 13A: ALL ACCEPTANCE TESTS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
