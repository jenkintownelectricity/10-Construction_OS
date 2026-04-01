#!/usr/bin/env python3
"""
trace_ingestor.py — Wave 3 Trace Bundle Ingestor for 10-Construction_OS

Ingests JSON trace bundles exported by OMNI-VIEW, validates them against
governance requirements, stages boundary records, and writes receipts.

Fail-closed semantics: any missing or invalid field causes immediate rejection
with exit code 1.

Usage:
    python tools/trace_ingestor.py <path_to_trace_bundle.json>

Dependencies: Python 3.8+ stdlib only (no external packages).
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_TRACE_TYPES = {"FOUNDATION_OUTLINE", "WALL_CENTERLINE"}
REQUIRED_FIELDS = [
    "trace_id",
    "source_tool",
    "trace_type",
    "units",
    "calibration",
    "polyline_points",
    "closed_status",
    "operator_confirmed",
]
REQUIRED_CALIBRATION_FIELDS = ["ppu", "unit"]

GOVERNANCE_KERNEL = "00-validkernel-governance"
GOVERNED_BY = "10-Construction_OS"
SOURCE_AUTHORITY = "OMNI-VIEW"
EXECUTED_BY = "trace_ingestor"

# Resolve repo root relative to this script's location (tools/ is one level deep)
REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BOUNDARIES_DIR = os.path.join(REPO_ROOT, "output", "boundaries")
RECEIPTS_DIR = os.path.join(REPO_ROOT, "receipts", "trace_ingestion")


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def load_bundle(path):
    """Load a trace bundle JSON file from disk. Fail-closed on any I/O or parse error."""
    if not os.path.isfile(path):
        fail(f"Trace bundle file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in trace bundle: {exc}")
    except OSError as exc:
        fail(f"Cannot read trace bundle: {exc}")


def validate_bundle(bundle):
    """Validate all governance-required fields. Returns a dict of sentinel check results.

    Raises SystemExit (via fail()) on first validation failure (fail-closed).
    """
    sentinels = {}

    # --- Required top-level fields ---
    for field in REQUIRED_FIELDS:
        if field not in bundle or bundle[field] is None:
            fail(f"Missing required field: {field}")
    sentinels["trace_id_present"] = True

    # --- trace_type ---
    if bundle["trace_type"] not in VALID_TRACE_TYPES:
        fail(f"Invalid trace_type: {bundle['trace_type']}. Must be one of {VALID_TRACE_TYPES}")
    sentinels["trace_type_valid"] = True

    # --- closed_status ---
    if bundle["closed_status"] is not True:
        fail("closed_status must be true")
    sentinels["closed_status_verified"] = True

    # --- calibration ---
    cal = bundle["calibration"]
    if not isinstance(cal, dict) or not cal:
        fail("calibration must be a non-empty object")
    for cf in REQUIRED_CALIBRATION_FIELDS:
        if cf not in cal or cal[cf] is None:
            fail(f"calibration missing required field: {cf}")
        if isinstance(cal[cf], str) and cal[cf].strip() == "":
            fail(f"calibration.{cf} must be non-empty")
    sentinels["calibration_verified"] = True

    # --- polyline_points ---
    pts = bundle["polyline_points"]
    if not isinstance(pts, list) or len(pts) < 3:
        fail("polyline_points must be a non-empty array with at least 3 points")
    sentinels["polyline_valid"] = True

    # --- operator_confirmed ---
    if bundle["operator_confirmed"] is not True:
        fail("operator_confirmed must be true")
    sentinels["operator_confirmed_verified"] = True

    return sentinels


# ---------------------------------------------------------------------------
# Hash & ID generation
# ---------------------------------------------------------------------------

def compute_geometry_hash(polyline_points):
    """Compute a SHA-256 hash over the sorted polyline_points JSON representation."""
    # Sort points for deterministic hashing (by x then y)
    sorted_pts = sorted(polyline_points, key=lambda p: (p.get("x", 0), p.get("y", 0)))
    canonical = json.dumps(sorted_pts, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def generate_boundary_id(trace_type, trace_id):
    """Generate a deterministic boundary_id from trace_type and trace_id."""
    combined = f"{trace_type}:{trace_id}"
    short_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()[:12]
    return f"bnd_{trace_type.lower()}_{short_hash}"


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_boundary(boundary):
    """Write the staged boundary JSON to output/boundaries/."""
    os.makedirs(BOUNDARIES_DIR, exist_ok=True)
    path = os.path.join(BOUNDARIES_DIR, f"{boundary['boundary_id']}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(boundary, fh, indent=2)
    return path


def write_receipt(receipt):
    """Write the ingestion receipt JSON to receipts/trace_ingestion/."""
    os.makedirs(RECEIPTS_DIR, exist_ok=True)
    path = os.path.join(RECEIPTS_DIR, f"{receipt['boundary_id']}_receipt.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)
    return path


# ---------------------------------------------------------------------------
# Core pipeline
# ---------------------------------------------------------------------------

def ingest(bundle_path):
    """Full ingestion pipeline: load, validate, hash, stage boundary, write receipt."""
    now = datetime.now(timezone.utc).isoformat()

    # 1. Load
    bundle = load_bundle(bundle_path)

    # 2. Validate (fail-closed)
    sentinels = validate_bundle(bundle)

    # 3. Compute geometry hash
    geometry_hash = compute_geometry_hash(bundle["polyline_points"])
    sentinels["geometry_hash_computed"] = True

    # 4. Generate boundary ID
    boundary_id = generate_boundary_id(bundle["trace_type"], bundle["trace_id"])

    # 5. Build staged boundary record
    boundary = {
        "boundary_id": boundary_id,
        "source_trace_id": bundle["trace_id"],
        "source_tool": bundle.get("source_tool", SOURCE_AUTHORITY),
        "source_file_ref": bundle.get("source_file_ref", ""),
        "trace_type": bundle["trace_type"],
        "units": bundle["units"],
        "calibration": bundle["calibration"],
        "polyline_points": bundle["polyline_points"],
        "geometry_hash": geometry_hash,
        "closed_status": True,
        "operator_confirmed": True,
        "status": "staged",
        "admitted_at": now,
        "lineage": {
            "source_trace_bundle": os.path.abspath(bundle_path),
            "source_authority": SOURCE_AUTHORITY,
            "governed_by": GOVERNED_BY,
            "governance_kernel": GOVERNANCE_KERNEL,
        },
    }

    # 6. Store boundary
    boundary_path = write_boundary(boundary)
    sentinels["boundary_stored"] = True
    print(f"[OK] Boundary staged: {boundary_path}")

    # 7. Relative paths for receipt references
    rel_boundary = os.path.relpath(boundary_path, REPO_ROOT)
    rel_receipt = os.path.join("receipts", "trace_ingestion", f"{boundary_id}_receipt.json")

    # 8. Build receipt
    receipt = {
        "receipt_id": f"receipt_trace_ingestion_{boundary_id}",
        "receipt_type": "trace_boundary_ingestion",
        "status": "success",
        "boundary_id": boundary_id,
        "source_trace_id": bundle["trace_id"],
        "trace_type": bundle["trace_type"],
        "governance_density": "full",
        "source_bundle_path": os.path.abspath(bundle_path),
        "output_boundary_path": rel_boundary,
        "output_receipt_path": rel_receipt,
        "evidence_summary": {
            "polyline_points_count": len(bundle["polyline_points"]),
            "geometry_hash": geometry_hash,
            "closed_status": True,
            "calibration_present": True,
            "operator_confirmed": True,
            "validation_passed": True,
        },
        "sentinel_checks": {
            **sentinels,
            "receipt_written": True,
        },
        "lineage": {
            "executed_at": now,
            "executed_by": EXECUTED_BY,
            "source_authority": SOURCE_AUTHORITY,
            "governed_by": GOVERNED_BY,
            "governance_kernel": GOVERNANCE_KERNEL,
        },
    }

    # 9. Write receipt
    receipt_path = write_receipt(receipt)
    print(f"[OK] Receipt written: {receipt_path}")
    print(f"[OK] Trace ingestion complete — boundary_id={boundary_id}")

    return boundary, receipt


# ---------------------------------------------------------------------------
# Fail-closed helper
# ---------------------------------------------------------------------------

def fail(message):
    """Print error and exit with code 1 (FAIL_CLOSED)."""
    print(f"[FAIL_CLOSED] {message}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """CLI entry point. Expects a single argument: path to trace bundle JSON."""
    if len(sys.argv) != 2:
        fail(f"Usage: {sys.argv[0]} <path_to_trace_bundle.json>")

    bundle_path = sys.argv[1]
    ingest(bundle_path)


if __name__ == "__main__":
    main()
