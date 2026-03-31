# Manufacturer Truth-Consumption Bridge

**SYSTEM PLANE:** domain_plane
**ROLE:** consume_manufacturer_truth
**LOCAL AUTHORITY:** inherited from Construction_OS execution scope only
**AUTHORITY SOURCE FOR MANUFACTURER TRUTH:** 10-building-envelope-manufacturer-os

---

## What This Is

This subtree is a manufacturer truth-consumption bridge inside Construction_OS.

It exists only to help Construction_OS consume upstream manufacturer truth
for building envelope systems.

## What This Is NOT

- It does not own governance.
- It does not own canonical manufacturer truth.
- It does not own UI authority.
- It does not own signal routing.
- It does not own registry authority.
- It does not create a sub-domain OS.

## Authority Model

```
10-building-envelope-manufacturer-os
(authority: produce_truth)
        \u2193 read-only / consumed / referenced
10-Construction_OS
(authority: canonical_owner_of_construction_domain_execution)
        \u2193
2-Engines-Tools-Datasets/Manufacturer_Atlas
(role: consume_manufacturer_truth)
```

Foundry governs. Domains execute. Registry records. Signals route.
Code colocation does not transfer authority.

---

## Structure

```
2-Engines-Tools-Datasets/Manufacturer_Atlas/
  docs/
    DOMAIN_BRIDGE_INTENT_v0.1.md
    DOMAIN_BRIDGE_BOUNDARY_v0.1.md
    PROJECTION_POSTURE_v0.1.md
    REPAIR_PHASE_LOG_v0.1.md
  schemas/
    manufacturer.schema.json
    product.schema.json
    system.schema.json
    installation_rule.schema.json
    certification_rule.schema.json
    compatibility_matrix.schema.json
  examples/
  projection/
    detail-resolution-paths.json
    lens-definitions.json
  truth-cache/
    manufacturers/
    products/
    systems/
    rules/installation/
    rules/certification/
    compatibility/
  README.md
```

---

## Current State

| Category | Cached Records | Grounded | Scaffold |
|----------|---------------|----------|----------|
| Manufacturers | 1 | 0 | 1 |
| Products | 5 | 0 | 5 |
| Systems/Assemblies | 8 | 0 | 8 |
| Installation Rules | 3 | 3 | 0 |
| Certification Rules | 1 | 1 | 0 |
| Compatibility | 8 | 5 | 3 |

All records are consumed upstream references, not locally owned truth.
