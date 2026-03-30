"""
Governed Contract Loader

Loads machine-readable contract artifacts from Construction_Kernel.
Validates contracts against kernel-owned schemas and enforces exact version match.
Fails closed if contracts are missing, malformed, incompatible, or version-mismatched.

Runtime consumes governed contracts. Runtime does not define them.
Runtime loads schemas from Construction_Kernel. Runtime does not define schemas.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


# Expected contract version — exact match required, no implicit compatibility.
EXPECTED_CONTRACT_VERSION = "1.0"

# Default path to Construction_Kernel contracts.
# Expects Construction_Kernel as a sibling directory to Construction_Runtime.
_DEFAULT_KERNEL_CONTRACTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "Construction_Kernel", "contracts"
)

# Environment variable override for governed contract path.
_ENV_CONTRACTS_PATH = "CONSTRUCTION_KERNEL_CONTRACTS_PATH"


class ContractLoadError(Exception):
    """Raised when a governed contract cannot be loaded. Fail-closed."""


class ContractVersionError(ContractLoadError):
    """Raised when a governed contract has an unexpected version. Fail-closed."""


class ContractSchemaError(ContractLoadError):
    """Raised when a governed contract fails schema validation. Fail-closed."""


def _resolve_contracts_path() -> Path:
    """Resolve the path to Construction_Kernel contracts directory."""
    env_path = os.environ.get(_ENV_CONTRACTS_PATH)
    if env_path:
        return Path(env_path)
    return Path(_DEFAULT_KERNEL_CONTRACTS_PATH).resolve()


def _load_json(filepath: Path) -> dict[str, Any]:
    """Load and parse a JSON contract file. Fail-closed on any error."""
    if not filepath.exists():
        raise ContractLoadError(
            f"Governed contract missing: {filepath}. "
            f"Runtime cannot operate without kernel contracts."
        )
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        raise ContractLoadError(
            f"Governed contract malformed: {filepath}. Error: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ContractLoadError(
            f"Governed contract invalid structure: {filepath}. Expected object."
        )
    return data


def _validate_version(data: dict[str, Any], filepath: Path) -> None:
    """
    Validate exact contract version match. Fail-closed on mismatch.

    No implicit compatibility. No version coercion. Unknown versions fail closed.
    """
    version = data.get("version")
    if version != EXPECTED_CONTRACT_VERSION:
        raise ContractVersionError(
            f"Governed contract version mismatch: {filepath}. "
            f"Expected '{EXPECTED_CONTRACT_VERSION}', got '{version}'. "
            f"No implicit compatibility — exact version match required."
        )


def _validate_authority(data: dict[str, Any], filepath: Path) -> None:
    """Validate that contract declares Construction_Kernel authority."""
    authority = data.get("authority")
    if authority != "Construction_Kernel":
        raise ContractSchemaError(
            f"Governed contract authority invalid: {filepath}. "
            f"Expected 'Construction_Kernel', got '{authority}'."
        )


def _load_schema(schema_name: str) -> dict[str, Any]:
    """
    Load a contract schema from Construction_Kernel schemas directory.

    Schemas are kernel-owned. Runtime loads them but does not define them.
    """
    contracts_path = _resolve_contracts_path()
    schema_path = contracts_path / "schemas" / schema_name
    if not schema_path.exists():
        raise ContractSchemaError(
            f"Governed contract schema missing: {schema_path}. "
            f"Runtime cannot validate contracts without kernel schemas."
        )
    return _load_json(schema_path)


def _validate_against_schema(data: dict[str, Any], schema: dict[str, Any], filepath: Path) -> None:
    """
    Validate a contract against its kernel-owned schema.

    Uses structural validation: checks required fields exist and have correct types.
    Runtime does not embed schema structures — it loads the schema from
    Construction_Kernel and validates against it.
    """
    required_fields = schema.get("required", [])
    properties = schema.get("properties", {})

    for field_name in required_fields:
        if field_name not in data:
            raise ContractSchemaError(
                f"Governed contract missing required field '{field_name}': {filepath}. "
                f"Schema: {schema.get('$id', 'unknown')}"
            )

    # Validate types for fields that have type constraints
    for field_name, field_schema in properties.items():
        if field_name not in data:
            continue
        value = data[field_name]
        expected_type = field_schema.get("type")
        if expected_type == "string" and not isinstance(value, str):
            raise ContractSchemaError(
                f"Governed contract field '{field_name}' expected string, got {type(value).__name__}: {filepath}."
            )
        elif expected_type == "array" and not isinstance(value, list):
            raise ContractSchemaError(
                f"Governed contract field '{field_name}' expected array, got {type(value).__name__}: {filepath}."
            )
        elif expected_type == "object" and not isinstance(value, dict):
            raise ContractSchemaError(
                f"Governed contract field '{field_name}' expected object, got {type(value).__name__}: {filepath}."
            )

        # Validate const constraints
        if "const" in field_schema and value != field_schema["const"]:
            raise ContractSchemaError(
                f"Governed contract field '{field_name}' expected '{field_schema['const']}', "
                f"got '{value}': {filepath}."
            )

        # Validate array minItems
        if expected_type == "array" and isinstance(value, list):
            min_items = field_schema.get("minItems", 0)
            if len(value) < min_items:
                raise ContractSchemaError(
                    f"Governed contract field '{field_name}' requires at least {min_items} items, "
                    f"got {len(value)}: {filepath}."
                )


def load_applicability_rules() -> list[dict[str, Any]]:
    """
    Load governed detail applicability rules from Construction_Kernel.

    Validates against kernel-owned schema and enforces exact version match.
    Returns the list of applicability rules defined by the kernel.
    Fails closed if the contract is missing, malformed, version-mismatched,
    or fails schema validation.
    """
    contracts_path = _resolve_contracts_path()
    filepath = contracts_path / "detail_applicability" / "applicability_rules.json"
    data = _load_json(filepath)

    # Validate version — exact match, no implicit compatibility
    _validate_version(data, filepath)

    # Validate authority
    _validate_authority(data, filepath)

    # Validate against kernel-owned schema
    schema = _load_schema("detail_applicability.schema.json")
    _validate_against_schema(data, schema, filepath)

    rules = data.get("rules")
    if not isinstance(rules, list) or len(rules) == 0:
        raise ContractLoadError(
            f"Governed contract has no rules: {filepath}. "
            f"Runtime requires at least one applicability rule."
        )

    # Validate each rule has required fields
    required_fields = {"rule_id", "condition_pattern", "applies_detail", "detail_family", "components", "relationships"}
    for rule in rules:
        missing = required_fields - set(rule.keys())
        if missing:
            raise ContractLoadError(
                f"Governed rule '{rule.get('rule_id', 'unknown')}' missing fields: {missing}. "
                f"Contract: {filepath}"
            )

    return rules


def load_ir_instruction_types() -> list[str]:
    """
    Load governed IR instruction types from Construction_Kernel.

    Validates against kernel-owned schema and enforces exact version match.
    Returns the list of valid IR instruction type strings.
    Fails closed if the contract is missing, malformed, or version-mismatched.
    """
    contracts_path = _resolve_contracts_path()
    filepath = contracts_path / "drawing_instruction_ir" / "ir_instruction_types.json"
    data = _load_json(filepath)

    # Validate version — exact match, no implicit compatibility
    _validate_version(data, filepath)

    # Validate authority
    _validate_authority(data, filepath)

    # Validate against kernel-owned schema
    schema = _load_schema("ir_instruction_types.schema.json")
    _validate_against_schema(data, schema, filepath)

    types = data.get("ir_instruction_types")
    if not isinstance(types, list) or len(types) == 0:
        raise ContractLoadError(
            f"Governed contract has no IR instruction types: {filepath}."
        )

    return types


def load_detail_schema() -> dict[str, Any]:
    """
    Load governed detail schema from Construction_Kernel.

    Validates against kernel-owned schema and enforces exact version match.
    Returns the schema contract defining valid roles, relationships, and parameters.
    Fails closed if the contract is missing, malformed, or version-mismatched.
    """
    contracts_path = _resolve_contracts_path()
    filepath = contracts_path / "detail_schema" / "detail_schema.json"
    data = _load_json(filepath)

    # Validate version — exact match, no implicit compatibility
    _validate_version(data, filepath)

    # Validate authority
    _validate_authority(data, filepath)

    # Validate against kernel-owned schema
    schema = _load_schema("detail_schema.schema.json")
    _validate_against_schema(data, schema, filepath)

    if "valid_component_roles" not in data:
        raise ContractLoadError(
            f"Governed detail schema missing valid_component_roles: {filepath}."
        )

    return data
