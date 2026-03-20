"""
Detail Search Engine — Wave 15.

Tier 0 deterministic search over the detail index.
Supports tag, family, condition, name, synonym, and composite search.
"""

from typing import Any


class DetailSearchError(Exception):
    """Raised when search fails validation. Fail closed."""


VALID_SEARCH_TYPES = frozenset(["tag", "family", "condition", "name", "synonym", "composite"])


def search_details(
    query: str,
    search_type: str,
    detail_index: dict[str, Any],
) -> dict[str, Any]:
    """
    Search the detail index.

    Args:
        query: Search query string.
        search_type: Type of search to perform.
        detail_index: Built detail index artifact.

    Returns:
        Search results dict.

    Raises:
        DetailSearchError on invalid search_type.
    """
    if search_type not in VALID_SEARCH_TYPES:
        raise DetailSearchError(f"Unknown search_type: {search_type}. Valid: {sorted(VALID_SEARCH_TYPES)}")

    if not query or not query.strip():
        return _empty_result(query, search_type)

    query_normalized = query.strip().lower()

    if search_type == "tag":
        return _search_by_tag(query_normalized, detail_index)
    elif search_type == "family":
        return _search_by_family(query_normalized, detail_index)
    elif search_type == "condition":
        return _search_by_condition(query_normalized, detail_index)
    elif search_type == "name":
        return _search_by_name(query_normalized, detail_index)
    elif search_type == "synonym":
        return _search_by_synonym(query_normalized, detail_index)
    elif search_type == "composite":
        return _search_composite(query_normalized, detail_index)
    else:
        raise DetailSearchError(f"Unhandled search_type: {search_type}")


def _empty_result(query: str, search_type: str) -> dict[str, Any]:
    return {
        "results": [],
        "query": query,
        "search_type": search_type,
        "tier": 0,
        "total_results": 0,
        "deterministic": True,
    }


def _search_by_tag(query: str, index: dict[str, Any]) -> dict[str, Any]:
    """Search by tag — exact or prefix match."""
    tag_index = index.get("tag_index", {})
    results = []

    for tag, detail_ids in sorted(tag_index.items()):
        if tag.lower() == query or tag.lower().startswith(query):
            for did in sorted(detail_ids):
                record = index.get("detail_lookup", {}).get(did)
                if record and did not in [r["detail_id"] for r in results]:
                    results.append({
                        "detail_id": did,
                        "match_type": "tag",
                        "matched_value": tag,
                        "display_name": record.get("display_name", ""),
                    })

    return {
        "results": results,
        "query": query,
        "search_type": "tag",
        "tier": 0,
        "total_results": len(results),
        "deterministic": True,
    }


def _search_by_family(query: str, index: dict[str, Any]) -> dict[str, Any]:
    """Search by assembly family."""
    family_index = index.get("family_index", {})
    results = []

    for family, detail_ids in sorted(family_index.items()):
        if family.lower() == query or query in family.lower():
            for did in sorted(detail_ids):
                record = index.get("detail_lookup", {}).get(did)
                if record:
                    results.append({
                        "detail_id": did,
                        "match_type": "family",
                        "matched_value": family,
                        "display_name": record.get("display_name", ""),
                    })

    return {
        "results": results,
        "query": query,
        "search_type": "family",
        "tier": 0,
        "total_results": len(results),
        "deterministic": True,
    }


def _search_by_condition(query: str, index: dict[str, Any]) -> dict[str, Any]:
    """Search by condition type."""
    condition_index = index.get("condition_index", {})
    results = []

    for condition, detail_ids in sorted(condition_index.items()):
        if condition.lower() == query or query in condition.lower():
            for did in sorted(detail_ids):
                record = index.get("detail_lookup", {}).get(did)
                if record:
                    results.append({
                        "detail_id": did,
                        "match_type": "condition",
                        "matched_value": condition,
                        "display_name": record.get("display_name", ""),
                    })

    return {
        "results": results,
        "query": query,
        "search_type": "condition",
        "tier": 0,
        "total_results": len(results),
        "deterministic": True,
    }


def _search_by_name(query: str, index: dict[str, Any]) -> dict[str, Any]:
    """Search by canonical display name."""
    detail_lookup = index.get("detail_lookup", {})
    results = []

    for did, record in sorted(detail_lookup.items()):
        display_name = record.get("display_name", "").lower()
        if query in display_name:
            results.append({
                "detail_id": did,
                "match_type": "name",
                "matched_value": record.get("display_name", ""),
                "display_name": record.get("display_name", ""),
            })

    return {
        "results": results,
        "query": query,
        "search_type": "name",
        "tier": 0,
        "total_results": len(results),
        "deterministic": True,
    }


def _search_by_synonym(query: str, index: dict[str, Any]) -> dict[str, Any]:
    """Search by synonym/alias."""
    detail_lookup = index.get("detail_lookup", {})
    results = []

    for did, record in sorted(detail_lookup.items()):
        synonyms = record.get("synonyms", [])
        for syn in synonyms:
            if query in syn.lower():
                results.append({
                    "detail_id": did,
                    "match_type": "synonym",
                    "matched_value": syn,
                    "display_name": record.get("display_name", ""),
                })
                break  # One match per detail

    return {
        "results": results,
        "query": query,
        "search_type": "synonym",
        "tier": 0,
        "total_results": len(results),
        "deterministic": True,
    }


def _search_composite(query: str, index: dict[str, Any]) -> dict[str, Any]:
    """Composite search across all types. Deterministic union of results."""
    seen_ids: set[str] = set()
    results: list[dict[str, Any]] = []

    for search_fn in [_search_by_name, _search_by_synonym, _search_by_tag,
                      _search_by_family, _search_by_condition]:
        sub_result = search_fn(query, index)
        for r in sub_result["results"]:
            if r["detail_id"] not in seen_ids:
                seen_ids.add(r["detail_id"])
                results.append(r)

    return {
        "results": results,
        "query": query,
        "search_type": "composite",
        "tier": 0,
        "total_results": len(results),
        "deterministic": True,
    }
