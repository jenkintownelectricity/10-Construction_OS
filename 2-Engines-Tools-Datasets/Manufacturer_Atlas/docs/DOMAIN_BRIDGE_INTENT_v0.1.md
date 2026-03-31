# Domain Bridge Intent v0.1

**SYSTEM PLANE:** domain_plane
**ROLE:** consume_manufacturer_truth
**UPSTREAM AUTHORITY:** 10-building-envelope-manufacturer-os

---

## Intent

This bridge enables Construction_OS to consume manufacturer truth
for building envelope systems at runtime.

It supports:
- Loading manufacturer identity references
- Loading product definitions for assembly resolution
- Loading system/assembly definitions for constraint validation
- Loading installation and certification rules for fail-closed checks
- Loading compatibility matrices for product pairing validation

## What This Bridge Does NOT Do

- Does not produce canonical manufacturer truth
- Does not own governance authority
- Does not own UI rendering surfaces
- Does not own signal routing
- Does not extend or replace ValidKernel_Registry
- Does not create a sub-domain operating system

## Upstream Source

All manufacturer truth originates from `10-building-envelope-manufacturer-os`.
Records cached locally in `truth-cache/` are consumed references only.
Local copies carry no sovereignty. Upstream is authoritative.
