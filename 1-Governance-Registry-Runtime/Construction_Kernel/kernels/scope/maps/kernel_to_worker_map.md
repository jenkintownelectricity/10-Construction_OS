# Kernel-to-Worker Map — Construction Scope Kernel

## Purpose

This map defines the integration boundary between the Construction Scope Kernel and any worker process or agent.

## Current Status

Reserved for future worker integration. No worker is implemented.

## Design Intent

- Workers may consume scope truth records to perform domain tasks.
- Workers MUST NOT modify kernel truth records directly.
- Workers operate downstream of the kernel, reading scope definitions as input.

## Future Integration Points

- A scope validation worker may read schemas and contracts to validate records.
- A coordination worker may read trade_responsibility records to identify interface gaps.
- An inspection worker may read inspection_step records to generate inspection checklists.
- A closeout worker may read closeout_requirement records to track deliverable completion.

## Constraints

- Workers MUST NOT embed scope logic; they MUST read it from kernel records.
- Worker state is never stored in the kernel.
- Workers MUST comply with all kernel contracts when interpreting scope records.

## Governance

- This map will be updated when a worker integration is designed and approved.
- Worker implementations MUST be documented with their own contracts.
- No worker may override scope truth or inject behavioral logic into the kernel.

## No-Execution Guarantee

- The scope kernel does not instantiate, schedule, or manage workers.
- All worker integration occurs outside the kernel boundary.
