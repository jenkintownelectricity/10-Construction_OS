"""L17 Module Completeness tests — verify all Wave 11A graph modules exist and are populated."""

import os

import pytest


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUNTIME_DIR = os.path.join(REPO_ROOT, "runtime")


GRAPH_MODULE_DIRS = [
    "graph",
    "graph_nodes",
    "graph_edges",
    "graph_validation",
    "graph_queries",
    "graph_materialization",
    "readiness_routing",
    "impact_analysis",
]

KERNEL_TYPING_DIRS = [
    "contracts",
    "standards",
    "validators",
]


class TestModuleCompleteness:
    """L17: All required graph modules and kernel typing directories exist."""

    @pytest.mark.parametrize("module_name", GRAPH_MODULE_DIRS)
    def test_all_graph_modules_exist(self, module_name):
        """Each of the 8 graph module directories must exist under runtime/."""
        module_path = os.path.join(RUNTIME_DIR, module_name)
        assert os.path.isdir(module_path), (
            f"Graph module directory missing: runtime/{module_name}"
        )

    @pytest.mark.parametrize("module_name", GRAPH_MODULE_DIRS)
    def test_all_graph_modules_have_init(self, module_name):
        """Each graph module directory must contain an __init__.py."""
        init_path = os.path.join(RUNTIME_DIR, module_name, "__init__.py")
        assert os.path.isfile(init_path), (
            f"Missing __init__.py in runtime/{module_name}"
        )

    @pytest.mark.parametrize("module_name", GRAPH_MODULE_DIRS)
    def test_all_graph_modules_have_code(self, module_name):
        """Each graph module must have at least one .py file beyond __init__.py."""
        module_path = os.path.join(RUNTIME_DIR, module_name)
        py_files = [
            f for f in os.listdir(module_path)
            if f.endswith(".py") and f != "__init__.py"
        ]
        assert len(py_files) >= 1, (
            f"No code files (beyond __init__.py) in runtime/{module_name}"
        )

    @pytest.mark.parametrize("dir_name", KERNEL_TYPING_DIRS)
    def test_kernel_typing_contracts_exist(self, dir_name):
        """Kernel typing directories must exist at the repository root."""
        dir_path = os.path.join(REPO_ROOT, dir_name)
        assert os.path.isdir(dir_path), (
            f"Kernel typing directory missing: {dir_name}/"
        )
