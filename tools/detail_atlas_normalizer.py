#!/usr/bin/env python3
"""
Detail Atlas Semantic Normalizer

Converts fast_brain/main/cad_processor.py raw DXF JSON output into canonical
Assembly Kernel JSON for automatic manufacturer detail ingestion.

Input:  cad_processor output (spatial + quantity + specs + full lenses)
Output: Assembly Kernel JSON conforming to 10-Construction_OS assembly schema

Authority: 10-Construction_OS (domain plane)
Design: fail-closed, deterministic, config-driven, no network calls
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Deterministic ID generation
# ---------------------------------------------------------------------------

def generate_assembly_id(manufacturer_id: str, condition_type: str, source_filename: str) -> str:
    """Generate deterministic assembly_id from stable inputs."""
    seed = f"{manufacturer_id}|{condition_type}|{source_filename}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    return f"{manufacturer_id}_{condition_type}_{digest}"


def generate_node_id(assembly_id: str, index: int = 1) -> str:
    """Generate deterministic node_id from assembly_id."""
    seed = f"{assembly_id}|node|{index}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8]
    return f"{assembly_id}_node_{digest}"


# ---------------------------------------------------------------------------
# Lens merging
# ---------------------------------------------------------------------------

def merge_lenses(cad_output: dict) -> dict:
    """Merge spatial, quantity, specs, and full lenses into unified view.

    Accepts either a dict keyed by lens name or a single-lens dict with
    a 'format' field.
    """
    merged = {
        "meta": {},
        "layers": [],
        "geometry": [],
        "linear_feet_by_layer": {},
        "total_linear_feet": 0.0,
        "block_counts": {},
        "entity_counts_by_layer": {},
        "notes": [],
        "dimensions": [],
        "leaders": [],
        "entities": [],
    }

    # Detect single-lens input
    if "format" in cad_output:
        cad_output = {cad_output["format"].lower(): cad_output}

    for lens_name in ("spatial", "quantity", "specs", "full"):
        lens = cad_output.get(lens_name, {})
        if not lens:
            continue

        # Meta comes from any lens (they share structure)
        if lens.get("meta") and not merged["meta"]:
            merged["meta"] = lens["meta"]

        if lens_name == "spatial":
            merged["geometry"] = lens.get("geometry", [])
            merged["layers"] = lens.get("layers_with_geometry", [])

        elif lens_name == "quantity":
            merged["linear_feet_by_layer"] = lens.get("linear_feet_by_layer", {})
            merged["total_linear_feet"] = lens.get("total_linear_feet", 0.0)
            merged["block_counts"] = lens.get("block_counts", {})
            merged["entity_counts_by_layer"] = lens.get("entity_counts_by_layer", {})

        elif lens_name == "specs":
            merged["notes"] = lens.get("notes", [])
            merged["dimensions"] = lens.get("dimensions", [])
            merged["leaders"] = lens.get("leaders", [])

        elif lens_name == "full":
            merged["entities"] = lens.get("entities", [])

    # Also pull layers from meta if not yet populated
    if not merged["layers"] and merged["meta"].get("layers"):
        merged["layers"] = merged["meta"]["layers"]

    return merged


# ---------------------------------------------------------------------------
# Layer → system mapping
# ---------------------------------------------------------------------------

def resolve_layers_to_systems(layers: list, layer_map: dict) -> list:
    """Map DXF layer names to construction system types."""
    systems = set()
    for layer in layers:
        normalized = layer.upper().strip()
        for key, system in layer_map.items():
            if key.upper() in normalized:
                systems.add(system)
    return sorted(systems)


# ---------------------------------------------------------------------------
# Block → component normalization
# ---------------------------------------------------------------------------

def resolve_blocks_to_components(block_counts: dict, block_map: dict) -> list:
    """Map DXF block names to assembly components."""
    components = []
    seen_ids = set()
    for block_name, count in block_counts.items():
        normalized = block_name.upper().strip()
        for key, component_template in block_map.items():
            if key.upper() in normalized and component_template["component_id"] not in seen_ids:
                component = dict(component_template)
                component["source_block"] = block_name
                component["block_count"] = count
                seen_ids.add(component["component_id"])
                components.append(component)
    return components


# ---------------------------------------------------------------------------
# Regex extraction: manufacturer & system
# ---------------------------------------------------------------------------

def extract_all_text(merged: dict) -> str:
    """Gather all text content from notes, leaders, and full entities."""
    texts = []
    for note in merged.get("notes", []):
        texts.append(note.get("text", ""))
    for leader in merged.get("leaders", []):
        texts.append(leader.get("annotation", "") or "")
    for entity in merged.get("entities", []):
        if entity.get("type") in ("TEXT", "MTEXT"):
            texts.append(entity.get("content", ""))
    return " ".join(texts)


def resolve_manufacturer(all_text: str, regex_rules: list) -> dict | None:
    """Extract manufacturer from text via regex rules. Returns first match."""
    for rule in regex_rules:
        if re.search(rule["pattern"], all_text):
            return {
                "manufacturer_id": rule["manufacturer_id"],
                "manufacturer_name": rule["manufacturer_name"],
            }
    return None


def resolve_system(all_text: str, regex_rules: list, layer_systems: list) -> str | None:
    """Extract roofing system type from text or layer-derived systems."""
    for rule in regex_rules:
        if re.search(rule["pattern"], all_text):
            return rule["system_type"]
    # Fall back to layer-derived systems
    if layer_systems:
        return layer_systems[0]
    return None


# ---------------------------------------------------------------------------
# Condition classification
# ---------------------------------------------------------------------------

def classify_condition(
    all_text: str,
    layers: list,
    block_counts: dict,
    heuristics: list,
) -> str | None:
    """Rule-based condition classification using heuristics config."""
    text_lower = all_text.lower()
    layers_upper = [l.upper() for l in layers]
    blocks_upper = [b.upper() for b in block_counts.keys()]

    best_match = None
    best_score = 0

    for heuristic in heuristics:
        score = 0
        # Check text indicators
        matched_indicators = 0
        for indicator in heuristic["required_indicators"]:
            if indicator.lower() in text_lower:
                matched_indicators += 1
        if matched_indicators >= heuristic.get("min_match", 1):
            score += matched_indicators * 2

        # Check layer hints
        for hint in heuristic.get("layer_hints", []):
            for layer in layers_upper:
                if hint.upper() in layer:
                    score += 1

        # Check block hints
        for hint in heuristic.get("block_hints", []):
            for block in blocks_upper:
                if hint.upper() in block:
                    score += 1

        if score > best_score:
            best_score = score
            best_match = heuristic["condition_type"]

    return best_match if best_score > 0 else None


# ---------------------------------------------------------------------------
# Assembly constraints from config
# ---------------------------------------------------------------------------

def build_assembly_constraints(condition_type: str, config: dict) -> list:
    """Get default assembly constraints for the condition type."""
    defaults = config.get("default_assembly_constraints", {})
    return defaults.get(condition_type, [])


# ---------------------------------------------------------------------------
# Template path assignment
# ---------------------------------------------------------------------------

def assign_template_path(condition_type: str, config: dict) -> str | None:
    """Lookup template path for condition type."""
    lookup = config.get("template_lookup", {})
    return lookup.get(condition_type)


# ---------------------------------------------------------------------------
# Fail-closed validation
# ---------------------------------------------------------------------------

class NormalizationError(Exception):
    """Raised when fail-closed conditions are triggered."""
    pass


def validate_fail_closed(
    manufacturer: dict | None,
    system_type: str | None,
    condition_type: str | None,
    components: list,
    merged: dict,
) -> list:
    """Validate all fail-closed conditions. Returns list of errors."""
    errors = []

    if manufacturer is None:
        errors.append("FAIL_CLOSED: manufacturer unresolved — no regex match in text content")

    if system_type is None:
        errors.append("FAIL_CLOSED: system unresolved — no system type identified from text or layers")

    if condition_type is None:
        errors.append("FAIL_CLOSED: condition ambiguous — no condition heuristic matched")

    # Check for component mapping conflicts (duplicate component_ids)
    comp_ids = [c["component_id"] for c in components]
    if len(comp_ids) != len(set(comp_ids)):
        errors.append("FAIL_CLOSED: component mapping conflict — duplicate component_ids detected")

    # Check schema minimum: must have meta
    if not merged.get("meta"):
        errors.append("FAIL_CLOSED: schema mismatch — no meta block in cad_processor output")

    return errors


# ---------------------------------------------------------------------------
# Core normalizer
# ---------------------------------------------------------------------------

def normalize(cad_output: dict, config: dict) -> dict:
    """Normalize cad_processor output into Assembly Kernel JSON.

    Args:
        cad_output: Raw output from cad_processor.py (all lenses)
        config: Detail Atlas mapping configuration

    Returns:
        Canonical Assembly Kernel JSON dict

    Raises:
        NormalizationError: On any fail-closed condition
    """
    # Step 1: Merge lenses
    merged = merge_lenses(cad_output)

    # Step 2: Extract all text
    all_text = extract_all_text(merged)

    # Step 3: Layer → system mapping
    layer_systems = resolve_layers_to_systems(
        merged["layers"], config.get("layer_to_system", {})
    )

    # Step 4: Block → component normalization
    components = resolve_blocks_to_components(
        merged["block_counts"], config.get("block_to_component", {})
    )

    # Step 5: Manufacturer extraction
    manufacturer = resolve_manufacturer(
        all_text, config.get("text_regex_to_manufacturer", [])
    )

    # Step 6: System extraction
    system_type = resolve_system(
        all_text, config.get("text_regex_to_system", []), layer_systems
    )

    # Step 7: Condition classification
    condition_type = classify_condition(
        all_text, merged["layers"], merged["block_counts"],
        config.get("condition_heuristics", [])
    )

    # Step 8: Fail-closed validation
    errors = validate_fail_closed(
        manufacturer, system_type, condition_type, components, merged
    )
    if errors:
        raise NormalizationError("\n".join(errors))

    # Step 9: Deterministic IDs
    source_filename = merged["meta"].get("filename", "unknown")
    assembly_id = generate_assembly_id(
        manufacturer["manufacturer_id"], condition_type, source_filename
    )
    node_id = generate_node_id(assembly_id)

    # Step 10: Assembly constraints
    assembly_constraints = build_assembly_constraints(condition_type, config)

    # Step 11: Template path
    template_path = assign_template_path(condition_type, config)

    # Step 12: Build canonical output
    assembly_kernel = {
        "assembly_id": assembly_id,
        "assembly_version": "1.0.0",
        "node_id": node_id,
        "manufacturer_id": manufacturer["manufacturer_id"],
        "manufacturer_name": manufacturer["manufacturer_name"],
        "condition_type": condition_type,
        "system_type": system_type,
        "components": components,
        "assembly_constraints": assembly_constraints,
        "template_path": template_path,
        "source_quantities": {
            "linear_feet_by_layer": merged["linear_feet_by_layer"],
            "total_linear_feet": merged["total_linear_feet"],
            "block_counts": merged["block_counts"],
        },
        "source_dimensions": [
            {
                "value_raw": d.get("value_raw"),
                "value_feet": d.get("value_feet"),
                "override_text": d.get("override_text"),
                "layer": d.get("layer"),
            }
            for d in merged.get("dimensions", [])
        ],
        "lineage": {
            "source_authority": "10-Construction_OS",
            "source_file": source_filename,
            "source_format": "cad_processor.dxf_json",
            "normalizer": "detail_atlas_normalizer",
            "normalizer_version": "1.0.0",
            "config_id": config.get("mapping_id", "unknown"),
            "config_version": config.get("mapping_version", "unknown"),
            "created": datetime.now(timezone.utc).isoformat(),
            "created_by": "detail_atlas_normalizer",
            "governance_kernel": "00-validkernel-governance",
            "truth_kernel": "00-Universal_Truth_Kernel",
        },
        "artifacts_enabled": {
            "detail_packet": True,
            "compliance_certificate": True,
            "svg_overlay": template_path is not None,
            "system_passport": True,
        },
    }

    return assembly_kernel


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def load_json(path: str) -> dict:
    """Load JSON from file path."""
    with open(path, "r") as f:
        return json.load(f)


def main():
    """CLI entry point for normalizer."""
    if len(sys.argv) < 3:
        print("Usage: python detail_atlas_normalizer.py <cad_json> <config_json> [output_json]")
        print("  cad_json:    path to cad_processor output (all lenses)")
        print("  config_json: path to detail atlas mapping config")
        print("  output_json: optional output path (default: stdout)")
        sys.exit(1)

    cad_path = sys.argv[1]
    config_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) >= 4 else None

    cad_output = load_json(cad_path)
    config = load_json(config_path)

    try:
        result = normalize(cad_output, config)
    except NormalizationError as e:
        print(f"NORMALIZATION FAILED (fail-closed):\n{e}", file=sys.stderr)
        sys.exit(1)

    output = json.dumps(result, indent=2)

    if output_path:
        with open(output_path, "w") as f:
            f.write(output)
            f.write("\n")
        print(f"Assembly Kernel JSON written to: {output_path}")
    else:
        print(output)


if __name__ == "__main__":
    main()
