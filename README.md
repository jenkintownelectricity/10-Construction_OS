# Construction OS Registry

Canonical platform inventory for the Construction OS architecture.

This registry catalogs all repositories that are confirmed members of the Construction OS platform, their layer assignments, and their architectural roles.

## Platform Inventory

See `registry/platform_inventory.json` for the machine-readable canonical inventory.

## Scope

This registry covers only repositories that have been confirmed as part of the Construction OS platform through architectural audit. Systems classified as PRE-UTK or independent are explicitly excluded.

## Registry Rules

- Entries are documentation-only and do not affect runtime behavior
- All entries must be confirmed through architectural audit before inclusion
- PRE-UTK systems must NOT be listed in this registry
- Layer and primary_area fields must align with confirmed audit findings
