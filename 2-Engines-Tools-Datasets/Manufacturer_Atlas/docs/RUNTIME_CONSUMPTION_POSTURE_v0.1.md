# Runtime Consumption Posture v0.1

**SYSTEM PLANE:** domain_plane
**ROLE:** consume_manufacturer_truth (runtime execution)
**UPSTREAM AUTHORITY:** 10-building-envelope-manufacturer-os

---

## Purpose

The `runtime/` directory contains narrow, deterministic helpers that
enable Construction_OS to consume upstream manufacturer truth at execution time.

## Data Flow

```
10-building-envelope-manufacturer-os
  (canonical truth authority)
        |
        v
Manufacturer_Atlas/truth-cache/
  (consumed upstream reference, read-only)
        |
        v
Manufacturer_Atlas/runtime/
  (typed loaders + deterministic evaluator)
        |
        v
Construction_OS runtime consumers
        |
        v
ShopDrawing_Compiler (downstream, future)
```

## What Runtime Does

- Loads manufacturer records from truth-cache/manufacturers/
- Loads product records from truth-cache/products/
- Loads system/assembly records from truth-cache/systems/
- Loads installation rules from truth-cache/rules/installation/
- Loads certification rules from truth-cache/rules/certification/
- Loads compatibility matrix from truth-cache/compatibility/
- Evaluates narrow Barrett PMMA compatibility path

## What Runtime Does NOT Do

- Does not own truth
- Does not write to truth-cache
- Does not modify upstream records
- Does not serve APIs
- Does not render UI
- Does not emit signals
- Does not manage registry
- Does not perform probabilistic or AI-based reasoning

## Fail-Closed Behavior

Every loader and evaluator fails closed:

- Missing truth-cache directory -> HALT
- Missing required JSON files -> HALT
- Invalid record shape -> HALT
- Missing Barrett manufacturer identity -> HALT
- Missing PMMA product -> HALT
- Scaffold-only data where deterministic answer cannot be given -> HALT or WARN honestly
- No silent fallback, no best-effort hidden defaults

## Scope

This pass provides one narrow proving path only: Barrett PMMA compatibility.
Full manufacturer-consumption generalization is a future pass.
