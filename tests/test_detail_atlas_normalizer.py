#!/usr/bin/env python3
"""
Tests for Detail Atlas Semantic Normalizer

Validates:
- Barrett parapet fixture normalization
- Roof drain fixture normalization
- Ambiguous input fail-closed behavior
- Deterministic ID generation
- Canonical JSON structure
- Lineage preservation
"""

import json
import sys
import unittest
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from detail_atlas_normalizer import (
    NormalizationError,
    classify_condition,
    extract_all_text,
    generate_assembly_id,
    generate_node_id,
    merge_lenses,
    normalize,
    resolve_blocks_to_components,
    resolve_layers_to_systems,
    resolve_manufacturer,
    resolve_system,
    validate_fail_closed,
)

# ---------------------------------------------------------------------------
# Shared test config (Barrett)
# ---------------------------------------------------------------------------
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "detail_atlas_mapping.barrett.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

def make_barrett_parapet_cad_output():
    """Simulated cad_processor output for Barrett parapet detail."""
    return {
        "spatial": {
            "format": "SPATIAL",
            "purpose": "Geometry analysis for spatial AI (The Eyes)",
            "meta": {
                "filename": "barrett_parapet_detail_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["PARAPET", "FLASHING", "ROOF", "METAL", "INSULATION"]
            },
            "geometry": [
                {"type": "LWPOLYLINE", "layer": "PARAPET", "bounds": {"min_x": 0, "min_y": 0, "max_x": 24, "max_y": 36}, "closed": True},
                {"type": "LINE", "layer": "FLASHING", "bounds": {"min_x": 0, "min_y": 0, "max_x": 24, "max_y": 18}, "closed": False},
            ],
            "layers_with_geometry": ["PARAPET", "FLASHING", "ROOF", "METAL", "INSULATION"],
            "geometry_count": 2
        },
        "quantity": {
            "format": "QUANTITY",
            "purpose": "Quantity takeoff for estimation AI (The Estimator)",
            "meta": {
                "filename": "barrett_parapet_detail_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["PARAPET", "FLASHING", "ROOF", "METAL", "INSULATION"]
            },
            "linear_feet_by_layer": {
                "PARAPET": 12.5,
                "FLASHING": 8.3,
                "ROOF": 45.2,
                "METAL": 6.0,
                "INSULATION": 3.5
            },
            "total_linear_feet": 75.5,
            "block_counts": {
                "CANT_STRIP": 2,
                "TERM_BAR": 1,
                "COPING": 1
            },
            "entity_counts_by_layer": {
                "PARAPET": {"LWPOLYLINE": 3, "LINE": 5},
                "FLASHING": {"LINE": 8}
            }
        },
        "specs": {
            "format": "SPECS",
            "purpose": "Specification extraction for detail AI (The Detailer)",
            "meta": {
                "filename": "barrett_parapet_detail_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["PARAPET", "FLASHING", "ROOF", "METAL", "INSULATION"]
            },
            "notes": [
                {"layer": "PARAPET", "text": "BARRETT SBS MODIFIED BITUMEN PARAPET TERMINATION", "location": [12.0, 30.0], "height": 0.125},
                {"layer": "FLASHING", "text": "MIN 8\" FLASHING HEIGHT", "location": [5.0, 15.0], "height": 0.1},
                {"layer": "METAL", "text": "24 GA PREFINISHED METAL COPING", "location": [12.0, 36.0], "height": 0.1}
            ],
            "dimensions": [
                {"layer": "FLASHING", "value_raw": 8.0, "value_feet": 0.6667, "override_text": "8\""},
                {"layer": "PARAPET", "value_raw": 36.0, "value_feet": 3.0, "override_text": "3'-0\""}
            ],
            "leaders": [
                {"layer": "PARAPET", "annotation": "TERMINATION BAR W/ SEALANT"}
            ],
            "note_count": 3,
            "dimension_count": 2
        },
        "full": {
            "format": "FULL",
            "purpose": "Complete DXF data extraction",
            "meta": {
                "filename": "barrett_parapet_detail_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["PARAPET", "FLASHING", "ROOF", "METAL", "INSULATION"]
            },
            "entities": [
                {"type": "TEXT", "layer": "PARAPET", "content": "BARRETT SBS MODIFIED BITUMEN PARAPET TERMINATION", "location": [12.0, 30.0], "color": 7},
                {"type": "TEXT", "layer": "FLASHING", "content": "MIN 8\" FLASHING HEIGHT", "location": [5.0, 15.0], "color": 1},
                {"type": "INSERT", "layer": "PARAPET", "block_name": "CANT_STRIP", "location": [6.0, 4.0], "scale": [1.0, 1.0], "rotation": 0.0, "color": None},
                {"type": "INSERT", "layer": "PARAPET", "block_name": "TERM_BAR", "location": [6.0, 18.0], "scale": [1.0, 1.0], "rotation": 0.0, "color": None},
                {"type": "LINE", "layer": "FLASHING", "start": [0.0, 0.0], "end": [0.0, 18.0], "length_raw": 18.0, "length_feet": 1.5, "color": 1}
            ],
            "entity_count": 5
        }
    }


