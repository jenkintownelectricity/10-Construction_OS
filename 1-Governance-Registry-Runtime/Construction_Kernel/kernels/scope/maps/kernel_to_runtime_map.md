# Kernel-to-Runtime Map — Construction Scope Kernel

## Purpose

This map defines the integration boundary between the Construction Scope Kernel and any runtime environment.

## Current Status

Reserved for future runtime integration. No runtime is implemented.

## Design Intent

- The scope kernel provides truth records that a runtime may read.
- The runtime MUST treat scope records as read-only inputs.
- No scope record contains executable logic, event handlers, or state transitions.

## Future Integration Points

- Runtime systems may query scope records to determine active scope boundaries.
- Runtime systems may read trade_responsibility records to route coordination tasks.
- Runtime systems may read inspection_step records to enforce hold points.
- Runtime systems may read commissioning_step records to generate checklists.

## Constraints

- The kernel MUST NOT be modified to accommodate runtime requirements.
- Runtime behavior MUST NOT leak into schema definitions or contract rules.
- All runtime integration MUST occur through a defined adapter layer.

## Governance

- This map will be updated when a runtime integration is designed and approved.
- Any runtime adapter MUST comply with the kernel contracts.
- Runtime state is never persisted in kernel truth records.

## No-Execution Guarantee

- The scope kernel contains zero executable code.
- All records are declarative truth, not imperative instructions.
- This guarantee is foundational and MUST NOT be violated by any integration.
