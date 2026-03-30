"""
Cognitive Bus Event Emitter.

Transforms internal ResolutionResults into Cognitive Bus event envelopes.
Emits proposals, observations, and anomaly signals only.
May NOT emit execution commands or ExternallyValidatedEvent.

Advisory/proposal class only — explicitly encoded in every event.
"""

import uuid
from datetime import datetime, timezone

from engine.config import (
    SOURCE_COMPONENT,
    SOURCE_REPO,
    BUS_SCHEMA_VERSION,
    MAX_PAYLOAD_BYTES,
    ALLOWED_EVENT_CLASSES,
    FORBIDDEN_EVENT_CLASSES,
    STATUS_RESOLVED,
    STATUS_CONFLICT,
)

import json


def build_proposal_event(resolution_result: dict) -> dict:
    """
    Build a Cognitive Bus Proposal event from a ResolutionResult.

    The proposal is advisory only — it does not constitute an execution command.
    """
    _validate_not_forbidden("Proposal")

    status = resolution_result.get("status", "UNRESOLVED")

    # Determine event_type based on resolution depth
    if resolution_result.get("variant_id"):
        event_type = "variant_selection_proposal"
    elif resolution_result.get("pattern_id"):
        event_type = "pattern_resolution_proposal"
    elif resolution_result.get("artifact_intent_id"):
        event_type = "artifact_intent_proposal"
    else:
        event_type = "pattern_resolution_proposal"

    payload = {
        "condition_id": resolution_result.get("condition_id", ""),
        "result_id": resolution_result.get("result_id", ""),
        "status": status,
        "advisory_class": "proposal",
        "pattern_family_id": resolution_result.get("pattern_family_id"),
        "pattern_id": resolution_result.get("pattern_id"),
        "variant_id": resolution_result.get("variant_id"),
        "artifact_intent_id": resolution_result.get("artifact_intent_id"),
        "score": resolution_result.get("score"),
        "fail_reasons": resolution_result.get("fail_reasons", []),
        "conflicts": resolution_result.get("conflicts", []),
        "correlation_refs": resolution_result.get("correlation_refs", []),
    }

    event = _build_envelope("Proposal", event_type, payload)
    _validate_payload_size(event)
    return event


def build_observation_event(
    resolution_result: dict,
    observation_type: str = None,
    severity: str = "info",
    detail: str = None,
) -> dict:
    """
    Build a Cognitive Bus Observation event from a ResolutionResult.

    Observations report state — they are not commands.
    """
    _validate_not_forbidden("Observation")

    status = resolution_result.get("status", "UNRESOLVED")

    if observation_type is None:
        if status == STATUS_CONFLICT:
            observation_type = "conflict"
        elif resolution_result.get("constraint_violations"):
            observation_type = "constraint_violation"
        elif resolution_result.get("fail_reasons"):
            for fr in resolution_result["fail_reasons"]:
                if fr.get("code") == "MISSING_TRUTH":
                    observation_type = "missing_truth"
                    break
            if observation_type is None:
                observation_type = "blocked_condition"
        else:
            observation_type = "resolution_status"

    affected = []
    if resolution_result.get("pattern_family_id"):
        affected.append(resolution_result["pattern_family_id"])
    if resolution_result.get("pattern_id"):
        affected.append(resolution_result["pattern_id"])
    if resolution_result.get("variant_id"):
        affected.append(resolution_result["variant_id"])

    payload = {
        "observation_type": observation_type,
        "advisory_class": "observation",
        "condition_id": resolution_result.get("condition_id", ""),
        "result_id": resolution_result.get("result_id", ""),
        "detail": detail or f"Resolution status: {status}",
        "affected_entities": affected,
        "severity": severity,
        "correlation_refs": resolution_result.get("correlation_refs", []),
    }

    event = _build_envelope("Observation", f"{observation_type}_observed" if not observation_type.endswith("_observed") else observation_type, payload)
    _validate_payload_size(event)
    return event


def build_anomaly_event(
    condition_id: str,
    anomaly_detail: str,
    affected_entities: list = None,
    severity: str = "warning",
    correlation_refs: list = None,
) -> dict:
    """
    Build a Cognitive Bus Observation event for an anomaly.

    Anomalies are observations, not execution commands.
    """
    _validate_not_forbidden("Observation")

    payload = {
        "observation_type": "anomaly",
        "advisory_class": "observation",
        "condition_id": condition_id,
        "detail": anomaly_detail,
        "affected_entities": affected_entities or [],
        "severity": severity,
        "correlation_refs": correlation_refs or [],
    }

    event = _build_envelope("Observation", "anomaly_detected", payload)
    _validate_payload_size(event)
    return event


def _build_envelope(event_class: str, event_type: str, payload: dict) -> dict:
    """Build a Cognitive Bus event envelope."""
    return {
        "event_id": f"evt-{uuid.uuid4().hex}",
        "event_class": event_class,
        "event_type": event_type,
        "schema_version": BUS_SCHEMA_VERSION,
        "source_component": SOURCE_COMPONENT,
        "source_repo": SOURCE_REPO,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }


def _validate_not_forbidden(event_class: str) -> None:
    """Fail closed if attempting to emit a forbidden event class."""
    if event_class in FORBIDDEN_EVENT_CLASSES:
        raise ValueError(
            f"ALEXANDER Engine may NOT emit {event_class} events. "
            f"Allowed: {sorted(ALLOWED_EVENT_CLASSES)}"
        )
    if event_class not in ALLOWED_EVENT_CLASSES:
        raise ValueError(
            f"Unknown event class: {event_class}. "
            f"Allowed: {sorted(ALLOWED_EVENT_CLASSES)}"
        )


def _validate_payload_size(event: dict) -> None:
    """Fail closed if payload exceeds max size."""
    payload_bytes = len(json.dumps(event.get("payload", {})).encode("utf-8"))
    if payload_bytes > MAX_PAYLOAD_BYTES:
        raise ValueError(
            f"Payload size {payload_bytes} bytes exceeds maximum {MAX_PAYLOAD_BYTES} bytes"
        )
