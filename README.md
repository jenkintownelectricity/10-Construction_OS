# Construction_Intelligence_Workers

Specialized worker fleet for construction intelligence signal extraction and proposal generation.

## Role

Construction_Intelligence_Workers sits beside the governed construction stack as a signal extraction layer. Workers process construction documents, drawings, specifications, and material references to produce structured proposals, observations, and signals.

## Core Constraints

1. **Workers extract and propose.** Every worker output is a proposal, observation, or signal. No worker output is canonical truth.
2. **Workers do not define truth.** Truth is defined upstream by governed kernel and runtime layers. Workers reference truth; they do not create it.
3. **Workers do not self-canonicalize.** No worker may promote its own output to canonical status. All outputs require external validation.
4. **Workers must hand off into governed validation surfaces.** Every worker output must be delivered to a governed validation surface before it may influence downstream decisions.

## Workers

| Worker | Purpose |
|---|---|
| `assembly_interpreter` | Interprets construction assembly documents, extracts structured assembly data |
| `spec_parser` | Parses specification documents, extracts requirements, constraints, material references |
| `detail_extractor` | Extracts detail information from construction drawings and documents |
| `material_intelligence` | Analyzes material references, identifies products, classifies by assembly fit |
| `compliance_signal` | Generates compliance signals by comparing extracted data against governed constraints |

## Bus Adapters (v0.1)

Worker bus adapters provide structured event emission to the Construction Cognitive Bus. Workers may emit **Observation** and **Proposal** events only. Workers must never emit `ExternallyValidatedEvent`.

### Adapter Modules

| Module | Purpose |
|---|---|
| `workers/config.py` | Worker identity constants, schema version, allowed event classes |
| `workers/schema_builder.py` | Builds valid event envelope dicts with all required fields |
| `workers/event_adapter.py` | Submits built envelopes to the Cognitive Bus admission gate |
| `workers/observation_emitter.py` | Convenience wrapper for Observation events |
| `workers/proposal_emitter.py` | Convenience wrapper for Proposal events |

### Usage

```python
from workers.observation_emitter import ObservationEmitter
from workers.proposal_emitter import ProposalEmitter

# Emit an observation
result = ObservationEmitter.emit("material.detected", {"material": "steel", "confidence": 0.95})

# Emit a proposal
result = ProposalEmitter.emit("assembly.suggestion", {"assembly_id": "A-001", "action": "review"})

# Check admission result
if result["admitted"]:
    print("Event admitted:", result["admission_path"])
else:
    print("Event rejected:", result["reason"])
```

## Stack Position

This repository operates beside the construction stack (Layers 0-7). It consumes governed definitions from upstream layers and delivers proposals into governed validation surfaces. It does not participate in truth definition or runtime governance.

## Read Order

See `docs/system/REPO_MANIFEST.md` for the canonical first-read order.
