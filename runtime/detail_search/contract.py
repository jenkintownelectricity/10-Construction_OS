"""
Detail Search Contract — Wave 15.

Defines the contract surface for the detail search subsystem.
"""

from typing import Any

CONTRACT_VERSION = "15.1.0"
WAVE = "15"
SUBSYSTEM = "detail_search"

SEARCH_TIERS = {
    0: "deterministic — canonical field matching, exact and prefix",
    1: "advisory — AI-expanded suggestions (bounded, marked advisory)",
}


class DetailSearchContract:
    """Contract definition for search_details()."""

    @staticmethod
    def input_spec() -> dict[str, Any]:
        return {
            "query": "str or dict — search query",
            "search_type": "str — one of: tag, family, condition, name, synonym, composite",
            "detail_index": "dict — built detail index artifact",
        }

    @staticmethod
    def output_spec() -> dict[str, Any]:
        return {
            "results": "list[dict] — matched details with match metadata",
            "query": "str — original query",
            "search_type": "str — type of search performed",
            "tier": "int — search tier (0=deterministic, 1=advisory)",
            "total_results": "int",
            "deterministic": "bool — whether results are Tier 0 deterministic",
        }

    @staticmethod
    def failure_cases() -> list[str]:
        return [
            "Empty query — returns empty results",
            "Unknown search_type — fail closed",
            "Ambiguity above threshold — fail closed or mark advisory",
        ]

    @staticmethod
    def search_types() -> list[str]:
        return ["tag", "family", "condition", "name", "synonym", "composite"]
