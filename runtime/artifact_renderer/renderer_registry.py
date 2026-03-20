"""Renderer registry — central catalog of available renderers.

All renderers must register here before they can be used by the pipeline.
The registry enforces capability declarations and prevents unregistered
renderer usage.
"""

from typing import Any, Protocol, runtime_checkable

from runtime.artifact_renderer.artifact_contract import RendererCapability
from runtime.artifact_renderer.renderer_errors import RendererNotFoundError


@runtime_checkable
class RendererProtocol(Protocol):
    """Protocol that all renderers must implement."""

    def renderer_id(self) -> str: ...

    def output_format(self) -> str: ...

    def capability(self) -> RendererCapability: ...

    def render(
        self,
        primitives: list,
        sheet: dict[str, Any],
        layers: list[str],
        metadata: dict[str, Any],
    ) -> tuple[str, list[dict[str, str]]]:
        """Render primitives to output format.

        Returns:
            Tuple of (content_string, list_of_errors).
        """
        ...


class RendererRegistry:
    """Central registry of available renderers.

    Renderers register with their capabilities. The pipeline queries
    the registry to find renderers for requested output formats.
    """

    def __init__(self) -> None:
        self._renderers: dict[str, RendererProtocol] = {}
        self._capabilities: dict[str, RendererCapability] = {}

    def register(self, renderer: RendererProtocol) -> None:
        """Register a renderer. Replaces any existing renderer for the same format."""
        fmt = renderer.output_format()
        self._renderers[fmt] = renderer
        self._capabilities[fmt] = renderer.capability()

    def get_renderer(self, output_format: str) -> RendererProtocol:
        """Get a renderer by output format.

        Raises:
            RendererNotFoundError: If no renderer is registered for the format.
        """
        if output_format not in self._renderers:
            raise RendererNotFoundError(output_format)
        return self._renderers[output_format]

    def has_renderer(self, output_format: str) -> bool:
        """Check if a renderer is registered for the given format."""
        return output_format in self._renderers

    def get_capability(self, output_format: str) -> RendererCapability | None:
        """Get the capability declaration for a format."""
        return self._capabilities.get(output_format)

    def list_formats(self) -> list[str]:
        """List all registered output formats."""
        return sorted(self._renderers.keys())

    def list_capabilities(self) -> list[RendererCapability]:
        """List all registered renderer capabilities."""
        return list(self._capabilities.values())

    def unregister(self, output_format: str) -> None:
        """Remove a renderer from the registry."""
        self._renderers.pop(output_format, None)
        self._capabilities.pop(output_format, None)

    @property
    def renderer_count(self) -> int:
        return len(self._renderers)


# Global registry instance
_global_registry = RendererRegistry()


def get_global_registry() -> RendererRegistry:
    """Get the global renderer registry."""
    return _global_registry


def register_renderer(renderer: RendererProtocol) -> None:
    """Register a renderer in the global registry."""
    _global_registry.register(renderer)


def get_renderer(output_format: str) -> RendererProtocol:
    """Get a renderer from the global registry."""
    return _global_registry.get_renderer(output_format)
