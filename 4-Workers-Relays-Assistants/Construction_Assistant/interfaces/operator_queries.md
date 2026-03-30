# Operator Query Interface Contract

## Purpose

Defines the interface contract between operators and the assistant for query submission and response receipt.

## Query Input Contract

### Required Fields

- **query_text:** The operator's question in natural language or structured form.

### Optional Fields

- **context:** Additional context the operator provides (project, assembly, spec reference, etc.).
- **intent_hint:** Operator's indication of what type of answer they seek (factual, status, next step, etc.).

### Input Constraints

1. Queries must be answerable from governed truth surfaces or classifiable as out-of-scope.
2. Queries requesting mutation, approval, or execution are rejected with an insufficiency emission explaining the boundary.
3. Queries are not stored as canonical records. They are transient inputs.

## Response Output Contract

### Required Fields

- **emission_class:** One of: truth, uncertainty, insufficiency, next_valid_action.
- **content:** The response content appropriate to the emission class.
- **source_reference:** The governed source consulted (layer, system, surface). Required for truth emissions. Included where applicable for other classes.

### Optional Fields

- **resolution_path:** For uncertainty and insufficiency emissions, what would resolve the gap.
- **inference_basis:** For inferred responses (subclass of uncertainty), the governed data used and what would convert it to confirmed truth.

### Output Constraints

1. Every response includes an emission class. No unclassified responses.
2. Truth emissions must include source reference.
3. Uncertainty and insufficiency emissions must include resolution path.
4. Next valid action emissions must name the owning system and state that the assistant does not execute.
5. No response implies approval, execution, or canonical write.
