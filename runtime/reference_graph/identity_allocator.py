"""
Identity Allocator — Wave 17A Construction Reference Graph.

Allocates stable, deterministic identities for all reference graph nodes.
ID format: CRG-{TYPE}-{NUMBER}
Identity is derived from (source_system, source_reference, object_type, scope).
Collisions fail closed.
"""

import hashlib
import threading
from typing import Any


# Canonical object types in the reference graph
VALID_OBJECT_TYPES = frozenset([
    "DETAIL", "VARIANT", "INSTRUCTION_SET", "MANIFEST",
    "RENDER_JOB", "DRAWING", "PDF", "DXF", "SVG",
    "MARKUP", "ANNOTATION", "OBSERVATION",
    "CONDITION", "PROJECT", "ARTIFACT",
    "ARTIFACT_REGION", "PAGE_REFERENCE",
])

# Type abbreviations for ID generation
TYPE_ABBREVIATIONS = {
    "DETAIL": "DETAIL",
    "VARIANT": "VARIANT",
    "INSTRUCTION_SET": "INSTRSET",
    "MANIFEST": "MANIFEST",
    "RENDER_JOB": "RJOB",
    "DRAWING": "DRAWING",
    "PDF": "PDF",
    "DXF": "DXF",
    "SVG": "SVG",
    "MARKUP": "MARKUP",
    "ANNOTATION": "ANNOT",
    "OBSERVATION": "OBS",
    "CONDITION": "COND",
    "PROJECT": "PROJECT",
    "ARTIFACT": "ARTIFACT",
    "ARTIFACT_REGION": "ARTREGN",
    "PAGE_REFERENCE": "PAGEREF",
}


class IdentityAllocationError(Exception):
    """Raised when identity allocation fails. Fail closed."""


class IdentityAllocator:
    """Allocates stable, deterministic CRG identities.

    Thread-safe. Deterministic given the same inputs.
    Duplicate submissions with identical payloads return existing IDs (idempotent replay).
    Duplicate submissions with different payloads fail closed.
    """

    def __init__(self) -> None:
        self._counter: dict[str, int] = {}
        self._identity_map: dict[str, str] = {}  # fingerprint -> graph_id
        self._payload_map: dict[str, dict[str, Any]] = {}  # fingerprint -> payload
        self._lock = threading.Lock()

    @staticmethod
    def compute_fingerprint(
        source_system: str,
        source_reference: str,
        object_type: str,
        scope: str,
    ) -> str:
        """Compute deterministic fingerprint for uniqueness checking."""
        raw = f"{source_system}:{source_reference}:{object_type}:{scope}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def allocate(
        self,
        source_system: str,
        source_reference: str,
        object_type: str,
        scope: str,
        payload: dict[str, Any] | None = None,
    ) -> str:
        """Allocate a stable CRG identity.

        Returns:
            CRG-{TYPE}-{NUMBER} format identity string.

        Raises:
            IdentityAllocationError: on invalid type, collision with different payload.
        """
        if object_type not in VALID_OBJECT_TYPES:
            raise IdentityAllocationError(
                f"Invalid object_type '{object_type}'. "
                f"Valid types: {sorted(VALID_OBJECT_TYPES)}"
            )

        if not source_system or not source_reference or not scope:
            raise IdentityAllocationError(
                "source_system, source_reference, and scope are all required."
            )

        fingerprint = self.compute_fingerprint(
            source_system, source_reference, object_type, scope,
        )
        payload = payload or {}

        with self._lock:
            if fingerprint in self._identity_map:
                existing_payload = self._payload_map.get(fingerprint, {})
                if existing_payload == payload:
                    return self._identity_map[fingerprint]
                raise IdentityAllocationError(
                    f"Identity collision: {source_system}:{source_reference}:"
                    f"{object_type}:{scope} already allocated with different payload."
                )

            abbrev = TYPE_ABBREVIATIONS[object_type]
            count = self._counter.get(object_type, 0) + 1
            self._counter[object_type] = count
            graph_id = f"CRG-{abbrev}-{count:06d}"

            self._identity_map[fingerprint] = graph_id
            self._payload_map[fingerprint] = payload

        return graph_id

    def lookup(self, fingerprint: str) -> str | None:
        """Look up an existing graph_id by fingerprint."""
        return self._identity_map.get(fingerprint)

    def count(self, object_type: str | None = None) -> int:
        """Return count of allocated identities, optionally filtered by type."""
        if object_type:
            return self._counter.get(object_type, 0)
        return sum(self._counter.values())

    def reset(self) -> None:
        """Reset allocator state. Used for full_rebuild mode."""
        with self._lock:
            self._counter.clear()
            self._identity_map.clear()
            self._payload_map.clear()
