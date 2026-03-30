# Drawing IR Consumption Note

## Purpose

Document how Construction_Runtime consumes Drawing Instruction IR rules defined by the Drawing Instruction IR specification.

---

## Consumption Rule

Runtime consumes IR instruction types from governed machine-readable contracts:
- `Construction_Kernel/contracts/drawing_instruction_ir/ir_instruction_types.json`

Human-readable doctrine source:
- `Construction_Kernel/docs/system/DRAWING_INSTRUCTION_IR.md`

Governed by:
- `Construction_Kernel/docs/governance/construction-detail-doctrine.md`

---

## Contract Loading

Runtime loads governed IR instruction types via `contract_loader.py`. Tests validate that all emitted IR instruction types exist in the governed contract. The IR contract defines the complete set of valid construction-semantic instruction types.

---

## Runtime Constraints

- Runtime consumes IR instruction types. Runtime does not define IR instruction types.
- Runtime tests must validate emitted types against the governed IR contract, not self-authored allowlists.
- Runtime must not invent IR instructions beyond governed translation of resolved detail logic.
- Runtime must not embed vendor-specific CAD commands in IR output.
- Runtime must not emit renderer-specific instructions at the IR layer.
- Runtime must maintain the separation between IR (what to draw) and renderer (how to emit).
- Runtime must fail closed when required IR inputs (component references, relationships, output intent) are incomplete.
- Runtime must fail closed when the governed IR contract is missing or malformed.

---

## Wave 6.5 Update

Tests updated in Wave 6.5 to validate IR instruction types against the governed kernel contract at `Construction_Kernel/contracts/drawing_instruction_ir/ir_instruction_types.json` rather than a self-authored allowlist.

---

## Safety Note

- This document defines architecture documentation only
- Test behavior was updated in Wave 6.5 to consume governed contracts