def make_roof_drain_cad_output():
    """Simulated cad_processor output for roof drain detail."""
    return {
        "spatial": {
            "format": "SPATIAL",
            "meta": {
                "filename": "barrett_roof_drain_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["DRAINAGE", "ROOF", "PLUMBING"]
            },
            "geometry": [
                {"type": "CIRCLE", "layer": "DRAINAGE", "bounds": {"min_x": -6, "min_y": -6, "max_x": 6, "max_y": 6}, "closed": True}
            ],
            "layers_with_geometry": ["DRAINAGE", "ROOF", "PLUMBING"],
            "geometry_count": 1
        },
        "quantity": {
            "format": "QUANTITY",
            "meta": {
                "filename": "barrett_roof_drain_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["DRAINAGE", "ROOF", "PLUMBING"]
            },
            "linear_feet_by_layer": {"DRAINAGE": 3.14, "ROOF": 20.0},
            "total_linear_feet": 23.14,
            "block_counts": {"ROOF_DRAIN": 1},
            "entity_counts_by_layer": {"DRAINAGE": {"CIRCLE": 1}}
        },
        "specs": {
            "format": "SPECS",
            "meta": {
                "filename": "barrett_roof_drain_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["DRAINAGE", "ROOF", "PLUMBING"]
            },
            "notes": [
                {"layer": "DRAINAGE", "text": "BARRETT ROOF DRAIN DETAIL", "location": [0.0, 10.0], "height": 0.125},
                {"layer": "DRAINAGE", "text": "SBS FLASHING COLLAR", "location": [0.0, -10.0], "height": 0.1}
            ],
            "dimensions": [],
            "leaders": [],
            "note_count": 2,
            "dimension_count": 0
        },
        "full": {
            "format": "FULL",
            "meta": {
                "filename": "barrett_roof_drain_001.dxf",
                "units": "Inches",
                "units_code": 1,
                "conversion_to_feet": 0.08333333,
                "layers": ["DRAINAGE", "ROOF", "PLUMBING"]
            },
            "entities": [
                {"type": "TEXT", "layer": "DRAINAGE", "content": "BARRETT ROOF DRAIN DETAIL", "location": [0.0, 10.0], "color": 7},
                {"type": "TEXT", "layer": "DRAINAGE", "content": "SBS FLASHING COLLAR", "location": [0.0, -10.0], "color": 1},
                {"type": "INSERT", "layer": "DRAINAGE", "block_name": "ROOF_DRAIN", "location": [0.0, 0.0], "scale": [1.0, 1.0], "rotation": 0.0, "color": None}
            ],
            "entity_count": 3
        }
    }


