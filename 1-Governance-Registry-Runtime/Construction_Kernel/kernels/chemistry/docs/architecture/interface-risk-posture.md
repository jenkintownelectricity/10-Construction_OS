# Chemistry Kernel Interface Risk Posture

## Purpose

Defines how the Chemistry Kernel manages risk at its interfaces with other kernels and downstream consumers.

## Interface Risk Categories

### 1. Chemistry-to-Material Kernel Interface
- **Risk:** Confusion between chemical behavior and physical properties
- **Mitigation:** Strict field-level separation. Chemistry records never contain tensile, elongation, hardness, or dimensional data. Cross-references use typed IDs only.
- **Failure mode:** A consumer treats a chemistry compatibility rule as a material specification
- **Posture:** Fail-closed. If a field does not belong to chemistry truth, the schema rejects it.

### 2. Chemistry-to-Assembly Kernel Interface
- **Risk:** Cure conditions interpreted as installation instructions
- **Mitigation:** Cure mechanism records state chemical requirements (temperature, humidity, time). They do not prescribe application method or sequencing.
- **Failure mode:** An assembler uses cure_time_hours as a workflow constraint without considering actual conditions
- **Posture:** Chemistry publishes facts. Assembly interprets for sequencing.

### 3. Chemistry-to-Specification Kernel Interface
- **Risk:** Chemistry compatibility data used as specification compliance evidence
- **Mitigation:** This kernel provides compatibility truth. Specification compliance requires additional context (approved products, submittals, project requirements).
- **Failure mode:** A specification reviewer assumes chemistry compatibility equals specification compliance

### 4. Chemistry-to-Reference Intelligence Interface
- **Risk:** Raw chemistry data consumed without interpretation guardrails
- **Mitigation:** All records include status, evidence_refs, and source hierarchy. Intelligence layer must respect status flags and confidence tiers.
- **Failure mode:** A draft or deprecated chemistry record is consumed as active truth

### 5. Chemistry-to-Runtime Interface
- **Risk:** Stale chemistry data used in real-time decisions
- **Mitigation:** All records carry revision lineage. Runtime consumers must validate against current active records.
- **Failure mode:** A cached incompatibility rule has been superseded but runtime still enforces it

## Default Posture

All interfaces default to **fail-closed**: if chemistry truth cannot be confirmed for a given combination, the interface reports "not verified" rather than "compatible."
