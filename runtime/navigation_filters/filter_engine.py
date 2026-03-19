"""FilterEngine — pure predicate-based filtering over node collections.

All filters are read-only predicates. No graph mutation. No side effects.
Operates on node summary dicts (as produced by NavigationQueryEngine).
"""

from __future__ import annotations

from typing import Callable


# Supported filter keys and the node-dict paths they match against.
_FILTER_EXTRACTORS: dict[str, Callable[[dict], object]] = {
    "system": lambda n: n.get("state_summary", {}).get("system"),
    "owner": lambda n: n.get("state_summary", {}).get("owner"),
    "readiness_state": lambda n: n.get("readiness_state"),
    "issue_type": lambda n: n.get("state_summary", {}).get("issue_type"),
    "blocker_type": lambda n: n.get("state_summary", {}).get("blocker_type"),
    "pattern_classification": lambda n: n.get("state_summary", {}).get("pattern_classification"),
    "assembly": lambda n: n.get("state_summary", {}).get("assembly"),
    "enrichment_distinction": lambda n: n.get("is_enrichment_derived"),
    "node_type": lambda n: n.get("node_type"),
}


class FilterEngine:
    """Pure predicate-based filter engine over node collections.

    Supports the following filter keys:
    - system, owner, readiness_state, issue_type, blocker_type,
      pattern_classification, assembly, enrichment_distinction, node_type

    Filters are applied as conjunction (AND): a node must match ALL supplied
    filter predicates to be included in the result.
    """

    def __init__(self) -> None:
        pass

    def apply_filters(self, nodes: list[dict], filters_dict: dict) -> list[dict]:
        """Apply all filters in *filters_dict* to *nodes* and return the matching subset.

        Parameters
        ----------
        nodes:
            List of node summary dicts.
        filters_dict:
            Mapping of filter key to desired value. Keys must be from the
            supported set. Unknown keys are silently ignored.

        Returns
        -------
        list[dict]
            Nodes that match ALL supplied filters.
        """
        if not filters_dict:
            return list(nodes)

        # Build predicate list from supplied filters.
        predicates: list[Callable[[dict], bool]] = []
        for key, desired_value in filters_dict.items():
            extractor = _FILTER_EXTRACTORS.get(key)
            if extractor is None:
                continue
            predicates.append(self._make_predicate(extractor, desired_value))

        if not predicates:
            return list(nodes)

        return [n for n in nodes if all(pred(n) for pred in predicates)]

    @staticmethod
    def _make_predicate(
        extractor: Callable[[dict], object], desired_value: object
    ) -> Callable[[dict], bool]:
        """Create a predicate that checks whether a node's extracted value matches.

        Supports exact match for scalars and membership check for lists/sets.
        """
        if isinstance(desired_value, (list, set, tuple)):
            desired_set = set(desired_value)
            return lambda n: extractor(n) in desired_set
        return lambda n: extractor(n) == desired_value
