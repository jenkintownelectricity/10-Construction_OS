# Frozen Seam Manifest

## What Are Seams?

A seam is a governed contract boundary between two repositories. It declares which artifacts in the authority repository are consumed by which modules in the consumer repository, along with the version policy, failure mode, and lifecycle status.

Seams are the machine-readable declaration of architectural contract relationships. They do not define construction truth or runtime behavior — they declare where governed contracts cross repository boundaries.

## Seam Authority Model

- **Construction_Kernel owns all seams.** The seam manifest lives in `Construction_Kernel/contracts/seams/seam_manifest.json`.
- **Authority artifacts** are the governed contract files and schemas that define what the consumer must obey.
- **Consumer modules** are the runtime files that load and validate governed contracts.
- **Consumers do not define seams.** If a consumer needs a new seam, it must be added to the kernel manifest first.

## Canonical Truth vs Governed Contracts

These terms are distinct and must not be confused:

| Term | Definition | Owned By |
|---|---|---|
| **Canonical truth** | Domain facts defined by Construction_Kernel doctrine and markdown models. The ultimate source of construction meaning. | Construction_Kernel `docs/` |
| **Governed contract** | A machine-readable formalization of canonical truth. JSON artifacts that runtime loads programmatically. | Construction_Kernel `contracts/` |
| **Seam** | A declared boundary between authority artifacts and consumer modules. Metadata about the contract relationship itself. | Construction_Kernel `contracts/seams/` |
| **Normalized runtime output** | Runtime-internal representations produced by deterministic transformation. Not canonical truth. | Construction_Runtime |
| **Derived output** | Non-canonical, recomputable convenience outputs. Never fed back as inputs. | Construction_Runtime |

## Seam Lifecycle States

| State | Meaning |
|---|---|
| `draft` | Seam is proposed but not yet enforced. Consumer may not yet exist. |
| `active` | Seam is live. Consumer loads and validates against authority artifacts. |
| `frozen` | Seam is locked. Authority artifacts and consumer modules are stable. Changes require explicit governance review. |
| `deprecated` | Seam is scheduled for removal. Consumer should migrate away. |

## Current Seams

| Seam ID | Authority | Consumer | Status |
|---|---|---|---|
| `detail_applicability` | `applicability_rules.json` + schema | `contract_loader.py`, `detail_resolver.py` | frozen |
| `detail_schema` | `detail_schema.json` + schema | `contract_loader.py` | frozen |
| `drawing_instruction_ir` | `ir_instruction_types.json` + schema | `contract_loader.py`, `ir_emitter.py` | frozen |

## Fail-Closed Rule

Every seam declares `"fail_mode": "fail_closed"`. If authority artifacts are missing, malformed, version-mismatched, or schema-invalid, the consumer must halt — not fall back, infer, or silently degrade.
