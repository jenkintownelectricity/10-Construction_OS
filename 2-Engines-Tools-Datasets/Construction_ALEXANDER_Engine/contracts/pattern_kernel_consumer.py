"""
Pattern Kernel Consumer Contract.

Reads governed pattern truth from Construction_Pattern_Language_OS.
This contract consumes canonical IDs and never mutates the kernel.

Consumer only — ALEXANDER may not define new canonical truth.
"""

import json
import os
import re
from pathlib import Path
from typing import Optional

import yaml

from engine.config import (
    PATTERN_LANGUAGE_OS_DIR,
    FAMILY_ID_PATTERN,
    PATTERN_ID_PATTERN,
    VARIANT_ID_PATTERN,
    ARTIFACT_ID_PATTERN,
    CONSTRAINT_ID_PATTERN,
    RELATIONSHIP_ID_PATTERN,
)


def _load_yaml(path: Path) -> dict:
    """Load a YAML file. Fail closed on any error."""
    if not path.exists():
        raise FileNotFoundError(f"Kernel file not found: {path}")
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Kernel file is not a valid YAML dict: {path}")
    return data


def _load_json(path: Path) -> dict:
    """Load a JSON file. Fail closed on any error."""
    if not path.exists():
        raise FileNotFoundError(f"Kernel file not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Kernel file is not a valid JSON dict: {path}")
    return data


def _load_file(path: Path) -> dict:
    """Load YAML or JSON based on extension."""
    suffix = path.suffix.lower()
    if suffix in (".yaml", ".yml"):
        return _load_yaml(path)
    elif suffix == ".json":
        return _load_json(path)
    else:
        raise ValueError(f"Unsupported kernel file format: {suffix}")


def _scan_directory(directory: Path) -> list:
    """Scan a directory for YAML/JSON files and load them all."""
    results = []
    if not directory.exists():
        return results
    for entry in sorted(directory.iterdir()):
        if entry.is_file() and entry.suffix.lower() in (".yaml", ".yml", ".json"):
            try:
                results.append(_load_file(entry))
            except (ValueError, json.JSONDecodeError, yaml.YAMLError):
                continue  # skip malformed files but don't crash
        elif entry.is_dir():
            results.extend(_scan_directory(entry))
    return results


def _validate_id(entity_id: str, pattern: str, entity_type: str) -> None:
    """Validate a canonical ID against its expected pattern. Fail closed."""
    if not isinstance(entity_id, str) or not re.match(pattern, entity_id):
        raise ValueError(
            f"Invalid {entity_type} canonical ID: {entity_id!r} "
            f"(expected pattern: {pattern})"
        )


