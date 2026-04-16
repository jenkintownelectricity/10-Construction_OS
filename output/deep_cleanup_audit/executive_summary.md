# Deep Cleanup Audit — Executive Summary

## What Is Real

**10-Construction_OS is the production system.** It has 39 Python tools, 11 workers, a parametric generator for 10 PMMA conditions, PDF and DXF export functions, Barrett source data, and a condition atlas with 120 canonical conditions. Everything that produces a printable detail packet today runs from this one repo.

**GPC_Shop_Drawings has the most mature CAD code.** Its `dxf_generator.py` (28.8KB) is the largest real DXF generation engine. It should be the canonical DXF production backend.

**WLV is a real workstation** with SVG/DXF/PDF export renderers in TypeScript. But it's interactive (Next.js app), not a batch generator.

**ALEXANDER is a real pattern engine** with 8 tested stages. But it's advisory — nothing currently consumes its output.

## What Is Duplicated

The ecosystem has built the same exporter **4 times**:
- 4 SVG exporters (Construction_OS, Runtime, WLV, ShopDrawing_Compiler)
- 4 DXF generators (GPC, Runtime, WLV, ShopDrawing_Compiler)  
- 3 PDF writers (Construction_OS, WLV, ShopDrawing_Compiler)

**None of them are wired to each other.** Each was built independently. The one that actually produces client-facing artifacts is the one in Construction_OS that was built during this emergency delivery.

## What Is Smoke

- 2 repos are empty READMEs (architect-reasoning, digital-twin)
- 4 kernel repos are JSON schemas with no executable code (Material, Chemistry, Scope, Spec)
- Sales Command Center is a scaffold with "generators declared but not implemented"
- The aspired end-to-end pipeline (ALEXANDER → Runtime → WLV → ShopDrawing_Compiler) has real code at each stage but the stages are NOT connected

## What the Cleaned Ecosystem Should Look Like

**Tier 1 — Production Core (2 repos)**
- 10-Construction_OS: truth, generators, export, output
- GPC_Shop_Drawings: production DXF engine

**Tier 2 — Supporting Systems (5 repos)**
- WLV: interactive workstation
- Construction_Runtime: svg/dxf writers (to be wired)
- ShopDrawing_Compiler: packet pipeline (to be wired)
- ALEXANDER: pattern advisory (to be wired)
- shop_drawings_ai: AI extraction

**Tier 3 — Governance + Infrastructure (7 repos)**
- validkernel-governance, registry, platform, control-plane, fabric, KG engine, domain-foundry

**Tier 4 — Reference / Archive (10 repos)**
- Assembly/Material/Chemistry/Scope/Spec Kernels, construction_dna, Construction_Kernel, Atlas, Building Envelope OS, manufacturer-mirror

**Tier 5 — Archive or Delete (5 repos)**
- architect-reasoning (empty), digital-twin (empty), VKBus (skeleton), Sales CC (scaffold), affiliate-domains (config)
