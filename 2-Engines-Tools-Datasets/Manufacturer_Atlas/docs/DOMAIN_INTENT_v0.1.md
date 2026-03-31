# Domain Intent v0.1

**SYSTEM PLANE:** domain_plane
**AUTHORITY:** produce_truth
**Domain:** Building Envelope Manufacturer Systems

---

## Intent

This repository is the canonical source of manufacturer truth for building envelope systems.

It produces and maintains:
- Manufacturer identity records
- Product definitions and specifications
- System assembly definitions
- Installation rules
- Certification rules
- Compatibility matrices

## What This Domain Produces

Truth records that downstream systems consume for:
- Detail resolution
- Assembly constraint validation
- Fail-closed bidding
- Governed installation verification
- Compatibility checking

## What This Domain Does NOT Own

- Runtime execution
- UI/frontend surfaces
- API servers
- Execution engines
- Signal routing
- Governance authority
- CAD/BIM rendering

## Authority Chain

```
Universal_Truth_Kernel
  ↓
ValidKernel-Governance
  ↓
Construction_OS (Domain d1)
  ↓
Manufacturer Systems Domain (this repo) — produce_truth
```

Code colocation does not transfer authority.
Foundry governs. Domains execute. Registry records. Signals route.
