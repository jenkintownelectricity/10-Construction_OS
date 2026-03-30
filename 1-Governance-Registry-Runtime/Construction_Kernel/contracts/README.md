# Construction Kernel — Governed Machine-Readable Contracts

## Purpose

This directory contains machine-readable contract artifacts that formalize the construction domain models defined in `docs/system/` and governed by `docs/governance/`.

Markdown documentation remains the human-readable doctrine layer. These JSON contracts are governed companion artifacts that allow downstream consumers (primarily Construction_Runtime) to programmatically load and validate against kernel-defined truth.

## Authority

- **Construction_Kernel owns these contracts.** They are governed artifacts, not runtime configuration.
- **Runtime consumes them and does not define them.** If runtime needs a rule, component role, relationship type, or IR instruction type that does not exist here, it must be added to the kernel contract first.
- **Contracts must stay synchronized with their markdown counterparts.** The markdown is the authoritative human-readable specification; the JSON is the authoritative machine-readable specification. Neither may contradict the other.

## Contract Artifacts

| Contract | File | Governed By | Schema |
|---|---|---|---|
| Detail Applicability Rules | `detail_applicability/applicability_rules.json` | `CONSTRUCTION_DETAIL_APPLICABILITY_MODEL.md` | `schemas/detail_applicability.schema.json` |
| Detail Schema | `detail_schema/detail_schema.json` | `CONSTRUCTION_DETAIL_SCHEMA.md` | `schemas/detail_schema.schema.json` |
| Drawing Instruction IR | `drawing_instruction_ir/ir_instruction_types.json` | `DRAWING_INSTRUCTION_IR.md` | `schemas/ir_instruction_types.schema.json` |

## Contract Schemas

Schema definitions live in `schemas/` and are owned by Construction_Kernel. Runtime loads and validates contracts against these schemas. Runtime must not define, embed, or override schema structures. Minimal structural checks in the runtime loader are permitted strictly for runtime safety (e.g., confirming a loaded object is a dict before schema validation runs).

## Terminology

These contracts use the following terms precisely:

- **Canonical truth**: Domain facts defined by Construction_Kernel doctrine and models. Only the kernel may originate canonical truth.
- **Governed contract**: A machine-readable formalization of canonical truth. Owned by Construction_Kernel. Consumed by runtime.
- **Normalized runtime output**: Runtime-internal representations produced by deterministic transformation of governed inputs. Not canonical truth.
- **Derived output**: Non-canonical, recomputable convenience outputs (condition packets, issue lists, route suggestions). Never fed back as inputs.

## Fail-Closed Rule

If a governed contract artifact is missing, malformed, or contains unrecognized fields, the consuming system must fail closed. It must not fall back to hardcoded defaults, infer missing rules, or silently degrade.

## Versioning

Each contract carries an explicit `"version"` field (e.g., `"1.0"`). Version policy:

- **Runtime requires exact version match.** The runtime contract loader declares the expected version and rejects contracts with any other version.
- **No implicit compatibility.** There is no "compatible range" or coercion logic.
- **Unknown versions fail closed.** If the contract version does not match exactly, the runtime raises `ContractVersionError` and halts.
- **Version changes require coordinated update** between kernel contracts and runtime contract loaders.
