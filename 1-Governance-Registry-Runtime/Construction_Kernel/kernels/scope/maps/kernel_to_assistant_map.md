# Kernel-to-Assistant Map — Construction Scope Kernel

## Purpose

This map defines the integration boundary between the Construction Scope Kernel and any AI assistant or conversational agent.

## Current Status

Reserved for future assistant integration. No assistant is implemented.

## Design Intent

- An assistant may read scope truth records to answer questions about scope boundaries.
- An assistant MUST NOT fabricate scope truth; it MUST cite kernel records.
- Scope records provide the ground truth that constrains assistant responses.

## Future Integration Points

- An assistant may query scope_of_work records to explain what is in or out of scope.
- An assistant may read trade_responsibility records to clarify trade coordination.
- An assistant may reference inspection_step records to describe hold point requirements.
- An assistant may cite warranty_handoff_record entries to explain warranty terms.

## Constraints

- Assistants MUST NOT modify kernel records.
- Assistants MUST NOT generate scope definitions that contradict kernel truth.
- Assistant responses about scope MUST be traceable to specific kernel records.

## Governance

- This map will be updated when an assistant integration is designed and approved.
- Assistant behavior contracts will be defined separately from kernel contracts.
- No assistant integration may introduce execution logic into the kernel.

## No-Execution Guarantee

- The scope kernel does not invoke, configure, or manage assistants.
- All assistant integration occurs outside the kernel boundary.
