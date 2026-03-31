# Capability Targets v0.1

**SYSTEM PLANE:** domain_plane
**AUTHORITY:** produce_truth

---

## Current Capabilities

| Capability | Status | Records |
|-----------|--------|----------|
| Manufacturer identity records | scaffold | 1 |
| Product definitions | scaffold | 5 |
| System/assembly definitions | scaffold | 8 |
| Installation rules | grounded | 3 |
| Certification rules | grounded | 1 |
| Compatibility constraints | scaffold | 3 constraint sets |
| Condition definitions | grounded | 5 |
| Detail references | scaffold | 4 |

## Target Capabilities (Next Phase)

| Capability | Blocker |
|-----------|----------|
| Ground manufacturer identity | Requires data agreement |
| Ground product specifications | Requires manufacturer TDS |
| Ground assembly layer sequences | Requires manufacturer system guides |
| Ground compatibility matrix | Requires manufacturer warranty matrix |
| Ground detail geometry | Requires manufacturer CAD source |

## Grounding Ratio

- Grounded records: 9 (conditions + rules)
- Scaffold records: 18 (manufacturers, products, systems, assemblies, details)
- Ratio: 33% grounded / 67% scaffold

All scaffold records carry explicit `scaffold_reason` or `status: scaffold`.
No fabricated manufacturer specifications.
