# Chemistry Kernel Non-Goals

## Explicit Non-Goals

This document records what the Construction Chemistry Kernel will never attempt to do. These boundaries are permanent and not subject to scope creep.

### 1. Product Recommendation
This kernel does not recommend specific products or manufacturers. It records chemical behavior of chemistry families and systems. Product selection is a downstream intelligence function.

### 2. Novel Reaction Prediction
This kernel records published, verified chemical behavior. It does not predict reactions that have not been documented through testing or research. Predictive chemistry is out of scope.

### 3. Specification Writing
This kernel does not generate specification language, product lists, or submittal requirements. That is the Specification Kernel's domain.

### 4. Installation Instruction
This kernel does not provide installation sequences, application methods, or workmanship criteria. Cure conditions are recorded as chemistry facts, not as installation instructions.

### 5. Cost Estimation
Chemical system cost data is not within scope. Cost is a project-level concern.

### 6. Field Diagnosis
This kernel does not diagnose field failures. It provides the chemistry truth that a diagnostic process might consume, but the diagnosis itself is an intelligence-layer function.

### 7. Regulatory Compliance Determination
This kernel records VOC content and hazard classifications from SDS data. It does not determine compliance with specific jurisdictional regulations. Compliance determination requires project-specific context.

### 8. Standards Text Reproduction
Referenced standards (ASTM, ISO, SCAQMD) are cited by identifier only. This kernel never reproduces standards text.

### 9. Material Physical Property Storage
Tensile strength, elongation, hardness, density, and other physical properties belong to the Material Kernel. This kernel stores only chemical behavior data.

### 10. Warranty Interpretation
Manufacturer warranty terms, conditions, and exclusions are contractual matters outside chemistry truth.

## Why Non-Goals Matter

Every non-goal protects the kernel from scope contamination. When a request falls into a non-goal category, the kernel must reject it cleanly and direct the caller to the appropriate system.
