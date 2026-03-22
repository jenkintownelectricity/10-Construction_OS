"""
Construction Awareness Cache v0.1 — Thaw/freeze lifecycle manager.

Only one thaw session at a time. Fail closed on conflict.
"""


class ThawError(Exception):
    """Raised when a thaw lifecycle violation occurs."""


class ThawManager:
    """Manages the thaw/freeze lifecycle for awareness compilation."""

    def __init__(self):
        self._thawed = False
        self._session_data: list[dict] = []

    @property
    def is_thawed(self) -> bool:
        return self._thawed

    def thaw(self) -> None:
        """Begin a thaw session. Fails if already thawed."""
        if self._thawed:
            raise ThawError("Cannot thaw: session already active")
        self._thawed = True
        self._session_data = []

    def add_validated(self, records: list[dict]) -> None:
        """Add validated records to the current thaw session."""
        if not self._thawed:
            raise ThawError("Cannot add records: no active thaw session")
        self._session_data.extend(records)

    def get_session_data(self) -> list[dict]:
        """Return a copy of current session data."""
        if not self._thawed:
            raise ThawError("Cannot read session data: no active thaw session")
        return list(self._session_data)

    def freeze(self) -> list[dict]:
        """End the thaw session and return the frozen data."""
        if not self._thawed:
            raise ThawError("Cannot freeze: no active thaw session")
        data = list(self._session_data)
        self._session_data = []
        self._thawed = False
        return data
