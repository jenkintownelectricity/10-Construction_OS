# Detail Applicability Consumption Note

## Purpose

Document how Construction_Runtime consumes detail applicability and detail schema rules defined by the Construction Detail Applicability Model and Construction Detail Schema.

---

## Consumption Rule

Runtime consumes detail applicability rules from governed machine-readable contracts:
- `Construction_Kernel/contracts/detail_applicability/applicability_rules.json`
- `Construction_Kernel/contracts/detail_schema/detail_schema.json`

Human-readable doctrine sources:
- `Construction_Kernel/docs/system/CONSTRUCTION_DETAIL_APPLICABILITY_MODEL.md`
- `Construction_Kernel/docs/system/CONSTRUCTION_DETAIL_SCHEMA.md`

Governed by:
- `Construction_Kernel/docs/governance/construction-detail-doctrine.md`

---

## Contract Loading

Runtime loads governed applicability rules via `contract_loader.py`. The loader:
1. Resolves the path to Construction_Kernel contracts (sibling directory or `CONSTRUCTION_KERNEL_CONTRACTS_PATH` env var)
2. Parses the governed JSON contract
3. Validates required fields on every rule
4. Fails closed if the contract is missing, malformed, or empty

Runtime does not embed, cache, or override governed rules. Each pipeline invocation loads from the governed source.

---

## Runtime Constraints

- Runtime consumes detail applicability rules and detail schema. Runtime does not define them.
- Runtime must not embed applicability rules inline in Python code.
- Runtime must not define detail logic or create detail variants.
- Runtime must not infer construction logic where no applicability rule matches.
- Runtime must not invent applicability matches for unresolved conditions.
- Runtime must not fall back to generic or default details.
- Runtime must fail closed when no applicability rule matches or when detail logic is incomplete.
- Runtime must fail closed when governed contract artifacts are missing, malformed, or incompatible.

---

## Wave 6.5 Update

Runtime behavior was updated in Wave 6.5 to load applicability rules from governed kernel contracts instead of defining them inline. The `detail_resolver.py` module no longer contains `APPLICABILITY_RULES`. Rules are loaded from `Construction_Kernel/contracts/detail_applicability/applicability_rules.json` via `contract_loader.py`.

---

## Safety Note

- This document defines architecture documentation only
- Runtime code was modified in Wave 6.5 to consume governed contracts
