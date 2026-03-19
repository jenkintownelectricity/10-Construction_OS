"""
Construction OS — Intake & Review Application Surfaces (Wave 7)

Application layer for project intake, evidence ingestion, assembly
identity resolution, runtime triggering, and condition inspection.

This layer consumes governed construction truth from Construction_Kernel
and invokes the deterministic drawing runtime. It does not redefine
kernel truth, modify governed contracts, or change runtime pipeline behavior.

All outputs are derived, recomputable, and non-canonical.
"""
