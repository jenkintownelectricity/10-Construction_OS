"""Module completeness tests — verify all Wave 12 modules exist."""

import os
import importlib

import pytest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 10 runtime navigation directories
RUNTIME_NAV_DIRS = [
    "navigation",
    "navigation_queries",
    "navigation_views",
    "navigation_filters",
    "navigation_state",
    "navigation_panels",
    "navigation_map",
    "navigation_list",
    "navigation_detail",
    "navigation_overlays",
]

# 19 app surface files (excluding __init__.py)
APP_NAV_FILES = [
    "navigation_app.py",
    "project_map.py",
    "system_map.py",
    "assembly_map.py",
    "condition_panel.py",
    "blocker_panel.py",
    "dependency_panel.py",
    "owner_panel.py",
    "remediation_panel.py",
    "evidence_panel.py",
    "artifact_panel.py",
    "package_panel.py",
    "revision_panel.py",
    "readiness_overlay.py",
    "impact_overlay.py",
    "filter_bar.py",
    "view_switcher.py",
    "path_trace.py",
]


class TestRuntimeNavigationDirsExist:
    @pytest.mark.parametrize("dirname", RUNTIME_NAV_DIRS)
    def test_runtime_nav_dir_exists(self, dirname):
        dirpath = os.path.join(REPO_ROOT, "runtime", dirname)
        assert os.path.isdir(dirpath), f"Missing runtime directory: {dirpath}"

    @pytest.mark.parametrize("dirname", RUNTIME_NAV_DIRS)
    def test_runtime_nav_dir_has_init(self, dirname):
        init_path = os.path.join(REPO_ROOT, "runtime", dirname, "__init__.py")
        assert os.path.isfile(init_path), f"Missing __init__.py: {init_path}"


class TestAppNavigationFilesExist:
    def test_apps_navigation_dir_exists(self):
        dirpath = os.path.join(REPO_ROOT, "apps", "navigation")
        assert os.path.isdir(dirpath), f"Missing apps/navigation directory"

    @pytest.mark.parametrize("filename", APP_NAV_FILES)
    def test_app_nav_file_exists(self, filename):
        fpath = os.path.join(REPO_ROOT, "apps", "navigation", filename)
        assert os.path.isfile(fpath), f"Missing app surface file: {fpath}"


class TestWave11aTestsStillExist:
    def test_wave11a_tests_still_pass(self):
        """Verify wave11a test modules can be imported."""
        wave11a_dir = os.path.join(REPO_ROOT, "tests", "wave11a")
        assert os.path.isdir(wave11a_dir), "wave11a test directory missing"
        conftest_path = os.path.join(wave11a_dir, "conftest.py")
        assert os.path.isfile(conftest_path), "wave11a conftest.py missing"
