"""
Detail Index Contract — Wave 15.

Defines the contract surface for the detail index subsystem.
All inputs, outputs, failure cases, and validation rules are specified here.
"""

from typing import Any

CONTRACT_VERSION = "15.1.0"
WAVE = "15"
SUBSYSTEM = "detail_index"

REQUIRED_DETAIL_FIELDS = frozenset([
    "detail_id", "system", "class", "condition", "variant",
    "assembly_family", "display_name", "synonyms", "tags",
    "compatible_material_classes", "risk_tags",
])

VALID_SYSTEMS = frozenset([
    "LOW_SLOPE", "STEEP_SLOPE", "BELOW_GRADE", "PLAZA_DECK",
    "AIR_BARRIER", "FACADE", "JOINT_PROTECTION",
])

VALID_CLASSES = frozenset([
    "TERMINATION", "EDGE", "PENETRATION", "TRANSITION",
    "DRAINAGE", "JOINT", "OPENING", "ANCHORAGE",
])


class DetailIndexContract:
    """Contract definition for build_detail_index()."""

    @staticmethod
    def input_spec() -> dict[str, Any]:
        return {
            "detail_dna_records": "list[dict] — canonical Detail DNA records from Construction_Kernel",
            "tag_index": "dict — tag-to-detail reverse index from Construction_Kernel",
            "route_index": "dict — detail-to-detail route relationships from Construction_Kernel",
        }

    @staticmethod
    def output_spec() -> dict[str, Any]:
        return {
            "detail_index": {
                "version": "str — contract version",
                "wave": "str — wave identifier",
                "detail_lookup": "dict[detail_id -> detail_record]",
                "family_index": "dict[assembly_family -> list[detail_id]]",
                "tag_index": "dict[tag -> list[detail_id]]",
                "condition_index": "dict[condition -> list[detail_id]]",
                "system_index": "dict[system -> list[detail_id]]",
                "class_index": "dict[class -> list[detail_id]]",
                "checksum": "str — SHA-256 of deterministic content",
            }
        }

    @staticmethod
    def failure_cases() -> list[str]:
        return [
            "Detail record missing required fields — fail closed",
            "Duplicate detail_id — fail closed",
            "Detail references invalid system/class — fail closed",
            "Empty detail_dna_records — fail closed",
        ]

    @staticmethod
    def validation_rules() -> list[str]:
        return [
            "Every indexed detail must have all REQUIRED_DETAIL_FIELDS",
            "No duplicate detail_id values allowed",
            "All system values must be in VALID_SYSTEMS",
            "All class values must be in VALID_CLASSES",
            "Output is deterministic for identical input",
        ]
