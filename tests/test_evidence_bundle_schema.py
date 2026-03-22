"""
Tests for evidence bundle, manufacturer compatibility, and code/spec lookup schemas.

Validates that the schemas for the ALEXANDER → Runtime resolution seam
scoring inputs are structurally correct and enforce required contracts.
"""

import json
import os
import unittest

SCHEMAS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas")


def _load_schema(name):
    with open(os.path.join(SCHEMAS_DIR, name), "r") as f:
        return json.load(f)


class TestEvidenceBundleSchema(unittest.TestCase):
    """Tests for evidence_bundle.schema.json."""

    def setUp(self):
        self.schema = _load_schema("evidence_bundle.schema.json")

    def test_schema_has_title(self):
        self.assertEqual(self.schema["title"], "Evidence Bundle for Resolution Scoring")

    def test_schema_version_is_1_0_0(self):
        self.assertEqual(self.schema["version"], "1.0.0")

    def test_required_fields(self):
        required = set(self.schema["required"])
        expected = {"bundle_id", "schema_version", "timestamp_utc", "condition_id", "evidence_type", "entries"}
        self.assertEqual(required, expected)

    def test_evidence_types_enum(self):
        types = self.schema["properties"]["evidence_type"]["enum"]
        self.assertIn("manufacturer_compatibility", types)
        self.assertIn("code_compliance", types)
        self.assertIn("specification_lookup", types)
        self.assertIn("field_observation", types)
        self.assertIn("composite", types)

    def test_entries_has_items_def(self):
        self.assertIn("$ref", self.schema["properties"]["entries"]["items"])

    def test_source_component_is_const(self):
        self.assertEqual(
            self.schema["properties"]["source_component"]["const"],
            "Construction_Reference_Intelligence",
        )

    def test_evidence_entry_source_types(self):
        entry_def = self.schema["$defs"]["evidence_entry"]
        source_types = entry_def["properties"]["source_type"]["enum"]
        self.assertIn("manufacturer_data", source_types)
        self.assertIn("building_code", source_types)
        self.assertIn("industry_standard", source_types)
        self.assertIn("compatibility_matrix", source_types)

    def test_evidence_entry_result_enum(self):
        entry_def = self.schema["$defs"]["evidence_entry"]
        results = entry_def["properties"]["result"]["enum"]
        self.assertIn("compatible", results)
        self.assertIn("incompatible", results)
        self.assertIn("compliant", results)
        self.assertIn("non_compliant", results)


class TestManufacturerCompatibilitySchema(unittest.TestCase):
    """Tests for manufacturer_compatibility_lookup.schema.json."""

    def setUp(self):
        self.schema = _load_schema("manufacturer_compatibility_lookup.schema.json")

    def test_schema_has_title(self):
        self.assertIn("Manufacturer Compatibility", self.schema["title"])

    def test_required_fields(self):
        required = set(self.schema["required"])
        expected = {"lookup_id", "schema_version", "timestamp_utc", "query", "results"}
        self.assertEqual(required, expected)

    def test_query_requires_manufacturer_refs(self):
        self.assertIn("manufacturer_refs", self.schema["properties"]["query"]["required"])

    def test_result_compatibility_status_enum(self):
        result_props = self.schema["properties"]["results"]["items"]["properties"]
        statuses = result_props["compatibility_status"]["enum"]
        self.assertIn("compatible", statuses)
        self.assertIn("incompatible", statuses)
        self.assertIn("conditional", statuses)
        self.assertIn("unknown", statuses)

    def test_source_component_is_const(self):
        self.assertEqual(
            self.schema["properties"]["source_component"]["const"],
            "Construction_Reference_Intelligence",
        )


class TestCodeSpecLookupSchema(unittest.TestCase):
    """Tests for code_spec_lookup.schema.json."""

    def setUp(self):
        self.schema = _load_schema("code_spec_lookup.schema.json")

    def test_schema_has_title(self):
        self.assertIn("Code/Specification Lookup", self.schema["title"])

    def test_required_fields(self):
        required = set(self.schema["required"])
        expected = {"lookup_id", "schema_version", "timestamp_utc", "query", "results"}
        self.assertEqual(required, expected)

    def test_query_requires_condition_type(self):
        self.assertIn("condition_type", self.schema["properties"]["query"]["required"])

    def test_result_compliance_status_enum(self):
        result_props = self.schema["properties"]["results"]["items"]["properties"]
        statuses = result_props["compliance_status"]["enum"]
        self.assertIn("compliant", statuses)
        self.assertIn("non_compliant", statuses)
        self.assertIn("conditional", statuses)
        self.assertIn("not_applicable", statuses)

    def test_climate_context_wind_zone_enum(self):
        climate = self.schema["properties"]["query"]["properties"]["climate_context"]
        self.assertEqual(climate["properties"]["wind_zone"]["enum"], [1, 2, 3])

    def test_source_component_is_const(self):
        self.assertEqual(
            self.schema["properties"]["source_component"]["const"],
            "Construction_Reference_Intelligence",
        )


if __name__ == "__main__":
    unittest.main()
