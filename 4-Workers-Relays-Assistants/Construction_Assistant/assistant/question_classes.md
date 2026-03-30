# Question Classes

## Purpose

Taxonomy of question types the assistant can handle. Each question class maps to one or more intent classes and determines routing and emission behavior.

## Taxonomy

### Factual Questions

- **Pattern:** "What is X?" / "What does the spec say about X?"
- **Intent class:** Truth lookup
- **Expected emission:** Truth or uncertainty
- **Routing:** Domain kernel (Layer 5)

### State Questions

- **Pattern:** "What is the status of X?" / "Has X been validated?"
- **Intent class:** Status lookup
- **Expected emission:** Truth or insufficiency
- **Routing:** Runtime (Layer 6) or Application OS (Layer 7)

### Origin Questions

- **Pattern:** "Where does X come from?" / "Who governs X?"
- **Intent class:** Lineage lookup
- **Expected emission:** Truth
- **Routing:** Governing kernel (Layer 5)

### Conflict Questions

- **Pattern:** "Does X conflict with Y?" / "Are X and Y compatible?"
- **Intent class:** Conflict question
- **Expected emission:** Truth or uncertainty
- **Routing:** Relevant kernels (Layer 5) and/or validation surfaces (Layer 6)

### Completeness Questions

- **Pattern:** "Is X complete?" / "What is missing from X?"
- **Intent class:** Completeness question
- **Expected emission:** Truth or insufficiency
- **Routing:** Runtime (Layer 6) or Application OS (Layer 7)

### Navigation Questions

- **Pattern:** "Where do I do X?" / "Which system handles X?"
- **Intent class:** Routing question
- **Expected emission:** Next valid action
- **Routing:** Resolved from assistant routing model

### Workflow Questions

- **Pattern:** "What do I do next?" / "What is the next step after X?"
- **Intent class:** Next-step question
- **Expected emission:** Next valid action
- **Routing:** Application OS (Layer 7)

### Out-of-Scope Questions

- **Pattern:** Any question that requires truth origination, state mutation, approval, or execution.
- **Intent class:** None (rejected)
- **Expected emission:** Insufficiency emission explaining why the question cannot be answered and what governed channel to use instead.
