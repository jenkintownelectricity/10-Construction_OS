"""Tests for runtime module completeness — Wave 8A structural validation.

Validates that all 20 runtime module directories exist, each has an
__init__.py, and each has at least one .py module file.
"""

import os
import pytest

RUNTIME_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "runtime")

# All 20 required runtime module directories
REQUIRED_MODULES = [
    "evidence",
    "bootstrap",
    "assembly_inference",
    "evidence_normalization",
    "workbench",
    "detail_preview",
    "parameter_editing",
    "drawing_generation",
    "sheet_builder",
    "package_builder",
    "qa",
    "deviation_detection",
    "conflict_checks",
    "revision",
    "release",
    "change_tracking",
    "export",
    "graph_refs",
    "condition_linking",
    "dependency_projection",
]


class TestModuleDirectoriesExist:
    """Verify all 20 runtime module directories exist."""

    @pytest.mark.parametrize("module_name", REQUIRED_MODULES)
    def test_directory_exists(self, module_name):
        module_path = os.path.normpath(os.path.join(RUNTIME_ROOT, module_name))
        assert os.path.isdir(module_path), (
            f"Runtime module directory missing: runtime/{module_name}/"
        )

    def test_total_module_count(self):
        assert len(REQUIRED_MODULES) == 20, "Expected exactly 20 required runtime modules"


class TestModuleInitFiles:
    """Verify each module has an __init__.py."""

    @pytest.mark.parametrize("module_name", REQUIRED_MODULES)
    def test_init_py_exists(self, module_name):
        init_path = os.path.normpath(
            os.path.join(RUNTIME_ROOT, module_name, "__init__.py")
        )
        assert os.path.isfile(init_path), (
            f"Missing __init__.py in runtime/{module_name}/"
        )


class TestModuleHasPyFiles:
    """Verify each module has at least one .py module file (beyond __init__.py)."""

    @pytest.mark.parametrize("module_name", REQUIRED_MODULES)
    def test_has_at_least_one_module_file(self, module_name):
        module_dir = os.path.normpath(os.path.join(RUNTIME_ROOT, module_name))
        if not os.path.isdir(module_dir):
            pytest.skip(f"Directory runtime/{module_name}/ does not exist")

        py_files = [
            f for f in os.listdir(module_dir)
            if f.endswith(".py") and f != "__init__.py"
        ]
        assert len(py_files) >= 1, (
            f"runtime/{module_name}/ must contain at least one .py module file "
            f"(besides __init__.py). Found: {os.listdir(module_dir)}"
        )
