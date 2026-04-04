"""
Extraction Worker — Wave 1 Guaranteed Detail Engine
Main entrypoint: claims an ingest job from Supabase, dispatches extraction,
writes results back. Supports local-file mode for testing without Supabase.

Usage
-----
  # Supabase mode (env vars SUPABASE_URL and SUPABASE_SERVICE_KEY must be set):
  python -m workers.extraction_worker

  # Local-file mode (no Supabase required):
  python -m workers.extraction_worker --local /path/to/file.dxf
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone

import requests

from workers.file_dispatcher import dispatch


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKER_ID = f"worker-{uuid.uuid4().hex[:8]}"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")

_HEADERS = {}


def _init_headers():
    global _HEADERS
    _HEADERS = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _supabase_configured():
    return bool(SUPABASE_URL) and bool(SUPABASE_KEY)


def _utcnow():
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Supabase helpers
# ---------------------------------------------------------------------------

def _rest_url(table, query_params=""):
    """Build the PostgREST URL for a table."""
    base = SUPABASE_URL.rstrip("/")
    url = f"{base}/rest/v1/{table}"
    if query_params:
        url = f"{url}?{query_params}"
    return url


def _claim_job():
    """
    Find a job with processing_status='uploaded', atomically set it to 'claimed'.
    Returns the job row dict or None.
    """
    # Step 1: find one uploaded job (oldest first)
    select_url = _rest_url(
        "ingest_jobs",
        "processing_status=eq.uploaded&order=uploaded_at_utc.asc&limit=1",
    )
    resp = requests.get(select_url, headers=_HEADERS, timeout=15)
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        return None

    job = rows[0]
    job_id = job["id"]

    # Step 2: claim it — PATCH with filter to avoid races
    patch_url = _rest_url("ingest_jobs", f"id=eq.{job_id}&processing_status=eq.uploaded")
    payload = {
        "processing_status": "claimed",
        "worker_id": WORKER_ID,
        "claimed_at_utc": _utcnow(),
    }
    resp = requests.patch(patch_url, headers=_HEADERS, json=payload, timeout=15)
    resp.raise_for_status()
    updated = resp.json()
    if not updated:
        # Another worker grabbed it first — try again or return None
        return None

    return updated[0]


def _download_file(job):
    """
    Download the file from Supabase Storage and return a local temp path.
    """
    bucket = job.get("storage_bucket", "")
    obj_path = job.get("storage_object_path", "")
    if not bucket or not obj_path:
        raise ValueError("Missing storage_bucket or storage_object_path on ingest_job")

    base = SUPABASE_URL.rstrip("/")
    download_url = f"{base}/storage/v1/object/{bucket}/{obj_path}"
    resp = requests.get(
        download_url,
        headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
        timeout=60,
    )
    resp.raise_for_status()

    # Write to a temp file preserving the original extension
    filename = job.get("filename", "download")
    tmp_dir = "/tmp/extraction_worker"
    os.makedirs(tmp_dir, exist_ok=True)
    local_path = os.path.join(tmp_dir, f"{job['id']}_{filename}")
    with open(local_path, "wb") as f:
        f.write(resp.content)

    return local_path


def _write_result(job_id, result):
    """Update the ingest_job row with extraction results."""
    status = result.get("extraction_status", "failed")

    # Map extraction_status to processing_status
    if status in ("extracted", "evidence_only"):
        processing_status = "extracted"
    elif status == "partial":
        processing_status = "partial"
    elif status == "halted":
        processing_status = "halted"
    else:
        processing_status = "failed"

    payload = {
        "processing_status": processing_status,
        "extraction_status": status,
        "entity_count": result.get("entity_count", 0),
        "file_type": result.get("file_type", "unknown"),
        "extracted_at_utc": result.get("extracted_at_utc", _utcnow()),
        "extraction_summary": json.loads(json.dumps(result)),  # ensure serialisable
    }

    if result.get("halt_reason"):
        payload["halt_reason"] = result["halt_reason"]

    patch_url = _rest_url("ingest_jobs", f"id=eq.{job_id}")
    resp = requests.patch(patch_url, headers=_HEADERS, json=payload, timeout=15)
    resp.raise_for_status()


def _fail_job(job_id, reason):
    """Mark a job as failed with a halt_reason."""
    payload = {
        "processing_status": "failed",
        "extraction_status": "failed",
        "halt_reason": str(reason),
        "extracted_at_utc": _utcnow(),
    }
    try:
        patch_url = _rest_url("ingest_jobs", f"id=eq.{job_id}")
        requests.patch(patch_url, headers=_HEADERS, json=payload, timeout=15)
    except Exception:
        # Best-effort — if this also fails we still want the outer error to surface
        pass


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run_supabase_mode():
    """Claim one job from Supabase, extract, write results."""
    _init_headers()

    job = _claim_job()
    if job is None:
        print(f"[{WORKER_ID}] No uploaded jobs found. Exiting.")
        return

    job_id = job["id"]
    print(f"[{WORKER_ID}] Claimed job {job_id} — {job.get('filename', '?')}")

    try:
        local_path = _download_file(job)
        print(f"[{WORKER_ID}] Downloaded to {local_path}")

        result = dispatch(local_path, ingest_job_id=job_id)
        print(f"[{WORKER_ID}] Extraction status={result['extraction_status']}  "
              f"entities={result.get('entity_count', 0)}")

        _write_result(job_id, result)
        print(f"[{WORKER_ID}] Results written for job {job_id}")

    except Exception as ex:
        print(f"[{WORKER_ID}] ERROR on job {job_id}: {ex}", file=sys.stderr)
        _fail_job(job_id, str(ex))


def run_local_mode(file_path):
    """Extract a local file without Supabase. Prints result JSON to stdout."""
    fake_job_id = str(uuid.uuid4())
    print(f"[local] Processing {file_path}  (fake job_id={fake_job_id})")

    try:
        result = dispatch(file_path, ingest_job_id=fake_job_id)
    except Exception as ex:
        result = {
            "extraction_id": str(uuid.uuid4()),
            "ingest_job_id": fake_job_id,
            "file_type": "unknown",
            "extraction_status": "failed",
            "entity_count": 0,
            "entities": [],
            "source_file": str(file_path),
            "halt_reason": str(ex),
            "extracted_at_utc": _utcnow(),
        }

    print(json.dumps(result, indent=2))
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Extraction Worker — Guaranteed Detail Engine")
    parser.add_argument(
        "--local",
        metavar="FILE",
        help="Run in local-file mode: extract a file on disk without Supabase.",
    )
    args = parser.parse_args()

    if args.local:
        run_local_mode(args.local)
    elif _supabase_configured():
        try:
            run_supabase_mode()
        except Exception as ex:
            print(f"[{WORKER_ID}] FATAL: {ex}", file=sys.stderr)
            sys.exit(1)
    else:
        print(
            "ERROR: Supabase not configured. Set SUPABASE_URL and SUPABASE_SERVICE_KEY,\n"
            "       or use --local <FILE> for local testing.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
