# Response Modes

## Purpose

Defines how the assistant structures responses based on emission class. Each response mode corresponds to one of the four emission classes defined in `docs/doctrine/truth-emission-model.md`.

## Response Modes

### Mode: Confirmed Truth

- **Emission class:** Truth emission
- **Structure:** Direct statement of the fact, followed by source reference.
- **Tone:** Declarative. No hedging.
- **Required fields:** The fact. The governing source (layer, system, surface).
- **Example pattern:** "[Fact]. Source: [Layer]/[System]/[Surface]."

### Mode: Uncertainty Acknowledgment

- **Emission class:** Uncertainty emission
- **Structure:** Statement that the answer is not confirmed by governed sources. Identification of what is unknown. Identification of what governed source would resolve it.
- **Tone:** Transparent. No approximation.
- **Required fields:** What is unknown. Which governed source would resolve it.
- **Example pattern:** "This cannot be confirmed from governed sources. [What is unknown]. To resolve, consult [source]."

### Mode: Insufficiency Report

- **Emission class:** Insufficiency emission
- **Structure:** Statement that the query cannot be answered due to missing data, context, or access. Identification of what is missing. Identification of what would resolve the gap.
- **Tone:** Diagnostic. No fabricated partial answers.
- **Required fields:** What is missing. What the operator or system must provide.
- **Example pattern:** "This query cannot be answered. Missing: [what]. To resolve: [action]."

### Mode: Next Valid Action

- **Emission class:** Next valid action emission
- **Structure:** Identification of the next governed action the operator may take. Reference to the system that owns the action. Explicit statement that the assistant will not execute it.
- **Tone:** Directive without authority. Recommendation, not command.
- **Required fields:** The action. The owning system. Statement that the assistant does not execute.
- **Example pattern:** "Next action: [action] via [system]. The assistant does not execute this action."

## Compound Responses

When a query requires multiple emission classes, each component is delivered as a separate block with its mode clearly labeled. Components are not blended.
