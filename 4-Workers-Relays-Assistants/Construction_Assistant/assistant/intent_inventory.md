# Intent Inventory

## Purpose

Defines the intent classes that the assistant recognizes and can process. Each intent class maps to a query routing path and an expected emission type.

## Intent Classes

### 1. Truth Lookup

- **Description:** Operator asks for a confirmed fact from the governed system.
- **Examples:** "What is the specified compressive strength for this mix?" / "What material is specified for this assembly?"
- **Routing:** To the domain kernel (Layer 5) that owns the fact.
- **Expected emission:** Truth emission (if available), uncertainty or insufficiency emission (if not).

### 2. Status Lookup

- **Description:** Operator asks for the current state of a pipeline stage, validation result, or workflow position.
- **Examples:** "Has this submittal been validated?" / "What stage is this spec in the pipeline?"
- **Routing:** To Construction_Runtime (Layer 6) or Construction_Application_OS (Layer 7).
- **Expected emission:** Truth emission with state data.

### 3. Lineage Lookup

- **Description:** Operator asks where a fact, rule, or decision originates.
- **Examples:** "Where does this requirement come from?" / "Which kernel governs this constraint?"
- **Routing:** To the governing kernel (Layer 5) or runtime (Layer 6) that owns the lineage.
- **Expected emission:** Truth emission with source reference.

### 4. Conflict Question

- **Description:** Operator asks whether two facts, requirements, or states are in conflict.
- **Examples:** "Does this spec conflict with the assembly definition?" / "Are these two requirements contradictory?"
- **Routing:** To the relevant kernels (Layer 5) and/or runtime validation surfaces (Layer 6).
- **Expected emission:** Truth emission if governed validation exists, uncertainty emission if no governed conflict check is available.

### 5. Completeness Question

- **Description:** Operator asks whether a required set of data, documents, or validations is complete.
- **Examples:** "Is this submittal package complete?" / "Are all required validations passing?"
- **Routing:** To Construction_Runtime (Layer 6) or Construction_Application_OS (Layer 7).
- **Expected emission:** Truth emission if completeness is governed, insufficiency emission if required data is missing.

### 6. Routing Question

- **Description:** Operator asks where to go or what system to use for a specific task.
- **Examples:** "Where do I submit this?" / "Which system handles spec validation?"
- **Routing:** Resolved by the assistant's routing model without upstream query.
- **Expected emission:** Next valid action emission.

### 7. Next-Step Question

- **Description:** Operator asks what they should do next in a workflow.
- **Examples:** "What is the next step after validation?" / "What do I need to do to resolve this failure?"
- **Routing:** To Construction_Application_OS (Layer 7) workflow state surfaces.
- **Expected emission:** Next valid action emission.
