"""Tests for Exporter — Wave 8A structural validation.

Validates that the Exporter can be instantiated and exposes required
export methods.
"""

import pytest

from runtime.export.exporter import Exporter


# ---------------------------------------------------------------------------
# Exporter instantiation
# ---------------------------------------------------------------------------

class TestExporterInstantiation:
    """Verify Exporter can be instantiated."""

    def test_instantiate_without_args(self):
        exporter = Exporter()
        assert exporter is not None

    def test_instantiate_with_contract_loader(self):
        exporter = Exporter(contract_loader="mock_loader")
        assert exporter._contract_loader == "mock_loader"

    def test_instantiate_with_config(self):
        exporter = Exporter(config={"format": "pdf"})
        assert exporter._config == {"format": "pdf"}


# ---------------------------------------------------------------------------
# Required methods
# ---------------------------------------------------------------------------

REQUIRED_METHODS = [
    "export_package",
    "export_drawing",
    "generate_deterministic_output",
]


class TestExporterMethods:
    """Verify Exporter has all required export methods."""

    @pytest.mark.parametrize("method_name", REQUIRED_METHODS)
    def test_method_exists(self, method_name):
        exporter = Exporter()
        assert hasattr(exporter, method_name), f"Exporter missing method: {method_name}"

    @pytest.mark.parametrize("method_name", REQUIRED_METHODS)
    def test_method_is_callable(self, method_name):
        exporter = Exporter()
        method = getattr(exporter, method_name)
        assert callable(method), f"Exporter.{method_name} is not callable"

    def test_all_three_methods_present(self):
        exporter = Exporter()
        for method_name in REQUIRED_METHODS:
            assert hasattr(exporter, method_name)
        assert len(REQUIRED_METHODS) == 3
