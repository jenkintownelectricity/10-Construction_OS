# Intake & Review Application Surfaces — Wave 7

## Purpose

Define the application layer for project intake, evidence ingestion, assembly identity resolution, runtime triggering, and condition inspection.

---

## Position in Architecture

```
Construction_Kernel (canonical truth, governed contracts)
  → Construction_Runtime (deterministic pipeline)
    → apps/intake/ (intake & review surfaces)  ← this layer
```

The intake layer sits above the runtime pipeline. It consumes governed construction truth and invokes the deterministic pipeline. It does not modify kernel truth, governed contracts, or pipeline behavior.

---

## Boundary Rules

The intake layer must NOT:

- Redefine kernel truth
- Modify governed contracts
- Change runtime pipeline behavior
- Introduce navigation logic
- Introduce execution sequencing
- Create canonical truth
- Store or cache condition packets as truth

The intake layer may ONLY:

- Ingest project evidence
- Resolve assembly identity from evidence and kernel models
- Invoke the deterministic drawing runtime
- Display condition packets and inspection views

---

## Modules

| Module | Purpose |
|---|---|
| `project_intake.py` | Ingest project data: building systems, assemblies, materials, scope |
| `evidence_ingestion.py` | Accept evidence: drawings, specifications, photos, RFIs, submittals |
| `assembly_identity_resolver.py` | Map evidence to kernel assembly models, resolve interfaces |
| `runtime_trigger.py` | Invoke deterministic pipeline, collect condition packets |
| `condition_inspector.py` | Browse conditions, inspect parameters, show readiness and blockers |

---

## Output Classification

All intake outputs are:

- **Derived** — produced by transformation of governed inputs
- **Recomputable** — regenerable from the same inputs at any time
- **Non-canonical** — not sources of truth

No intake output may be fed back as input to the kernel or runtime pipeline.

---

## Fail-Closed Posture

- Missing project data fails closed
- Unknown evidence types fail closed
- Unresolvable assembly references are tracked as unresolved, not guessed
- Empty condition lists fail closed
- Runtime pipeline failures are surfaced, not suppressed
