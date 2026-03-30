# Operator Model

## Definition

An operator is any human or system that queries Construction_Assistant for information derived from the governed construction stack.

## Interaction Pattern

1. **Operator submits a query.** The query is a natural-language or structured question about construction domain state, governance, workflow, validation, or next actions.
2. **Assistant classifies the query.** The query is mapped to an intent class and routed to the appropriate stack surface.
3. **Assistant retrieves from governed source.** The assistant reads the relevant truth surface from Layer 5, 6, or 7.
4. **Assistant classifies the response.** The response is classified as truth, uncertainty, insufficiency, or next valid action.
5. **Assistant emits bounded response.** The response is delivered to the operator with its emission class clearly indicated.

## Operator Expectations

- The operator receives classified responses. Every response states whether it is confirmed truth, uncertain, insufficient, or a next-action recommendation.
- The operator can distinguish between what the system knows, what it does not know, and what is missing.
- The operator is never given fabricated certainty.
- The operator is never given output that implies the assistant has executed, approved, or written anything.

## Operator Responsibilities

- The operator is responsible for acting on next valid action emissions through the appropriate governed system interface.
- The operator is responsible for providing missing context when an insufficiency emission identifies a gap.
- The operator must not treat assistant output as approval, certification, or canonical record.

## Trust Model

The operator trusts the assistant to accurately relay governed truth. The operator does not trust the assistant to originate truth, execute actions, or mutate state. This trust boundary is enforced by the assistant's architecture, not by operator discipline alone.
