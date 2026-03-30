"""
Seam Governance Tests

Verifies the seam manifest exists and declares required seams.
Runtime does NOT depend on the seam manifest for execution.
These tests verify governance metadata only.
"""

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# Resolve path to Construction_Kernel contracts
_KERNEL_CONTRACTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "Construction_Kernel", "contracts"
)


class TestSeamManifestExists:
    """Verify seam manifest exists and is well-formed."""

    def _load_manifest(self):
        manifest_path = os.path.join(_KERNEL_CONTRACTS_PATH, "seams", "seam_manifest.json")
        assert os.path.exists(manifest_path), (
            f"Seam manifest missing: {manifest_path}"
        )
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_seam_manifest_present(self):
        """seam_manifest.json must exist in Construction_Kernel."""
        manifest = self._load_manifest()
        assert isinstance(manifest, dict)
        assert "seams" in manifest

    def test_required_seams_declared(self):
        """All three required seams must be declared."""
        manifest = self._load_manifest()
        seam_ids = {s["seam_id"] for s in manifest["seams"]}
        assert "detail_applicability" in seam_ids
        assert "detail_schema" in seam_ids
        assert "drawing_instruction_ir" in seam_ids

    def test_seam_fields_complete(self):
        """Every seam must have all required fields."""
        manifest = self._load_manifest()
        required_fields = {
            "seam_id", "authority_repo", "authority_artifacts",
            "consumer_repo", "consumer_modules", "version_policy",
            "canonicality", "fail_mode", "seam_status",
        }
        for seam in manifest["seams"]:
            missing = required_fields - set(seam.keys())
            assert not missing, (
                f"Seam '{seam.get('seam_id')}' missing fields: {missing}"
            )

    def test_all_seams_owned_by_kernel(self):
        """Every seam must declare Construction_Kernel as authority."""
        manifest = self._load_manifest()
        for seam in manifest["seams"]:
            assert seam["authority_repo"] == "Construction_Kernel", (
                f"Seam '{seam['seam_id']}' authority is '{seam['authority_repo']}', "
                f"expected 'Construction_Kernel'"
            )

    def test_all_seams_fail_closed(self):
        """Every seam must declare fail_closed fail mode."""
        manifest = self._load_manifest()
        for seam in manifest["seams"]:
            assert seam["fail_mode"] == "fail_closed", (
                f"Seam '{seam['seam_id']}' fail_mode is '{seam['fail_mode']}', "
                f"expected 'fail_closed'"
            )

    def test_authority_artifact_paths_valid(self):
        """All declared authority artifact paths must exist in Construction_Kernel."""
        manifest = self._load_manifest()
        kernel_root = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "Construction_Kernel"
        )
        for seam in manifest["seams"]:
            for artifact_path in seam["authority_artifacts"]:
                full_path = os.path.join(kernel_root, artifact_path)
                assert os.path.exists(full_path), (
                    f"Seam '{seam['seam_id']}' artifact missing: {artifact_path}"
                )

    def test_seam_status_valid(self):
        """All seam statuses must be valid lifecycle states."""
        manifest = self._load_manifest()
        valid_states = {"draft", "active", "frozen", "deprecated"}
        for seam in manifest["seams"]:
            assert seam["seam_status"] in valid_states, (
                f"Seam '{seam['seam_id']}' status '{seam['seam_status']}' "
                f"not in {valid_states}"
            )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
