"""Runtime logger v0.2.

Append-only audit logging with structured events including:
timestamp, pipeline_id, run_id, stage, event_type, severity,
error_code, message, input/output refs and hashes, schema_version.
"""

import hashlib
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "0.2"

# Event types
PIPELINE_STARTED = "PIPELINE_STARTED"
PARSE_COMPLETED = "PARSE_COMPLETED"
VALIDATION_FAILED = "VALIDATION_FAILED"
VALIDATION_PASSED = "VALIDATION_PASSED"
GEOMETRY_COMPLETED = "GEOMETRY_COMPLETED"
GENERATION_COMPLETED = "GENERATION_COMPLETED"
DELIVERABLE_EMITTED = "DELIVERABLE_EMITTED"
ENGINE_COMPLETED = "ENGINE_COMPLETED"
PIPELINE_COMPLETED = "PIPELINE_COMPLETED"
PIPELINE_ABORTED = "PIPELINE_ABORTED"


def _compute_hash(data: Any) -> str:
    """Compute a SHA-256 hash of data for audit trail."""
    return hashlib.sha256(str(data).encode()).hexdigest()[:16]


class RuntimeLogger:
    """Append-only audit logger for Construction Runtime.

    v0.2: Each event includes full audit metadata.
    Backward-compatible: v0.1 log methods still work.
    """

    def __init__(self, name: str = "construction_runtime", pipeline_id: str = ""):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.DEBUG)

        self._events: list[dict[str, Any]] = []
        self.pipeline_id = pipeline_id or str(uuid.uuid4())[:8]
        self.run_id = str(uuid.uuid4())[:8]

    def _append_event(
        self,
        stage: str,
        event_type: str,
        severity: str,
        message: str,
        error_code: str = "",
        input_ref: str = "",
        output_ref: str = "",
        input_hash: str = "",
        output_hash: str = "",
    ) -> dict[str, Any]:
        """Append a structured audit event."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pipeline_id": self.pipeline_id,
            "run_id": self.run_id,
            "stage": stage,
            "event_type": event_type,
            "severity": severity,
            "error_code": error_code,
            "message": message,
            "input_ref": input_ref,
            "output_ref": output_ref,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "schema_version": SCHEMA_VERSION,
        }
        self._events.append(event)
        log_level = {"info": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR}.get(severity, logging.INFO)
        self._logger.log(log_level, "[%s] %s: %s", event_type, stage, message)
        return event

    # ── v0.2 structured methods ──────────────────────────

    def log_pipeline_started(self, input_type: str, input_data: Any = None) -> None:
        self._append_event(
            stage="pipeline", event_type=PIPELINE_STARTED, severity="info",
            message=f"Pipeline started for input_type={input_type}",
            input_hash=_compute_hash(input_data) if input_data else "",
        )

    def log_parse_completed(self, parser_name: str, output: Any = None) -> None:
        self._append_event(
            stage="parse", event_type=PARSE_COMPLETED, severity="info",
            message=f"Parse completed: {parser_name}",
            output_hash=_compute_hash(output) if output else "",
        )

    def log_validation_result(self, stage: str, is_valid: bool, errors: list = None) -> None:
        event_type = VALIDATION_PASSED if is_valid else VALIDATION_FAILED
        severity = "info" if is_valid else "warning"
        error_code = ""
        if errors:
            error_code = errors[0].get("code", "") if isinstance(errors[0], dict) else str(errors[0])
        self._append_event(
            stage=f"validation.{stage}", event_type=event_type, severity=severity,
            message=f"Validation {stage}: valid={is_valid}, error_count={len(errors or [])}",
            error_code=error_code,
        )

    def log_geometry_completed(self, output: Any = None) -> None:
        self._append_event(
            stage="geometry", event_type=GEOMETRY_COMPLETED, severity="info",
            message="Geometry engine completed.",
            output_hash=_compute_hash(output) if output else "",
        )

    def log_generation_completed(self, deliverable_type: str, output: Any = None) -> None:
        self._append_event(
            stage="generation", event_type=GENERATION_COMPLETED, severity="info",
            message=f"Generation completed: {deliverable_type}",
            output_hash=_compute_hash(output) if output else "",
        )

    def log_deliverable_emitted(self, deliverable_id: str, formats: list[str] = None) -> None:
        self._append_event(
            stage="deliverable", event_type=DELIVERABLE_EMITTED, severity="info",
            message=f"Deliverable emitted: {deliverable_id}, formats={formats or []}",
            output_ref=deliverable_id,
        )

    def log_pipeline_completed(self) -> None:
        self._append_event(
            stage="pipeline", event_type=PIPELINE_COMPLETED, severity="info",
            message="Pipeline completed successfully.",
        )

    def log_pipeline_aborted(self, reason: str, error_code: str = "") -> None:
        self._append_event(
            stage="pipeline", event_type=PIPELINE_ABORTED, severity="error",
            message=f"Pipeline aborted: {reason}",
            error_code=error_code,
        )

    # ── v0.1 backward-compatible methods ─────────────────

    def log_parser_event(self, parser_name: str, status: str, details: str = "") -> None:
        self._append_event(
            stage="parse", event_type=PARSE_COMPLETED, severity="info",
            message=f"Parser [{parser_name}]: {status} — {details}",
        )

    def log_validation(self, is_valid: bool, warnings: list[str], errors: list[str]) -> None:
        severity = "info" if is_valid else "warning"
        event_type = VALIDATION_PASSED if is_valid else VALIDATION_FAILED
        self._append_event(
            stage="validation", event_type=event_type, severity=severity,
            message=f"Validation: valid={is_valid}, warnings={len(warnings)}, errors={len(errors)}",
        )

    def log_engine_action(self, engine_name: str, action: str, details: str = "") -> None:
        self._append_event(
            stage="engine", event_type=ENGINE_COMPLETED, severity="info",
            message=f"Engine [{engine_name}]: {action} — {details}",
        )

    def log_generation(self, deliverable_type: str, status: str, details: str = "") -> None:
        self._append_event(
            stage="generation", event_type=GENERATION_COMPLETED, severity="info",
            message=f"Generator [{deliverable_type}]: {status} — {details}",
        )

    def log_pipeline(self, step: str, status: str, details: str = "") -> None:
        self._append_event(
            stage="pipeline", event_type=PIPELINE_STARTED if status == "start" else PIPELINE_COMPLETED,
            severity="info",
            message=f"Pipeline [{step}]: {status} — {details}",
        )

    def get_events(self) -> list[dict[str, Any]]:
        """Return all logged events (append-only, no mutation)."""
        return list(self._events)
