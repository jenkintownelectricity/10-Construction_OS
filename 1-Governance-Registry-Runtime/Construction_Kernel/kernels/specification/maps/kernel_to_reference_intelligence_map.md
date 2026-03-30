# Kernel-to-Reference Intelligence Map — Construction Specification Kernel

## Relationship

Construction_Reference_Intelligence reads specification truth from this kernel. The relationship is unidirectional: intelligence layer reads, kernel does not read from intelligence.

## What Intelligence Reads

### Specification Requirements
The intelligence layer reads all active requirement records to:
- Identify cross-project specification patterns
- Detect common gaps in specification coverage
- Correlate requirements with failure modes from the risk registry
- Assess specification completeness relative to control layer coverage

### Ambiguity Flags
The intelligence layer reads ambiguity-flagged records to:
- Surface specification gaps for human review
- Identify systemic ambiguity patterns across specification sections
- Recommend clarification strategies based on historical resolutions

### Interface Zone Coverage
The intelligence layer reads interface zone references on requirements to:
- Assess whether specifications adequately address all transitions
- Identify interface zones with no specification coverage
- Correlate interface gaps with historical failure data

### Standards References
The intelligence layer reads standards citations to:
- Verify that referenced standards are current
- Identify specification sections missing expected standards references
- Correlate standards requirements across multiple kernels

### Testing and Submittal Requirements
The intelligence layer reads testing and submittal records to:
- Evaluate specification quality (thoroughness of QA/QC requirements)
- Identify specifications lacking field testing requirements
- Assess submittal completeness

### Warranty Requirements
The intelligence layer reads warranty records to:
- Assess warranty coordination (do all systems have matching warranty durations?)
- Identify warranty gaps at interface zones
- Correlate warranty types with failure risk

### Revision Lineage
The intelligence layer reads revision records to:
- Track specification instability (frequent revisions may indicate design uncertainty)
- Identify patterns in addendum-driven changes
- Assess the impact of RFI-driven specification modifications

## Access Mechanism

The intelligence layer accesses kernel data through `kernel_refs` — structured pointers containing kernel repository name, schema type, record ID, and schema version.

## Boundary Enforcement

The intelligence layer never writes to this kernel. Intelligence outputs (risk scores, recommendations, pattern analyses) remain in the intelligence layer's own data structures.
