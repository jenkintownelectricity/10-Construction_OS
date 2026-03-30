# Construction OS v2 — Truth Model

## Authority

Armand Lefebvre, L0 — Lefebvre Design Solutions LLC

## Truth Hierarchy

```
Universal_Truth_Kernel
  │
  └── Construction_Kernel (domain root beneath UTK)
        │
        ├── Intent Truth Plane
        │     │
        │     └── Construction_Intent_Kernel
        │           ├── Specification Truth
        │           ├── Assembly Intent
        │           ├── Scope Responsibility
        │           └── Required Methods
        │
        └── Actual Truth Plane
              │
              └── Construction_Reality_Kernel
                    ├── Observed Conditions
                    ├── Installed Assemblies
                    ├── Field Modifications
                    └── Inspection Data
```

## Structural Rules

1. **Universal_Truth_Kernel sits above Construction_Kernel.**
   UTK is Layer 0. Construction_Kernel is the domain root beneath UTK.

2. **Construction_Kernel is the domain root beneath Universal_Truth_Kernel.**
   It inherits the 3-line truth axioms and applies them to the construction domain.

3. **Construction_Kernel splits into two truth planes:**
   - Intent Truth Plane
   - Actual Truth Plane

4. **Intent Truth Plane descends into Construction_Intent_Kernel.**
   Intent Truth captures what was planned, specified, and authorized.

5. **Actual Truth Plane descends into Construction_Reality_Kernel.**
   Actual Truth captures what was observed, installed, and verified in the field.

6. **Intent Truth examples:**
   - Specification Truth — what the documents say
   - Assembly Intent — how components are meant to be assembled
   - Scope Responsibility — who is responsible for what
   - Required Methods — how work must be performed

7. **Actual Truth examples:**
   - Observed Conditions — what exists on site
   - Installed Assemblies — what was actually built
   - Field Modifications — changes made during construction
   - Inspection Data — verified observations from inspections

8. **The comparison layer below both planes is the Cognitive Observation Layer.**
   The Cognitive Observation Layer compares Intent Truth against Actual Truth.

9. **The Cognitive Observation Layer is explicitly non-authoritative and Ring 2 in posture.**
   It observes and reports. It does not own truth. It does not create truth.
   It is a seam-gated sentinel observation layer.

10. **Deviation / Pattern Detection occurs below the Cognitive Observation Layer.**
    When Intent and Actual diverge, deviations are detected and patterns are identified.

11. **Construction_Runtime sits below Deviation / Pattern Detection.**
    Runtime executes deterministic operations based on governance-authorized commands.

12. **Artifacts sit below Construction_Runtime.**
    Artifacts are derived outputs — reports, views, exports, notifications.

13. **Artifacts are derived outputs, not truth owners.**
    An artifact may display truth but does not define it.

14. **Runtime is deterministic and may not invent truth.**
    Runtime executes what governance authorizes. It does not create new truth.

15. **Intent Truth and Actual Truth are compared, not collapsed.**
    The two truth planes exist independently. Their comparison produces
    observations, not a merged truth. Collapsing them would destroy the
    ability to detect deviations.

## Full Truth Flow

```
Universal_Truth_Kernel
  └── Construction_Kernel
        ├── Intent Truth Plane → Construction_Intent_Kernel
        └── Actual Truth Plane → Construction_Reality_Kernel
                    │
              Cognitive Observation Layer (non-authoritative, Ring 2)
                    │
              Deviation / Pattern Detection
                    │
              Construction_Runtime (deterministic, no truth invention)
                    │
              Artifacts (derived outputs, not truth owners)
```

## Prohibitions

- Runtime must not be placed above either truth plane
- Intelligence must not own truth
- Artifacts must not be treated as canonical truth
- Universal_Truth_Kernel must not be omitted from the lineage
- Intent Truth and Actual Truth must not be collapsed into one plane

## Doctrine Lock

Construction OS v2 Doctrine-Frozen Rollout
Integrity-Level Hierarchy
Seam-Gated Sentinel Observation
