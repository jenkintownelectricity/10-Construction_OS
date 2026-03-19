"""Tests for RevisionManager — Wave 8A structural validation.

Validates that the revision manager can be instantiated and exposes
the required lineage management methods.
"""

import pytest

from runtime.revision.revision_manager import RevisionManager


# ---------------------------------------------------------------------------
# Instantiation
# ---------------------------------------------------------------------------

class TestRevisionManagerInstantiation:
    """Verify RevisionManager can be created."""

    def test_instantiate_without_args(self):
        manager = RevisionManager()
        assert manager is not None

    def test_instantiate_with_contract_loader(self):
        manager = RevisionManager(contract_loader="mock_loader")
        assert manager._contract_loader == "mock_loader"

    def test_instantiate_with_config(self):
        manager = RevisionManager(config={"auto_tag": True})
        assert manager._config == {"auto_tag": True}


# ---------------------------------------------------------------------------
# Required methods
# ---------------------------------------------------------------------------

REQUIRED_METHODS = [
    "create_revision",
    "get_lineage",
    "compare_revisions",
    "generate_change_summary",
]


class TestRevisionManagerMethods:
    """Verify RevisionManager has all required methods."""

    @pytest.mark.parametrize("method_name", REQUIRED_METHODS)
    def test_method_exists(self, method_name):
        manager = RevisionManager()
        assert hasattr(manager, method_name), f"RevisionManager missing method: {method_name}"

    @pytest.mark.parametrize("method_name", REQUIRED_METHODS)
    def test_method_is_callable(self, method_name):
        manager = RevisionManager()
        method = getattr(manager, method_name)
        assert callable(method), f"RevisionManager.{method_name} is not callable"

    def test_all_four_methods_present(self):
        manager = RevisionManager()
        for method_name in REQUIRED_METHODS:
            assert hasattr(manager, method_name)
        assert len(REQUIRED_METHODS) == 4
