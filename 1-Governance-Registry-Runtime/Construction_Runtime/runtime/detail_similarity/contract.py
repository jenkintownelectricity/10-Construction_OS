"""
Detail Similarity Contract — Wave 15.

Defines the contract surface for the detail similarity subsystem.
Similarity is ADVISORY — it does not redefine canonical relationships.
"""

from typing import Any

CONTRACT_VERSION = "15.1.0"
WAVE = "15"
SUBSYSTEM = "detail_similarity"

SIMILARITY_FACTORS = [
    "tags",
    "conditions",
    "components",
    "geometry_type",
    "relationship_context",
]

FACTOR_WEIGHTS = {
    "tags": 0.30,
    "conditions": 0.20,
    "components": 0.15,
    "geometry_type": 0.20,
    "assembly_family": 0.15,
}


class DetailSimilarityContract:
    """Contract definition for compute_detail_similarity()."""

    @staticmethod
    def input_spec() -> dict[str, Any]:
        return {
            "detail_id": "str — source detail ID",
            "candidate_id": "str — candidate detail ID to compare",
            "detail_index": "dict — built detail index artifact",
        }

    @staticmethod
    def output_spec() -> dict[str, Any]:
        return {
            "source_id": "str",
            "candidate_id": "str",
            "similarity_score": "float — 0.0 to 1.0",
            "factor_scores": "dict[str, float] — per-factor similarity scores",
            "advisory": "bool — always True, similarity is advisory",
            "deterministic": "bool — always True",
        }

    @staticmethod
    def rules() -> list[str]:
        return [
            "Similarity is advisory, not truth",
            "Similarity must not redefine canonical relationships",
            "Scores must be deterministic from declared factors",
            "Weights must sum to 1.0",
        ]
