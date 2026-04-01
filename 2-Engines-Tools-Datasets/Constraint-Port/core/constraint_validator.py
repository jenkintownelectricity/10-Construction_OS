"""Constraint Validator.

Deterministic validation helpers for ConstraintObject, ConstraintEvidence,
and ConstraintDecision dicts. All checks reference the authoritative schema
constants defined in constraint_types.py.

Boundary rules:
- Validation only — no mutation, no execution
- Fail-closed: any invalid data returns errors
- Deterministic: same input always produces same output
"""

from __future__ import annotations

import re
from typing import Any

from core.constraint_types import (
    CONSTRAINT_TYPES,
    LOGIC_OPERATORS,
    DECISION_ACTIONS,
    SEVERITIES,
    EVIDENCE_COMPLETENESS_VALUES,
    ENTITY_TYPES,
    DECISION_ON_FAIL_VALUES,
    CONSTRAINT_OBJECT_REQUIRED_FIELDS,
    CONSTRAINT_EVIDENCE_REQUIRED_FIELDS,
    CONSTRAINT_DECISION_REQUIRED_FIELDS,
)

_RULE_ID_PATTERN = re.compile(r"^CR-[A-Z0-9]+-[0-9]+$")
_EVIDENCE_ID_PATTERN = re.compile(r"^EV-[A-Z0-9]+-[0-9]+$")
_DECISION_ID_PATTERN = re.compile(r"^CD-[A-Z0-9]+-[0-9]+$")


def validate_constraint_object(obj: Any) -> list[dict[str, str]]:
    """Validate a ConstraintObject dict against the authoritative schema.

    Returns list of error dicts. Empty list means valid.
    """
    errors: list[dict[str, str]] = []

    if not isinstance(obj, dict):
        return [{"code": "INVALID_TYPE", "message": f"ConstraintObject must be dict, got {type(obj).__name__}"}]

    for field_name in CONSTRAINT_OBJECT_REQUIRED_FIELDS:
        if field_name not in obj:
            errors.append({"code": "MISSING_FIELD", "message": f"Missing required field: '{field_name}'"})

    rule_id = obj.get("rule_id")
    if rule_id is not None and (not isinstance(rule_id, str) or not _RULE_ID_PATTERN.match(rule_id)):
        errors.append({"code": "INVALID_FORMAT", "message": f"rule_id '{rule_id}' must match '^CR-[A-Z0-9]+-[0-9]+$'"})

    ct = obj.get("constraint_type")
    if ct is not None and ct not in CONSTRAINT_TYPES:
        errors.append({"code": "INVALID_ENUM", "message": f"constraint_type '{ct}' not in {sorted(CONSTRAINT_TYPES)}"})

    lo = obj.get("logic_operator")
    if lo is not None and lo not in LOGIC_OPERATORS:
        errors.append({"code": "INVALID_ENUM", "message": f"logic_operator '{lo}' not in {sorted(LOGIC_OPERATORS)}"})

    dof = obj.get("decision_on_fail")
    if dof is not None and dof not in DECISION_ON_FAIL_VALUES:
        errors.append({"code": "INVALID_ENUM", "message": f"decision_on_fail '{dof}' not in {sorted(DECISION_ON_FAIL_VALUES)}"})

    applies_to = obj.get("applies_to")
    if applies_to is not None:
        if isinstance(applies_to, dict):
            et = applies_to.get("entity_type")
            if et is None:
                errors.append({"code": "MISSING_FIELD", "message": "applies_to.entity_type is required"})
            elif et not in ENTITY_TYPES:
                errors.append({"code": "INVALID_ENUM", "message": f"applies_to.entity_type '{et}' not in {sorted(ENTITY_TYPES)}"})
        else:
            errors.append({"code": "INVALID_TYPE", "message": "applies_to must be a dict"})

    trigger = obj.get("trigger")
    if trigger is not None:
        if isinstance(trigger, dict):
            if "condition" not in trigger:
                errors.append({"code": "MISSING_FIELD", "message": "trigger.condition is required"})
        else:
            errors.append({"code": "INVALID_TYPE", "message": "trigger must be a dict"})

    re_list = obj.get("required_evidence")
    if re_list is not None:
        if not isinstance(re_list, list) or len(re_list) < 1:
            errors.append({"code": "INVALID_VALUE", "message": "required_evidence must be a non-empty list"})

    return errors