def make_ambiguous_cad_output():
    """Simulated cad_processor output with no identifiable manufacturer or condition."""
    return {
        "spatial": {
            "format": "SPATIAL",
            "meta": {
                "filename": "unknown_detail.dxf",
                "units": "Feet",
                "units_code": 2,
                "conversion_to_feet": 1.0,
                "layers": ["LAYER1", "LAYER2"]
            },
            "geometry": [],
            "layers_with_geometry": ["LAYER1", "LAYER2"],
            "geometry_count": 0
        },
        "quantity": {
            "format": "QUANTITY",
            "meta": {
                "filename": "unknown_detail.dxf",
                "units": "Feet",
                "units_code": 2,
                "conversion_to_feet": 1.0,
                "layers": ["LAYER1", "LAYER2"]
            },
            "linear_feet_by_layer": {},
            "total_linear_feet": 0.0,
            "block_counts": {},
            "entity_counts_by_layer": {}
        },
        "specs": {
            "format": "SPECS",
            "meta": {
                "filename": "unknown_detail.dxf",
                "units": "Feet",
                "units_code": 2,
                "conversion_to_feet": 1.0,
                "layers": ["LAYER1", "LAYER2"]
            },
            "notes": [
                {"layer": "LAYER1", "text": "GENERAL NOTE", "location": [0.0, 0.0], "height": 0.1}
            ],
            "dimensions": [],
            "leaders": [],
            "note_count": 1,
            "dimension_count": 0
        },
        "full": {
            "format": "FULL",
            "meta": {
                "filename": "unknown_detail.dxf",
                "units": "Feet",
                "units_code": 2,
                "conversion_to_feet": 1.0,
                "layers": ["LAYER1", "LAYER2"]
            },
            "entities": [
                {"type": "TEXT", "layer": "LAYER1", "content": "GENERAL NOTE", "location": [0.0, 0.0], "color": 7}
            ],
            "entity_count": 1
        }
    }


# ===========================================================================
# Test Cases
# ===========================================================================

class TestDeterministicIDs(unittest.TestCase):
    """Verify deterministic ID generation produces stable, reproducible IDs."""

    def test_assembly_id_deterministic(self):
        id1 = generate_assembly_id("barrett", "parapet_termination", "test.dxf")
        id2 = generate_assembly_id("barrett", "parapet_termination", "test.dxf")
        self.assertEqual(id1, id2)

    def test_assembly_id_varies_with_input(self):
        id1 = generate_assembly_id("barrett", "parapet_termination", "test.dxf")
        id2 = generate_assembly_id("barrett", "roof_drain", "test.dxf")
        self.assertNotEqual(id1, id2)

    def test_node_id_deterministic(self):
        node1 = generate_node_id("assembly_abc")
        node2 = generate_node_id("assembly_abc")
        self.assertEqual(node1, node2)

    def test_node_id_varies_with_index(self):
        node1 = generate_node_id("assembly_abc", 1)
        node2 = generate_node_id("assembly_abc", 2)
        self.assertNotEqual(node1, node2)

    def test_assembly_id_format(self):
        aid = generate_assembly_id("barrett", "parapet_termination", "test.dxf")
        self.assertTrue(aid.startswith("barrett_parapet_termination_"))
        # 12 hex chars after last underscore
        suffix = aid.split("_")[-1]
        self.assertEqual(len(suffix), 12)


class TestLensMerging(unittest.TestCase):
    """Verify lens merging produces unified view."""

    def test_merge_all_lenses(self):
        cad = make_barrett_parapet_cad_output()
        merged = merge_lenses(cad)
        self.assertEqual(merged["meta"]["filename"], "barrett_parapet_detail_001.dxf")
        self.assertIn("PARAPET", merged["layers"])
        self.assertGreater(len(merged["geometry"]), 0)
        self.assertGreater(len(merged["notes"]), 0)
        self.assertGreater(len(merged["entities"]), 0)
        self.assertGreater(merged["total_linear_feet"], 0)
        self.assertIn("CANT_STRIP", merged["block_counts"])

    def test_merge_preserves_quantities(self):
        cad = make_barrett_parapet_cad_output()
        merged = merge_lenses(cad)
        self.assertEqual(merged["total_linear_feet"], 75.5)
        self.assertEqual(merged["block_counts"]["CANT_STRIP"], 2)


class TestLayerToSystem(unittest.TestCase):
    """Verify layer-to-system mapping."""

    def test_known_layers(self):
        config = load_config()
        systems = resolve_layers_to_systems(
            ["PARAPET", "FLASHING", "INSULATION"],
            config["layer_to_system"]
        )
        self.assertIn("SBS Modified Bitumen", systems)
        self.assertIn("Thermal Envelope", systems)

    def test_unknown_layer(self):
        config = load_config()
        systems = resolve_layers_to_systems(
            ["XYZZY"],
            config["layer_to_system"]
        )
        self.assertEqual(systems, [])