class PatternKernelConsumer:
    """
    Read-only consumer of Construction_Pattern_Language_OS.

    Loads pattern families, patterns, variants, artifact intents,
    constraint profiles, and pattern relationships from the kernel.
    All access is read-only. All IDs are validated against canonical formats.
    """

    def __init__(self, kernel_dir: Optional[Path] = None):
        self._kernel_dir = kernel_dir or PATTERN_LANGUAGE_OS_DIR
        self._families: dict = {}
        self._patterns: dict = {}
        self._variants: dict = {}
        self._artifact_intents: dict = {}
        self._constraint_profiles: dict = {}
        self._relationships: dict = {}
        self._loaded = False

    def load(self) -> None:
        """Load all kernel entities. Fail closed if kernel dir missing."""
        if not self._kernel_dir.exists():
            raise FileNotFoundError(
                f"Pattern Language OS kernel not found at: {self._kernel_dir}"
            )

        # Load pattern families and their children
        families_dir = self._kernel_dir / "pattern_language"
        for family_data in _scan_directory(families_dir):
            fid = family_data.get("id", "")
            if re.match(FAMILY_ID_PATTERN, fid):
                self._families[fid] = family_data
            elif re.match(PATTERN_ID_PATTERN, fid):
                self._patterns[fid] = family_data
            elif re.match(VARIANT_ID_PATTERN, fid):
                self._variants[fid] = family_data

        # Load artifact intents
        artifacts_dir = self._kernel_dir / "artifact_intents"
        for art_data in _scan_directory(artifacts_dir):
            aid = art_data.get("id", "")
            if re.match(ARTIFACT_ID_PATTERN, aid):
                self._artifact_intents[aid] = art_data

        # Load constraint profiles
        constraints_dir = self._kernel_dir / "constraint_profiles"
        for cns_data in _scan_directory(constraints_dir):
            cid = cns_data.get("id", "")
            if re.match(CONSTRAINT_ID_PATTERN, cid):
                self._constraint_profiles[cid] = cns_data

        # Load pattern relationships
        rels_dir = self._kernel_dir / "pattern_relationships"
        for rel_data in _scan_directory(rels_dir):
            rid = rel_data.get("id", "")
            if re.match(RELATIONSHIP_ID_PATTERN, rid):
                self._relationships[rid] = rel_data

        self._loaded = True

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            raise RuntimeError("Kernel not loaded. Call load() first.")

    def get_all_families(self) -> dict:
        self._ensure_loaded()
        return dict(self._families)

    def get_family(self, family_id: str) -> Optional[dict]:
        self._ensure_loaded()
        _validate_id(family_id, FAMILY_ID_PATTERN, "PatternFamily")
        return self._families.get(family_id)

    def get_families_by_domain_key(self, domain_key: str) -> list:
        """Find families whose ID contains the given domain key (e.g., 'EDGE')."""
        self._ensure_loaded()
        return [
            f for fid, f in self._families.items()
            if domain_key.upper() in fid.upper()
        ]

    def get_all_patterns(self) -> dict:
        self._ensure_loaded()
        return dict(self._patterns)

    def get_pattern(self, pattern_id: str) -> Optional[dict]:
        self._ensure_loaded()
        _validate_id(pattern_id, PATTERN_ID_PATTERN, "Pattern")
        return self._patterns.get(pattern_id)

    def get_patterns_for_family(self, family_id: str) -> list:
        """Get all patterns belonging to a family."""
        self._ensure_loaded()
        _validate_id(family_id, FAMILY_ID_PATTERN, "PatternFamily")
        family = self._families.get(family_id)
        if not family:
            return []
        pattern_ids = family.get("patterns", [])
        results = []
        for pid in pattern_ids:
            pid_str = pid if isinstance(pid, str) else pid.get("id", "") if isinstance(pid, dict) else ""
            pat = self._patterns.get(pid_str)
            if pat:
                results.append(pat)
        return results

    def get_all_variants(self) -> dict:
        self._ensure_loaded()
        return dict(self._variants)

    def get_variant(self, variant_id: str) -> Optional[dict]:
        self._ensure_loaded()
        _validate_id(variant_id, VARIANT_ID_PATTERN, "PatternVariant")
        return self._variants.get(variant_id)

    def get_variants_for_pattern(self, pattern_id: str) -> list:
        """Get all variants belonging to a pattern."""
        self._ensure_loaded()
        _validate_id(pattern_id, PATTERN_ID_PATTERN, "Pattern")
        pattern = self._patterns.get(pattern_id)
        if not pattern:
            return []
        variant_ids = pattern.get("variants", [])
        results = []
        for vid in variant_ids:
            vid_str = vid if isinstance(vid, str) else vid.get("id", "") if isinstance(vid, dict) else ""
            var = self._variants.get(vid_str)
            if var:
                results.append(var)
        return results

    def get_artifact_intent(self, artifact_id: str) -> Optional[dict]:
        self._ensure_loaded()
        _validate_id(artifact_id, ARTIFACT_ID_PATTERN, "ArtifactIntent")
        return self._artifact_intents.get(artifact_id)

    def get_artifact_intents_for_pattern(self, pattern_id: str) -> list:
        """Get artifact intents referencing a pattern."""
        self._ensure_loaded()
        results = []
        for art in self._artifact_intents.values():
            refs = art.get("pattern_refs", [])
            for ref in refs:
                ref_id = ref if isinstance(ref, str) else ref.get("id", "") if isinstance(ref, dict) else ""
                if ref_id == pattern_id:
                    results.append(art)
                    break
        return results

    def get_constraint_profile(self, constraint_id: str) -> Optional[dict]:
        self._ensure_loaded()
        _validate_id(constraint_id, CONSTRAINT_ID_PATTERN, "ConstraintProfile")
        return self._constraint_profiles.get(constraint_id)

    def get_constraints_for_pattern(self, pattern_id: str) -> list:
        """Get constraint profiles applying to a pattern or its family."""
        self._ensure_loaded()
        results = []
        for cns in self._constraint_profiles.values():
            applies = cns.get("applies_to", [])
            for ref in applies:
                ref_id = ref if isinstance(ref, str) else ref.get("id", "") if isinstance(ref, dict) else ""
                if ref_id == pattern_id:
                    results.append(cns)
                    break
        return results

    def get_constraints_for_family(self, family_id: str) -> list:
        """Get constraint profiles applying to a family."""
        self._ensure_loaded()
        results = []
        for cns in self._constraint_profiles.values():
            applies = cns.get("applies_to", [])
            for ref in applies:
                ref_id = ref if isinstance(ref, str) else ref.get("id", "") if isinstance(ref, dict) else ""
                if ref_id == family_id:
                    results.append(cns)
                    break
        return results

    def get_all_relationships(self) -> dict:
        self._ensure_loaded()
        return dict(self._relationships)

    def get_relationships_for_entity(self, entity_id: str) -> list:
        """Get all relationships where entity is source or target."""
        self._ensure_loaded()
        results = []
        for rel in self._relationships.values():
            src = rel.get("source", {})
            tgt = rel.get("target", {})
            src_id = src.get("id", "") if isinstance(src, dict) else str(src)
            tgt_id = tgt.get("id", "") if isinstance(tgt, dict) else str(tgt)
            if entity_id in (src_id, tgt_id):
                results.append(rel)
        return results

    def get_conflicts_for_entity(self, entity_id: str) -> list:
        """Get conflict relationships for an entity."""
        return [
            r for r in self.get_relationships_for_entity(entity_id)
            if r.get("type") == "conflict" or r.get("relationship_type") == "conflict"
        ]

    def get_dependencies_for_entity(self, entity_id: str) -> list:
        """Get dependency relationships for an entity."""
        return [
            r for r in self.get_relationships_for_entity(entity_id)
            if r.get("type") == "dependency" or r.get("relationship_type") == "dependency"
        ]