def validate_constraint_evidence(evidence: Any) -> list[dict[str, str]]:
    """Validate a ConstraintEvidence dict against the authoritative schema.

    Returns list of error dicts. Empty list means valid.
    """
    errors: list[dict[str, str]] = []

    if not isinstance(evidence, dict):
        return [{"code": "INVALID_TYPE", "message": f"ConstraintEvidence must be dict, got {type(evidence).__name__}"}]

    for field_name in CONSTRAINT_EVIDENCE_REQUIRED_FIELDS:
        if field_name not in evidence:
            errors.append({"code": "MISSING_FIELD", "message": f"Missing required field: '{field_name}'"})

    eid = evidence.get("evidence_id")
    if eid is not None and (not isinstance(eid, str) or not _EVIDENCE_ID_PATTERN.match(eid)):
        errors.append({"code": "INVALID_FORMAT", "message": f"evidence_id '{eid}' must match '^EV-[A-Z0-9]+-[0-9]+$'"})

    rid = evidence.get("rule_id")
    if rid is not None and (not isinstance(rid, str) or not _RULE_ID_PATTERN.match(rid)):
        errors.append({"code": "INVALID_FORMAT", "message": f"rule_id '{rid}' must match '^CR-[A-Z0-9]+-[0-9]+$'"})

    comp = evidence.get("completeness")
    if comp is not None and comp not in EVIDENCE_COMPLETENESS_VALUES:
        errors.append({"code": "INVALID_ENUM", "message": f"completeness '{comp}' not in {sorted(EVIDENCE_COMPLETENESS_VALUES)}"})

    items = evidence.get("evidence_items")
    if items is not None:
        if not isinstance(items, list):
            errors.append({"code": "INVALID_TYPE", "message": "evidence_items must be a list"})
        else:
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    errors.append({"code": "INVALID_TYPE", "message": f"evidence_items[{i}] must be a dict"})
                else:
                    for req in ("key", "value", "source"):
                        if req not in item:
                            errors.append({"code": "MISSING_FIELD", "message": f"evidence_items[{i}].{req} is required"})

    return errors


def validate_constraint_decision(decision: Any) -> list[dict[str, str]]:
    """Validate a ConstraintDecision dict against the authoritative schema.

    Returns list of error dicts. Empty list means valid.
    """
    errors: list[dict[str, str]] = []

    if not isinstance(decision, dict):
        return [{"code": "INVALID_TYPE", "message": f"ConstraintDecision must be dict, got {type(decision).__name__}"}]

    for field_name in CONSTRAINT_DECISION_REQUIRED_FIELDS:
        if field_name not in decision:
            errors.append({"code": "MISSING_FIELD", "message": f"Missing required field: '{field_name}'"})

    did = decision.get("decision_id")
    if did is not None and (not isinstance(did, str) or not _DECISION_ID_PATTERN.match(did)):
        errors.append({"code": "INVALID_FORMAT", "message": f"decision_id '{did}' must match '^CD-[A-Z0-9]+-[0-9]+$'"})

    action = decision.get("action")
    if action is not None and action not in DECISION_ACTIONS:
        errors.append({"code": "INVALID_ENUM", "message": f"action '{action}' not in {sorted(DECISION_ACTIONS)}"})

    severity = decision.get("severity")
    if severity is not None and severity not in SEVERITIES:
        errors.append({"code": "INVALID_ENUM", "message": f"severity '{severity}' not in {sorted(SEVERITIES)}"})

    det = decision.get("deterministic")
    if det is not None and det is not True:
        errors.append({"code": "INVALID_VALUE", "message": "deterministic must be true"})

    return errors
