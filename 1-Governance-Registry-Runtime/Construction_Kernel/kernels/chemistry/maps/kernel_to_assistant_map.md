# Kernel-to-Assistant Map

## Purpose

Documents the relationship between the Construction Chemistry Kernel and any AI assistant layer.

## Status

Reserved for future assistant integration. No assistant is implemented.

## Design Intent

- The chemistry kernel provides structured truth data that an AI assistant could reference.
- No assistant logic, prompts, or conversation flows exist in this kernel.
- Future assistants would query kernel records to answer chemistry questions.

## Placeholder Notes

- An assistant could look up adhesion rules for a given substrate-chemistry pairing.
- Incompatibility warnings could be surfaced during material selection conversations.
- Cure condition constraints could inform field installation guidance.
- No timeline is established for assistant integration.

## Constraints

- Kernel records must never contain assistant prompts or conversational logic.
- Assistants must treat kernel data as authoritative and not override it.
- Any future assistant must cite kernel record IDs when referencing chemistry facts.

## References

- See `kernel_map.md` for entity overview.
- See contracts for the validation rules governing each entity type.
