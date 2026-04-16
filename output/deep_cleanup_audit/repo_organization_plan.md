# Repo Organization Plan

## A. KEEP AS CORE (production-critical)

| Repo | Role | Action |
|------|------|--------|
| **10-Construction_OS** | Primary truth, generators, export tools, all output | Harden. This is the center. |
| **GPC_Shop_Drawings** | Production DXF generator, CAD engine | Maintain. Best CAD code in ecosystem. |

## B. KEEP AS SUPPORTING (real code, not yet wired)

| Repo | Role | Action |
|------|------|--------|
| **Construction_Runtime** | svg_writer.py + dxf_writer.py + geometry_engine | Wire to Construction_OS generator output |
| **10-White-Lightning_Vision_OS** | Interactive workstation, export renderers | Keep as standalone workstation. Do NOT embed into CAOS. |
| **ShopDrawing_Compiler** | Compiler pipeline, export engines | Wire intake to Construction_OS geometry output |
| **Construction_ALEXANDER_Engine** | 8-stage pattern advisory | Wire output to something that consumes proposals |
| **shop_drawings_ai** | AI assembly extraction | Keep for training and OCR pipeline |

## C. KEEP AS REFERENCE ONLY (read, don't build on)

| Repo | Role | Action |
|------|------|--------|
| **00-validkernel-governance** | Doctrine | Read-only reference |
| **00-validkernel-registry** | System topology | Read-only reference |
| **Construction_Assembly_Kernel** | Assembly schemas | Reference for schema validation |
| **Construction_Atlas** | Condition web UI (Vercel) | Demo/visualization only |
| **Construction_Kernel** | Master coordinator | Reference architecture |
| **construction_dna** | Audit trails | Historical reference |
| **70-manufacturer-mirror** | Barrett pilot demo | Mirror surface, not source |
| **10-building-envelope-manufacturer-os** | Envelope rules | Specialized reference |

## D. MERGE LATER (absorb useful parts into core)

| Repo | Merge Into | What to Keep |
|------|-----------|--------------|
| **Construction_Application_OS** | WLV or Construction_OS | Assembly parser app |
| **Construction_Runtime generator/** | Construction_OS generators/ | svg_writer.py, dxf_writer.py |

## E. ARCHIVE LATER (freeze, stop development)

| Repo | Reason |
|------|--------|
| **Construction_Material_Kernel** | Schema-only, no executable code |
| **Construction_Chemistry_Kernel** | Schema-only, no executable code |
| **Construction_Scope_Kernel** | Schema-only, no executable code |
| **Construction_Specification_Kernel** | Schema-only, no executable code |
| **00-validkernelos-vkbus** | Incomplete skeleton |
| **Construction_OS_Sales_Command_Center** | Scaffold only, no generators |

## F. DELETE LATER (empty or no real system)

| Repo | Reason |
|------|--------|
| **50-validkernel-architect-reasoning-workspace** | Empty README (550 bytes) |
| **60-validkernel-schematic-digital-twin** | Empty README (691 bytes) |

## G. KEEP AS INFRASTRUCTURE (not in detail path)

| Repo | Role |
|------|------|
| **30-validkernel-platform** | Platform runtime monorepo |
| **40-validkernel-control-plane** | Control dispatcher |
| **20-Governed-Multi-Domain-OS-Fabric** | UI adapter |
| **30-validkernel-knowledge-graph-engine** | Graph analysis |
| **10-domain-foundry-os** | Domain runtime |
| **20-VTI_TM** | Engineering core |
| **80-vk-owned-affiliate-domains** | Domain hosting config |
