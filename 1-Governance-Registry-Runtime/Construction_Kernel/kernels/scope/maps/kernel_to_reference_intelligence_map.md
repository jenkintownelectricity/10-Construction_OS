# Kernel-to-Reference Intelligence Map — Construction Scope Kernel

## Purpose

This map defines how the reference intelligence layer reads scope truth from the Construction Scope Kernel.

## Intelligence Layer Role

The reference intelligence layer provides contextual knowledge to assistants, workers, and runtime systems. It reads scope kernel records as authoritative inputs and uses them to:

- Resolve scope boundary questions against kernel truth.
- Identify coordination risks by reading trade_responsibility and interface_zone data.
- Surface inspection requirements by reading inspection_step hold points.
- Track closeout completeness by reading closeout_requirement records.

## Read Pattern

The intelligence layer operates in a **read-only** posture toward the scope kernel:

```
Reference Intelligence Layer
  └── reads ──► scope_of_work records
  └── reads ──► trade_responsibility records
  └── reads ──► inspection_step records
  └── reads ──► commissioning_step records
  └── reads ──► closeout_requirement records
  └── reads ──► warranty_handoff_record records
```

## Truth Authority

- The scope kernel is the single source of truth for scope boundaries.
- The intelligence layer MUST NOT fabricate, infer, or override scope truth.
- When scope truth is ambiguous, the intelligence layer MUST flag the gap rather than fill it.

## Cross-Kernel Intelligence

- The intelligence layer may combine scope truth with detail truth (from the Detail Kernel) and standards truth (from the Standards Kernel) to provide richer context.
- Cross-kernel synthesis MUST cite the source kernel for each fact.

## Constraints

- The intelligence layer MUST NOT write to the scope kernel.
- Intelligence outputs (summaries, recommendations, risk flags) are not kernel truth.
- Intelligence layer behavior is governed by its own contracts, not scope kernel contracts.

## Principles

- Scope truth flows outward from the kernel. Intelligence reads; it does not write.
- All intelligence outputs that reference scope MUST be traceable to specific kernel record IDs.
- No execution leakage occurs between the intelligence layer and the scope kernel.
