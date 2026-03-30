"""
reflection_status_manager.py — Manages reflection statuses for mirror components.

A reflection is a mirror's view of a specific capability or slice.
Each reflection has a lifecycle status that governs what operations
are permitted. Transitions between statuses must follow valid paths.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ReflectionStatus(Enum):
    """
    Lifecycle status of a reflection.

    Lifecycle flow:
        STAGED -> ACTIVE -> FROZEN -> DEPRECATED
                    |                    ^
                    +-----> FROZEN ------+
                    |                    ^
                    +----> DEPRECATED ---+

    STAGED: Registered but not yet active. Under construction or review.
    ACTIVE: Live and operational. Participating in parity checks.
    FROZEN: Temporarily suspended. No updates accepted. Can reactivate or deprecate.
    DEPRECATED: End of life. Scheduled for removal. Terminal state.
    """
    STAGED = "staged"
    ACTIVE = "active"
    FROZEN = "frozen"
    DEPRECATED = "deprecated"


# Valid transitions: from_status -> set of allowed to_statuses
VALID_TRANSITIONS: dict[ReflectionStatus, set[ReflectionStatus]] = {
    ReflectionStatus.STAGED: {ReflectionStatus.ACTIVE, ReflectionStatus.DEPRECATED},
    ReflectionStatus.ACTIVE: {ReflectionStatus.FROZEN, ReflectionStatus.DEPRECATED},
    ReflectionStatus.FROZEN: {ReflectionStatus.ACTIVE, ReflectionStatus.DEPRECATED},
    ReflectionStatus.DEPRECATED: set(),  # Terminal state — no transitions out
}


@dataclass
class ReflectionEntry:
    """
    A single reflection's state record.

    Attributes:
        reflection_id: Unique identifier.
        mirror_id: The mirror that owns this reflection.
        slice_id: The slice this reflection covers.
        status: Current lifecycle status.
        reason: Reason for the current status.
        updated_at: ISO timestamp of last status change.
        history: List of previous status transitions.
    """
    reflection_id: str
    mirror_id: str
    slice_id: str
    status: ReflectionStatus = ReflectionStatus.STAGED
    reason: str = ""
    updated_at: str = ""
    history: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.updated_at:
            self.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "reflection_id": self.reflection_id,
            "mirror_id": self.mirror_id,
            "slice_id": self.slice_id,
            "status": self.status.value,
            "reason": self.reason,
            "updated_at": self.updated_at,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ReflectionEntry:
        """Deserialize from dictionary."""
        return cls(
            reflection_id=data["reflection_id"],
            mirror_id=data["mirror_id"],
            slice_id=data["slice_id"],
            status=ReflectionStatus(data["status"]),
            reason=data.get("reason", ""),
            updated_at=data.get("updated_at", ""),
            history=data.get("history", []),
        )


class ReflectionStatusManager:
    """
    Manages lifecycle statuses for mirror reflections.

    Enforces valid transitions, maintains history, and provides
    query capabilities across all managed reflections.
    """

    def __init__(self) -> None:
        self._reflections: dict[str, ReflectionEntry] = {}

    def register(
        self,
        reflection_id: str,
        mirror_id: str,
        slice_id: str,
        initial_status: ReflectionStatus = ReflectionStatus.STAGED,
        reason: str = "Initial registration",
    ) -> ReflectionEntry:
        """
        Register a new reflection.

        Args:
            reflection_id: Unique identifier for the reflection.
            mirror_id: The mirror that owns this reflection.
            slice_id: The slice this reflection covers.
            initial_status: Starting status (default: STAGED).
            reason: Reason for registration.

        Returns:
            The created ReflectionEntry.

        Raises:
            ValueError: If reflection_id already exists.
        """
        if reflection_id in self._reflections:
            raise ValueError(f"Reflection '{reflection_id}' already registered")

        entry = ReflectionEntry(
            reflection_id=reflection_id,
            mirror_id=mirror_id,
            slice_id=slice_id,
            status=initial_status,
            reason=reason,
        )
        entry.history.append({
            "from_status": None,
            "to_status": initial_status.value,
            "reason": reason,
            "timestamp": entry.updated_at,
        })

        self._reflections[reflection_id] = entry
        return entry

    def get_status(self, reflection_id: str) -> ReflectionStatus:
        """
        Get the current status of a reflection.

        Args:
            reflection_id: The reflection to query.

        Returns:
            Current ReflectionStatus.

        Raises:
            KeyError: If reflection_id is not registered.
        """
        if reflection_id not in self._reflections:
            raise KeyError(f"Reflection '{reflection_id}' not found")
        return self._reflections[reflection_id].status

    def set_status(
        self,
        reflection_id: str,
        new_status: ReflectionStatus,
        reason: str = "",
    ) -> ReflectionEntry:
        """
        Transition a reflection to a new status.

        Args:
            reflection_id: The reflection to update.
            new_status: The target status.
            reason: Reason for the transition.

        Returns:
            The updated ReflectionEntry.

        Raises:
            KeyError: If reflection_id is not registered.
            ValueError: If the transition is not valid.
        """
        if reflection_id not in self._reflections:
            raise KeyError(f"Reflection '{reflection_id}' not found")

        entry = self._reflections[reflection_id]
        old_status = entry.status

        if not self.validate_transition(old_status, new_status):
            raise ValueError(
                f"Invalid transition: {old_status.value} -> {new_status.value}. "
                f"Valid targets from {old_status.value}: "
                f"{[s.value for s in VALID_TRANSITIONS[old_status]]}"
            )

        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        entry.history.append({
            "from_status": old_status.value,
            "to_status": new_status.value,
            "reason": reason,
            "timestamp": now,
        })
        entry.status = new_status
        entry.reason = reason
        entry.updated_at = now

        return entry

    def validate_transition(
        self,
        from_status: ReflectionStatus,
        to_status: ReflectionStatus,
    ) -> bool:
        """
        Check whether a status transition is valid.

        Args:
            from_status: Current status.
            to_status: Desired target status.

        Returns:
            True if the transition is allowed, False otherwise.
        """
        return to_status in VALID_TRANSITIONS.get(from_status, set())

    def list_reflections(
        self,
        mirror_id: Optional[str] = None,
        status: Optional[ReflectionStatus] = None,
        slice_id: Optional[str] = None,
    ) -> list[ReflectionEntry]:
        """
        List reflections with optional filters.

        Args:
            mirror_id: Filter by mirror ID.
            status: Filter by current status.
            slice_id: Filter by slice ID.

        Returns:
            List of matching ReflectionEntry objects.
        """
        results = list(self._reflections.values())

        if mirror_id is not None:
            results = [r for r in results if r.mirror_id == mirror_id]

        if status is not None:
            results = [r for r in results if r.status == status]

        if slice_id is not None:
            results = [r for r in results if r.slice_id == slice_id]

        return results

    def get_entry(self, reflection_id: str) -> ReflectionEntry:
        """
        Get the full reflection entry.

        Args:
            reflection_id: The reflection to query.

        Returns:
            The ReflectionEntry.

        Raises:
            KeyError: If reflection_id is not registered.
        """
        if reflection_id not in self._reflections:
            raise KeyError(f"Reflection '{reflection_id}' not found")
        return self._reflections[reflection_id]

    def has_reflection(self, reflection_id: str) -> bool:
        """Check whether a reflection is registered."""
        return reflection_id in self._reflections

    def count(self, status: Optional[ReflectionStatus] = None) -> int:
        """
        Count registered reflections, optionally filtered by status.

        Args:
            status: Optional status filter.

        Returns:
            Count of matching reflections.
        """
        if status is None:
            return len(self._reflections)
        return sum(1 for r in self._reflections.values() if r.status == status)
