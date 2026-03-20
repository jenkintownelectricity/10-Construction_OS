"""
Detail Similarity Engine — Wave 15.

Computes advisory similarity scores between details.
Deterministic from declared factors. Does not redefine canonical relationships.
"""

from typing import Any

from runtime.detail_similarity.contract import FACTOR_WEIGHTS


class DetailSimilarityError(Exception):
    """Raised when similarity computation fails."""


def compute_detail_similarity(
    detail_id: str,
    candidate_id: str,
    detail_index: dict[str, Any],
) -> dict[str, Any]:
    """
    Compute similarity between two details.

    Args:
        detail_id: Source detail ID.
        candidate_id: Candidate detail ID to compare.
        detail_index: Built detail index artifact.

    Returns:
        Similarity result dict.
    """
    detail_lookup = detail_index.get("detail_lookup", {})

    if detail_id not in detail_lookup:
        raise DetailSimilarityError(f"Unknown detail_id: {detail_id}")
    if candidate_id not in detail_lookup:
        raise DetailSimilarityError(f"Unknown candidate_id: {candidate_id}")

    source = detail_lookup[detail_id]
    candidate = detail_lookup[candidate_id]

    factor_scores = {
        "tags": _tag_similarity(source, candidate),
        "conditions": _condition_similarity(source, candidate),
        "components": _component_similarity(source, candidate),
        "geometry_type": _geometry_similarity(source, candidate),
        "assembly_family": _family_similarity(source, candidate),
    }

    weighted_score = sum(
        factor_scores[factor] * weight
        for factor, weight in FACTOR_WEIGHTS.items()
    )

    return {
        "source_id": detail_id,
        "candidate_id": candidate_id,
        "similarity_score": round(weighted_score, 4),
        "factor_scores": {k: round(v, 4) for k, v in factor_scores.items()},
        "advisory": True,
        "deterministic": True,
    }


def find_similar_details(
    detail_id: str,
    detail_index: dict[str, Any],
    top_n: int = 5,
    min_score: float = 0.0,
) -> list[dict[str, Any]]:
    """
    Find the most similar details to a given detail.

    Args:
        detail_id: Source detail ID.
        detail_index: Built detail index artifact.
        top_n: Maximum results to return.
        min_score: Minimum similarity score threshold.

    Returns:
        Sorted list of similarity results (most similar first).
    """
    detail_lookup = detail_index.get("detail_lookup", {})
    if detail_id not in detail_lookup:
        raise DetailSimilarityError(f"Unknown detail_id: {detail_id}")

    results = []
    for candidate_id in sorted(detail_lookup.keys()):
        if candidate_id == detail_id:
            continue
        result = compute_detail_similarity(detail_id, candidate_id, detail_index)
        if result["similarity_score"] >= min_score:
            results.append(result)

    results.sort(key=lambda r: (-r["similarity_score"], r["candidate_id"]))
    return results[:top_n]


def _tag_similarity(source: dict, candidate: dict) -> float:
    """Jaccard similarity on tags."""
    s_tags = set(source.get("tags", []))
    c_tags = set(candidate.get("tags", []))
    if not s_tags and not c_tags:
        return 1.0
    if not s_tags or not c_tags:
        return 0.0
    intersection = s_tags & c_tags
    union = s_tags | c_tags
    return len(intersection) / len(union)


def _condition_similarity(source: dict, candidate: dict) -> float:
    """Binary match on condition field."""
    return 1.0 if source.get("condition") == candidate.get("condition") else 0.0


def _component_similarity(source: dict, candidate: dict) -> float:
    """Jaccard similarity on compatible_material_classes."""
    s_mats = set(source.get("compatible_material_classes", []))
    c_mats = set(candidate.get("compatible_material_classes", []))
    if not s_mats and not c_mats:
        return 1.0
    if not s_mats or not c_mats:
        return 0.0
    intersection = s_mats & c_mats
    union = s_mats | c_mats
    return len(intersection) / len(union)


def _geometry_similarity(source: dict, candidate: dict) -> float:
    """Similarity based on geometry tags (geo-* prefix)."""
    s_geo = {t for t in source.get("tags", []) if t.startswith("geo-")}
    c_geo = {t for t in candidate.get("tags", []) if t.startswith("geo-")}
    if not s_geo and not c_geo:
        return 1.0
    if not s_geo or not c_geo:
        return 0.0
    intersection = s_geo & c_geo
    union = s_geo | c_geo
    return len(intersection) / len(union)


def _family_similarity(source: dict, candidate: dict) -> float:
    """Binary match on assembly_family."""
    return 1.0 if source.get("assembly_family") == candidate.get("assembly_family") else 0.0
