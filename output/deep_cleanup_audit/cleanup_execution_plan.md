# Cleanup Execution Plan

## PHASE 1 — Stop Duplication (Week 1)
**Goal:** Freeze canonical owners so nobody builds another SVG exporter.

- Declare 10-Construction_OS as canonical batch SVG/PDF/DXF producer
- Declare GPC_Shop_Drawings as canonical production DXF generator
- Declare WLV as canonical interactive workstation (standalone)
- Document in validkernel-governance that no new exporter repos are created

**Repos affected:** All. **Risk:** Low (documentation only). **Gain:** Stops the cycle of rebuilding exporters.

## PHASE 2 — Freeze Canonical Owners (Week 1-2)
**Goal:** Every function has exactly one owner.

| Function | Owner |
|----------|-------|
| Condition atlas | 10-Construction_OS |
| Assembly truth | 10-Construction_OS |
| Parametric generation | 10-Construction_OS |
| Batch SVG export | 10-Construction_OS |
| Batch PDF export | 10-Construction_OS |
| Batch DXF export | 10-Construction_OS + GPC_Shop_Drawings |
| Interactive workstation | WLV |
| Pattern advisory | ALEXANDER |
| Governance doctrine | validkernel-governance |

**Risk:** Medium (requires agreement). **Gain:** Ends confusion about where things live.

## PHASE 3 — Archive Stale Systems (Week 2-3)
**Goal:** Reduce noise.

- Archive Material/Chemistry/Scope/Spec Kernels (mark as archived in README)
- Archive Sales Command Center (not yet implemented)
- Archive VKBus (incomplete skeleton)
- Delete or archive architect-reasoning-workspace and schematic-digital-twin

**Risk:** Low (nothing depends on these). **Gain:** 6-8 fewer repos to scan.

## PHASE 4 — Merge Surviving Logic (Week 3-4)
**Goal:** Consolidate useful code.

- Copy Construction_Runtime svg_writer.py + dxf_writer.py into Construction_OS generators/
- Build DrawingInstructionSet adapter for the parametric generator output
- Wire GPC dxf_generator.py as an optional DXF backend

**Risk:** Medium (code integration). **Prerequisite:** Phase 2 frozen. **Gain:** Unified generator stack.

## PHASE 5 — Unify Artifact Pipeline (Week 4-5)
**Goal:** One path from condition to client packet.

- Build geometry JSON → SVG renderer adapter
- Wire: generator → geometry JSON → SVG renderer → PDF compiler → DXF exporter
- Test with all 10 Barrett PMMA conditions
- Test with 10 fireproofing conditions

**Risk:** Medium. **Prerequisite:** Phase 4 complete. **Gain:** Fully automated detail generation.

## PHASE 6 — Harden Production Path (Week 5-6)
**Goal:** Make it reliable.

- Add validation at each pipeline stage
- Add receipt generation at each stage
- Add packet completeness validator
- Add white-background verification
- Add titleblock presence check

**Risk:** Low. **Gain:** No more silent failures.

## PHASE 7 — Wire Manufacturer Mirror + Renderer Adapters (Week 6-8)
**Goal:** Multi-manufacturer support.

- Wire manufacturer-mirror to consume from Construction_OS
- Add manufacturer-specific calibration specimens (Barrett, GAF, Siplast, etc.)
- Wire ALEXANDER pattern resolution to provide condition suggestions
- Wire WLV as interactive editor consuming parametric geometry

**Risk:** High (multi-system integration). **Prerequisite:** Phases 1-6 complete. **Gain:** Multi-manufacturer production stack.
