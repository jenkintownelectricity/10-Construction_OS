"""Contract validation utilities for Construction Runtime v0.2.

Validates pipeline stage outputs against JSON schema contracts.
"""

import json
import os
from typing import Any

_CONTRACTS_DIR = os.path.dirname(os.path.abspath(__file__))
_schema_cache: dict[str, dict] = {}


def _load_schema(contract_name: str) -> dict:
    """Load a contract schema by name."""
    if contract_name in _schema_cache:
        return _schema_cache[contract_name]
    path = os.path.join(_CONTRACTS_DIR, f"{contract_name}.schema.json")
    with open(path, "r") as f:
        schema = json.load(f)
    _schema_cache[contract_name] = schema
    return schema


def validate_contract(data: dict[str, Any], contract_name: str) -> dict[str, Any]:
    """Validate data against a named contract schema.

    Performs structural validation: required fields, types, enums.
    Does not require jsonschema library — uses lightweight built-in checks.

    Returns:
        {"is_valid": bool, "errors": list[dict], "contract_name": str, "schema_version": str}
    """
    try:
        schema = _load_schema(contract_name)
    except FileNotFoundError:
        return {
            "is_valid": False,
            "errors": [{"code": "CONTRACT_NOT_FOUND", "message": f"Contract '{contract_name}' not found.", "path": ""}],
            "contract_name": contract_name,
            "schema_version": "unknown",
        }

    errors: list[dict[str, str]] = []
    schema_version = schema.get("schema_version", "unknown")

    # Check required fields
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for field_name in required:
        if field_name not in data:
            errors.append({
                "code": "MISSING_REQUIRED_FIELD",
                "message": f"Missing required field: '{field_name}'",
                "path": field_name,
            })

    # Check types for present fields
    type_map = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "array": list, "object": dict}
    for field_name, field_schema in properties.items():
        if field_name not in data:
            continue
        expected_type = field_schema.get("type")
        if expected_type and expected_type in type_map:
            if not isinstance(data[field_name], type_map[expected_type]):
                errors.append({
                    "code": "INVALID_TYPE",
                    "message": f"Field '{field_name}' expected type '{expected_type}', got '{type(data[field_name]).__name__}'",
                    "path": field_name,
                })

        # Check enum values
        if "enum" in field_schema and data[field_name] not in field_schema["enum"]:
            errors.append({
                "code": "ENUM_VIOLATION",
                "message": f"Field '{field_name}' value '{data[field_name]}' not in {field_schema['enum']}",
                "path": field_name,
            })

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "contract_name": contract_name,
        "schema_version": schema_version,
    }
