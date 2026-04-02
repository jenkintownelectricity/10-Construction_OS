# Barrett Onboarding Flow v0.1

## Authority
10-Construction_OS (domain execution plane)

## Purpose
Document the shortest governed path to onboard Barrett's 4 system families. This flow applies to any manufacturer — Barrett is the reference implementation.

## Sub-10-Minute Onboarding Target

| Step | Time | Action | Output |
|------|------|--------|--------|
| 1 | 30s | Create manufacturer record | MFR-BARRETT-001 |
| 2 | 1m | Select golden DXF per family | 1 representative detail per family |
| 3 | 1m | Parse DXF to raw JSON | Raw JSON with entities, layers, coordinates |
| 4 | 3m | Map layers to ownership classes | SYSTEM_OWNED / CONTEXT_ONLY / ANNOTATION per layer |
| 5 | 2m | Create family definition pack | Family JSON with components, layers, conditions |
| 6 | 1m | Run readiness audit | READY / PARTIAL / BLOCKED per family |
| 7 | 30s | Generate receipt | Onboarding receipt with evidence |
| **Total** | **~9m** | | |

## Barrett Families

| Family | System | CSI | Status |
|--------|--------|-----|--------|
| Black Pearl | Cold-applied rubberized asphalt sheet | 07 11 13 | PARTIAL |
| PMMA | PMMA-based flashing/detail system | 07 62 00 | PARTIAL |
| RamProof GC | Single-component fluid-applied | 07 11 13 | PARTIAL |
| RamTough 250 | Hot fluid-applied rubberized asphalt | 07 11 13 | PARTIAL |

## Path to READY

### Black Pearl (closest to READY)
1. Parse local DXF JSON (already done — parse_status: success)
2. Confirm layer-to-ownership: RAM Black Pearl Sheet → SYSTEM_OWNED, Protection Course → SYSTEM_OWNED, Others → CONTEXT_ONLY, Text/Defpoints → ANNOTATION
3. Validate component list against actual parsed layers
4. Mark READY

### PMMA
1. Parse DXF JSON from PMMA family folder
2. Map layers (expected: PMMA, RamFlash, Fleece, Primer → SYSTEM_OWNED)
3. Validate component list
4. Mark READY

### RamProof GC
1. Parse DXF JSON from RamProof_GC folder
2. Map layers (expected: RamProof GC → SYSTEM_OWNED)
3. Simplest family — likely fewest layers
4. Mark READY

### RamTough 250
1. Parse DXF JSON from RT-250 folder
2. Map layers (expected: RamTough 250, Protection Course → SYSTEM_OWNED)
3. Note PMMA cross-family pairing
4. Mark READY

## Onboarding Other Manufacturers

This same flow applies to:
- **Carlisle** — same steps, different layer names and product families
- **GAF** — same steps
- **Siplast** — same steps
- **Tremco** — same steps

No platform rebuild required. Create:
1. Manufacturer record
2. Family definition(s)
3. Layer mappings
4. Readiness audit

The taxonomy, ownership classes, and readiness rules are manufacturer-agnostic.

## Current Blockers to READY

1. DXF source files are gitignored (local-only) — layer mapping cannot be validated from repo alone
2. Component lists are from product knowledge, not yet confirmed against parsed DXF layers
3. No automated layer-to-ownership mapping tool exists yet (manual operator step)

## Next Steps

1. Run golden DXF parse for each family against local source files
2. Confirm layer names match definition expectations
3. Update definitions with confirmed layers
4. Mark families READY where evidence supports it
5. Build automated layer classifier if manual mapping proves too slow
