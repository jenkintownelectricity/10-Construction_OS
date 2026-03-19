"""
Navigation Application Surface

Thin application layer that delegates all navigation logic to runtime services.
This package provides UI-facing surfaces for project maps, system maps,
assembly maps, condition panels, blocker panels, dependency panels,
owner panels, remediation panels, evidence panels, artifact panels,
package panels, revision panels, overlays, filters, and view switching.

All modules are SURFACES ONLY — they call runtime services and render
returned state. They do not compute graph edges, blocker chains,
owner routes, or impact sets independently.
"""

from apps.navigation.navigation_app import NavigationApp

__all__ = ["NavigationApp"]