class TestBlockToComponent(unittest.TestCase):
    """Verify block-to-component normalization."""

    def test_known_blocks(self):
        config = load_config()
        components = resolve_blocks_to_components(
            {"CANT_STRIP": 2, "TERM_BAR": 1},
            config["block_to_component"]
        )
        comp_ids = [c["component_id"] for c in components]
        self.assertIn("cant_strip", comp_ids)
        self.assertIn("termination_bar", comp_ids)

    def test_deduplication(self):
        config = load_config()
        components = resolve_blocks_to_components(
            {"TERM_BAR": 1, "TERMINATION_BAR": 1},
            config["block_to_component"]
        )
        comp_ids = [c["component_id"] for c in components]
        self.assertEqual(comp_ids.count("termination_bar"), 1)


class TestManufacturerExtraction(unittest.TestCase):
    """Verify regex manufacturer extraction."""

    def test_barrett_match(self):
        config = load_config()
        result = resolve_manufacturer(
            "BARRETT SBS MODIFIED BITUMEN",
            config["text_regex_to_manufacturer"]
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["manufacturer_id"], "barrett")

    def test_no_match(self):
        config = load_config()
        result = resolve_manufacturer(
            "GENERAL ROOFING DETAIL",
            config["text_regex_to_manufacturer"]
        )
        self.assertIsNone(result)


class TestSystemExtraction(unittest.TestCase):
    """Verify system type extraction."""

    def test_sbs_from_text(self):
        config = load_config()
        result = resolve_system(
            "SBS MODIFIED BITUMEN",
            config["text_regex_to_system"],
            []
        )
        self.assertEqual(result, "SBS Modified Bitumen")

    def test_fallback_to_layers(self):
        config = load_config()
        result = resolve_system(
            "SOME GENERIC TEXT",
            config["text_regex_to_system"],
            ["SBS Modified Bitumen"]
        )
        self.assertEqual(result, "SBS Modified Bitumen")


class TestConditionClassification(unittest.TestCase):
    """Verify condition classification heuristics."""

    def test_parapet_classification(self):
        config = load_config()
        result = classify_condition(
            "PARAPET TERMINATION FLASHING DETAIL",
            ["PARAPET", "FLASHING"],
            {"CANT_STRIP": 2, "TERM_BAR": 1},
            config["condition_heuristics"]
        )
        self.assertEqual(result, "parapet_termination")

    def test_drain_classification(self):
        config = load_config()
        result = classify_condition(
            "ROOF DRAIN DETAIL",
            ["DRAINAGE"],
            {"ROOF_DRAIN": 1},
            config["condition_heuristics"]
        )
        self.assertEqual(result, "roof_drain")

    def test_ambiguous_returns_none(self):
        config = load_config()
        result = classify_condition(
            "GENERAL NOTE",
            ["LAYER1"],
            {},
            config["condition_heuristics"]
        )
        self.assertIsNone(result)


class TestFailClosed(unittest.TestCase):
    """Verify fail-closed validation."""

    def test_all_resolved(self):
        errors = validate_fail_closed(
            {"manufacturer_id": "barrett", "manufacturer_name": "Barrett"},
            "SBS Modified Bitumen",
            "parapet_termination",
            [{"component_id": "cant_strip"}],
            {"meta": {"filename": "test.dxf"}}
        )
        self.assertEqual(errors, [])

    def test_no_manufacturer(self):
        errors = validate_fail_closed(
            None, "SBS", "parapet_termination", [], {"meta": {}}
        )
        self.assertTrue(any("manufacturer unresolved" in e for e in errors))

    def test_no_system(self):
        errors = validate_fail_closed(
            {"manufacturer_id": "x", "manufacturer_name": "X"},
            None, "parapet_termination", [], {"meta": {}}
        )
        self.assertTrue(any("system unresolved" in e for e in errors))

    def test_no_condition(self):
        errors = validate_fail_closed(
            {"manufacturer_id": "x", "manufacturer_name": "X"},
            "SBS", None, [], {"meta": {}}
        )
        self.assertTrue(any("condition ambiguous" in e for e in errors))

    def test_no_meta(self):
        errors = validate_fail_closed(
            {"manufacturer_id": "x", "manufacturer_name": "X"},
            "SBS", "parapet_termination", [], {}
        )
        self.assertTrue(any("schema mismatch" in e for e in errors))


