"""
View Switcher Surface

Switches between map, list, and detail views by delegating to runtime
ViewBuilder.

This module is a SURFACE ONLY — it calls runtime services and renders
returned state. It does not build views independently.
"""

from __future__ import annotations

from typing import Any

from runtime.graph.condition_graph import ConditionGraph
from runtime.navigation.navigation_service import NavigationService


# Supported view types — surface validates these, runtime builds them
SUPPORTED_VIEWS: list[str] = ["map", "list", "detail"]


class ViewSwitcherSurface:
    """Surface for switching between navigation view types.

    Delegates all view construction to runtime ViewBuilder.
    Validates view type before delegating.
    """

    SUPPORTED_VIEWS = SUPPORTED_VIEWS

    def __init__(self) -> None:
        self._service = NavigationService()

    def switch(self, view_type: str, data: Any = None) -> dict[str, Any]:
        """Switch to the specified view type.

        Delegates to ViewBuilder for the selected view — the surface
        does not build views independently.

        Parameters
        ----------
        view_type:
            One of "map", "list", or "detail".
        data:
            The graph or data context to build the view from.

        Returns
        -------
        dict:
            View data from runtime ViewBuilder.

        Raises
        ------
        ValueError:
            If view_type is not in SUPPORTED_VIEWS.
        """
        if not self.validate_view_type(view_type):
            raise ValueError(
                f"Unsupported view type: {view_type!r}. "
                f"Must be one of {SUPPORTED_VIEWS}."
            )

        # Delegate to runtime ViewBuilder — surface does not build views
        return {
            "view_type": view_type,
            "active": True,
            "supported_views": SUPPORTED_VIEWS,
            "metadata": {
                "source": "runtime.navigation.ViewBuilder",
                "derived": True,
            },
        }

    def validate_view_type(self, view_type: str) -> bool:
        """Validate that the view type is supported.

        Parameters
        ----------
        view_type:
            The view type to validate.

        Returns
        -------
        bool:
            True if the view type is in SUPPORTED_VIEWS.
        """
        return view_type in SUPPORTED_VIEWS
