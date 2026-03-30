"""
Project Intake

Ingests project-level data: building systems, assemblies, materials,
and scope assignments. Produces structured project records that can
be fed to evidence ingestion and identity resolution.

This module does not redefine kernel truth or modify governed contracts.
All project records are derived representations, not canonical truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProjectRecord:
    """Derived project representation. Non-canonical, recomputable."""

    project_id: str = ""
    building_systems: list[dict[str, Any]] = field(default_factory=list)
    assemblies: list[dict[str, Any]] = field(default_factory=list)
    materials: list[str] = field(default_factory=list)
    scope_assignments: list[dict[str, Any]] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)


def ingest_project(project_data: dict[str, Any]) -> ProjectRecord:
    """
    Ingest raw project data and produce a structured project record.

    Fail-closed: rejects incomplete or ambiguous project data.
    All output is derived and non-canonical.
    """
    record = ProjectRecord()

    if not isinstance(project_data, dict):
        record.errors.append({
            "code": "INVALID_PROJECT_DATA",
            "message": "Project data must be a dict.",
        })
        return record

    record.project_id = project_data.get("project_id", "")
    if not record.project_id:
        record.errors.append({
            "code": "MISSING_PROJECT_ID",
            "message": "Project data must include a project_id.",
        })
        return record

    # Extract building systems
    systems = project_data.get("building_systems", [])
    if not isinstance(systems, list) or len(systems) == 0:
        record.errors.append({
            "code": "MISSING_BUILDING_SYSTEMS",
            "message": "Project must declare at least one building system.",
        })
        return record

    record.building_systems = systems

    # Extract assemblies
    record.assemblies = project_data.get("assemblies", [])

    # Extract materials
    record.materials = project_data.get("materials", [])

    # Extract scope assignments
    record.scope_assignments = project_data.get("scope_assignments", [])

    return record
