"""
Detail Map Cache — Wave 14 Subsystem 4.

Simple derivable cache for route query results.
Cache is entirely derived and safe to delete at any time.
"""

import hashlib
import json
from typing import Any


class DetailMapCache:
    """In-memory derivable cache for detail map queries."""

    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}

    def get(self, key: str) -> Any | None:
        return self._cache.get(key)

    def put(self, key: str, value: Any) -> None:
        self._cache[key] = value

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)

    @staticmethod
    def make_key(*args: str) -> str:
        """Create a deterministic cache key from arguments."""
        raw = "|".join(args)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
