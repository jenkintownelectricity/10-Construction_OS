"""Runtime-to-Cognitive-Bus adapter/client seam.

This module provides the bounded adapter through which Construction_Runtime
publishes events to Construction_Cognitive_Bus. It is the single integration
point — runtime code never imports bus internals directly.

Fail-closed: if the bus is unavailable or rejects an event that was required,
the adapter raises rather than silently continuing.
"""

from __future__ import annotations

from typing import Any


class BusPublicationError(Exception):
    """Raised when event publication to the Cognitive Bus fails.

    This is a fail-closed error — the runtime must not silently continue
    when a required event cannot be published.
    """

    def __init__(self, event_type: str, reason: str, event: dict[str, Any] | None = None):
        self.event_type = event_type
        self.reason = reason
        self.event = event
        super().__init__(
            f"Bus publication failed for {event_type}: {reason}"
        )


class CognitiveBusAdapter:
    """Adapter seam for publishing runtime events to the Cognitive Bus.

    This adapter encapsulates all interaction with the bus. The default
    implementation imports and calls the bus admission gate directly.
    For testing or when the bus is not available, a custom publish function
    can be injected.
    """

    def __init__(self, publish_fn: Any = None):
        """Initialize the adapter.

        Args:
            publish_fn: Optional callable(event_dict) -> result_dict.
                If None, the adapter will attempt to import and use
                the Cognitive Bus admission gate directly.
        """
        self._publish_fn = publish_fn
        self._bus_available: bool | None = None

    def publish(self, event: dict[str, Any]) -> dict[str, Any]:
        """Publish an event to the Cognitive Bus.

        Args:
            event: A complete event envelope dict.

        Returns:
            The bus admission result dict.

        Raises:
            BusPublicationError: If publication fails for any reason.
        """
        event_type = event.get("event_type", "unknown")

        if self._publish_fn is not None:
            return self._call_publish(self._publish_fn, event, event_type)

        # Attempt direct bus import
        receive_fn = self._get_bus_receive_fn()
        return self._call_publish(receive_fn, event, event_type)

    def _get_bus_receive_fn(self) -> Any:
        """Resolve the bus admission gate function.

        Raises:
            BusPublicationError: If bus module cannot be imported.
        """
        try:
            from bus.admission_gate import receive_event  # type: ignore[import-untyped]
            self._bus_available = True
            return receive_event
        except ImportError as exc:
            self._bus_available = False
            raise BusPublicationError(
                event_type="*",
                reason=f"Cognitive Bus module not available: {exc}",
            ) from exc

    def _call_publish(
        self,
        fn: Any,
        event: dict[str, Any],
        event_type: str,
    ) -> dict[str, Any]:
        """Call the publish function and handle failures.

        Raises:
            BusPublicationError: On any failure — fail closed.
        """
        try:
            result = fn(event)
        except BusPublicationError:
            raise
        except Exception as exc:
            raise BusPublicationError(
                event_type=event_type,
                reason=f"Bus call raised {type(exc).__name__}: {exc}",
                event=event,
            ) from exc

        if not isinstance(result, dict):
            raise BusPublicationError(
                event_type=event_type,
                reason=f"Bus returned non-dict result: {type(result).__name__}",
                event=event,
            )

        if not result.get("admitted", False):
            reason = result.get("reason", "unknown rejection reason")
            raise BusPublicationError(
                event_type=event_type,
                reason=f"Bus rejected event: {reason}",
                event=event,
            )

        return result