class TestBarrettParapetNormalization(unittest.TestCase):
    """Full integration test: Barrett parapet fixture."""

    def setUp(self):
        self.config = load_config()
        self.cad_output = make_barrett_parapet_cad_output()

    def test_normalize_succeeds(self):
        result = normalize(self.cad_output, self.config)
        self.assertIn("assembly_id", result)
        self.assertIn("node_id", result)

    def test_manufacturer_is_barrett(self):
        result = normalize(self.cad_output, self.config)
        self.assertEqual(result["manufacturer_id"], "barrett")
        self.assertEqual(result["manufacturer_name"], "Barrett Company")

    def test_condition_is_parapet(self):
        result = normalize(self.cad_output, self.config)
        self.assertEqual(result["condition_type"], "parapet_termination")

    def test_system_is_sbs(self):
        result = normalize(self.cad_output, self.config)
        self.assertEqual(result["system_type"], "SBS Modified Bitumen")

    def test_components_present(self):
        result = normalize(self.cad_output, self.config)
        comp_ids = [c["component_id"] for c in result["components"]]
        self.assertIn("cant_strip", comp_ids)
        self.assertIn("termination_bar", comp_ids)

    def test_assembly_constraints_present(self):
        result = normalize(self.cad_output, self.config)
        self.assertGreater(len(result["assembly_constraints"]), 0)

    def test_lineage_preserved(self):
        result = normalize(self.cad_output, self.config)
        lineage = result["lineage"]
        self.assertEqual(lineage["source_authority"], "10-Construction_OS")
        self.assertEqual(lineage["source_file"], "barrett_parapet_detail_001.dxf")
        self.assertEqual(lineage["normalizer"], "detail_atlas_normalizer")
        self.assertEqual(lineage["config_id"], "barrett_sbs_detail_atlas")

    def test_deterministic_output(self):
        """Same input must produce same IDs."""
        r1 = normalize(self.cad_output, self.config)
        r2 = normalize(self.cad_output, self.config)
        self.assertEqual(r1["assembly_id"], r2["assembly_id"])
        self.assertEqual(r1["node_id"], r2["node_id"])

    def test_template_path_assigned(self):
        result = normalize(self.cad_output, self.config)
        self.assertEqual(result["template_path"], "templates/parapet_termination.svg")

    def test_quantities_preserved(self):
        result = normalize(self.cad_output, self.config)
        self.assertEqual(result["source_quantities"]["total_linear_feet"], 75.5)

    def test_canonical_json_structure(self):
        """Verify all required top-level keys are present."""
        result = normalize(self.cad_output, self.config)
        required_keys = [
            "assembly_id", "assembly_version", "node_id",
            "manufacturer_id", "manufacturer_name",
            "condition_type", "system_type",
            "components", "assembly_constraints",
            "template_path", "lineage", "artifacts_enabled",
        ]
        for key in required_keys:
            self.assertIn(key, result, f"Missing required key: {key}")


class TestRoofDrainNormalization(unittest.TestCase):
    """Full integration test: Roof drain fixture."""

    def setUp(self):
        self.config = load_config()
        self.cad_output = make_roof_drain_cad_output()

    def test_normalize_succeeds(self):
        result = normalize(self.cad_output, self.config)
        self.assertEqual(result["condition_type"], "roof_drain")
        self.assertEqual(result["manufacturer_id"], "barrett")

    def test_drain_component(self):
        result = normalize(self.cad_output, self.config)
        comp_ids = [c["component_id"] for c in result["components"]]
        self.assertIn("roof_drain", comp_ids)

    def test_drain_constraints(self):
        result = normalize(self.cad_output, self.config)
        rule_ids = [c["rule_id"] for c in result["assembly_constraints"]]
        self.assertIn("RULE_DRAIN_FLASHING", rule_ids)


class TestAmbiguousInputFailClosed(unittest.TestCase):
    """Verify ambiguous input triggers fail-closed."""

    def test_raises_normalization_error(self):
        config = load_config()
        cad_output = make_ambiguous_cad_output()
        with self.assertRaises(NormalizationError) as ctx:
            normalize(cad_output, config)
        error_msg = str(ctx.exception)
        self.assertIn("manufacturer unresolved", error_msg)
        self.assertIn("condition ambiguous", error_msg)


if __name__ == "__main__":
    unittest.main()
