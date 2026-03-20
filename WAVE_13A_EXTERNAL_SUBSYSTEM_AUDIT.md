# WAVE 13A — EXTERNAL SUBSYSTEM BRANCH AUDIT REPORT

**Date**: 2026-03-20
**Authority**: Construction OS System Architect
**Mode**: Branch audit only — no merges performed
**Scope**: construction_dna, holograph_details, CADless_drawings

---

## 1 — construction_dna Branch Audit

### Repository Overview
- **Purpose**: 20-tier material DNA taxonomy system for construction materials
- **Tech Stack**: TypeScript monorepo (Turborepo) — `packages/kernel`, `packages/core`, `packages/web`, `packages/song-kernel`
- **Main Branch HEAD**: `e3b6adc` (2026-02-14)

**CRITICAL FINDING**: This repository contains TWO UNRELATED SYSTEMS:
1. **Construction Material Kernel** (`packages/kernel`) — material DNA taxonomy, compatibility engine, failure modes
2. **Song/Beat Kernel** (`packages/song-kernel`) — music production schemas (COMPLETELY IRRELEVANT to Construction OS)

Only `packages/kernel`, `packages/core`, and `packages/web` are relevant to Wave 13A.

### Branch Analysis

#### Branch: `origin/main`
- **Last Activity**: 2026-02-14
- **Classification**: PRODUCTION READY
- **Contains**:
  - `packages/kernel/src/types/material-dna.ts` — Full 20-tier MaterialDNA type system (346 lines)
  - `packages/kernel/src/data/compatibility.ts` — Material compatibility engine (371 lines)
  - `packages/kernel/src/data/failure-modes.ts` — Failure mode database
  - `packages/kernel/src/data/chemistries.ts` — Chemistry classification data
  - `packages/kernel/src/data/constants.ts` — Material constants
  - `packages/kernel/src/utils/validation.ts` — DNA validation utilities
  - `packages/core/src/index.ts` — Core functions: `createMaterialDNA()`, `validateMaterialDNA()`, `checkCompatibility()`, `getFailureModes()`, `searchMaterials()`, `classifyMaterial()`
  - `packages/web/` — Next.js dashboard for material browsing
- **Verdict**: **USE AS SOURCE**

#### Branch: `origin/claude/entity-extraction-scaffold-5vKZG`
- **Last Activity**: 2026-02-15
- **Ahead of main**: 1 commit | **Behind main**: 0
- **Changes**: +CLAUDE_LOG.md (61 lines), +README.md updates (39 lines)
- **Purpose**: Documentation — adds CLAUDE_LOG and updates README
- **Classification**: EXPERIMENTAL
- **Comparison**: Equal to main (docs-only delta)
- **Verdict**: **IGNORE** — documentation scaffolding only, no functional value for Wave 13A

#### Branch: `origin/claude/lightning-studio-music-kernel-MKeUe`
- **Last Activity**: 2026-02-14
- **Ahead of main**: 1 commit | **Behind main**: 0
- **Changes**: CHANGELOG.md (+29/-1), README.md (+9)
- **Purpose**: Documents song-kernel package
- **Classification**: OBSOLETE (for Construction OS purposes)
- **GOVERNANCE FLAG**: Song kernel is an unrelated music system sharing the repo. Not a Construction OS concern.
- **Verdict**: **IGNORE** — music production system, zero relevance

#### Branch: `origin/claude/setup-construction-dna-dashboard-RHzn8`
- **Last Activity**: 2026-02-12
- **Ahead of main**: 0 | **Behind main**: 3
- **Changes**: 5 files, 611 deletions (deletes song-kernel schemas/types)
- **Classification**: OBSOLETE / SUPERSEDED
- **Comparison**: Worse than main — behind by 3 commits, destructive changes
- **Verdict**: **IGNORE** — superseded by main, destructive deletions

### construction_dna Summary

| Branch | Classification | Verdict |
|--------|---------------|---------|
| main | PRODUCTION READY | **USE AS SOURCE** |
| entity-extraction-scaffold | EXPERIMENTAL | IGNORE |
| lightning-studio-music-kernel | OBSOLETE | IGNORE |
| setup-construction-dna-dashboard | SUPERSEDED | IGNORE |

**Best Branch for Wave 13A**: `main`

### Reusable APIs (from main)

```typescript
// packages/core/src/index.ts
function createMaterialDNA(input: Partial<MaterialDNA>): MaterialDNA
function validateMaterialDNA(dna: MaterialDNA): ValidationResult
function checkCompatibility(materialA: MaterialDNA, materialB: MaterialDNA): CompatibilityResult
function getFailureModes(dna: MaterialDNA): FailureMode[]
function searchMaterials(query: SearchQuery): MaterialDNA[]
function classifyMaterial(input: ClassificationInput): MaterialClassification
```

```typescript
// packages/kernel/src/types/material-dna.ts — Key Types
interface MaterialDNA {
  id: string
  name: string
  manufacturer: string
  division: string           // CSI division
  category: string
  chemistry: ChemistryProfile
  physical: PhysicalProperties
  performance: PerformanceMetrics
  engineering: EngineeringData
  classification: ClassificationData
  // ... 20 tiers total
}
```

### Risks
1. **Song kernel contamination**: Unrelated music system shares the monorepo — must ensure Construction OS adapter ONLY imports from `packages/kernel` and `packages/core`
2. **No published npm package**: Must be consumed as source or git dependency
3. **Web dashboard** (`packages/web`) should NOT be integrated — it's a standalone UI

---

## 2 — holograph_details Branch Audit

### Repository Overview
- **Purpose**: 3D BIM Detail Viewer — multi-tenant SaaS for holographic construction detail rendering
- **Tech Stack**: TypeScript — Express backend + React/Three.js frontend (polr-holographic-viewer)
- **Main Branch HEAD**: Most recent commit 2026-02-15

### Branch Analysis

#### Branch: `origin/main`
- **Last Activity**: 2026-02-15
- **Classification**: PRODUCTION READY
- **Contains**:
  - `polr-holographic-viewer/` — Complete Three.js-based 3D viewer with:
    - `materials/material-factory.ts` — Material factory (397 lines) with `MaterialFactory.create()`, `getPhysicalMaterial()`, `getHatchMaterial()`
    - `materials/base-materials.ts` — Base material definitions
    - `materials/texture-library.ts` — Texture management
    - `materials/manufacturers.ts` — Manufacturer-specific materials
    - `materials/ai-texture-generator.ts` — AI texture generation
    - `stores/dna-material-store.ts` — DNA material state management
    - `services/dna-import.ts` — DNA file import/export (305 lines)
    - `hooks/useDNACompatibility.ts` — Material compatibility React hook (218 lines)
    - `types/construction-dna.ts` — DNA type definitions (444 lines)
  - `backend/src/routes/details.ts` — REST API for details CRUD (234 lines)
  - `shared/types/` — Shared type definitions (detail.ts, layer.ts, tenant.ts, user.ts)
- **Verdict**: **USE AS SOURCE**

#### Branch: `origin/claude/entity-extraction-scaffold-5vKZG`
- **Last Activity**: 2026-02-15
- **Ahead of main**: 1 commit | **Behind main**: 0
- **Changes**: +CLAUDE_LOG.md (93 lines), +README.md updates (33 lines)
- **Purpose**: Documentation scaffolding
- **Classification**: EXPERIMENTAL
- **Comparison**: Equal to main (docs-only)
- **Verdict**: **IGNORE** — documentation only

#### Branch: `origin/claude/build-bim-viewer-saas-DA7q1`
- **Last Activity**: 2026-02-12
- **Ahead of main**: 1 commit | **Behind main**: 5
- **Changes**: Deletes L0-CMD-2026-0212-002-SAAS.md (284 deletions)
- **Purpose**: Removed SaaS planning document
- **Classification**: OBSOLETE
- **Comparison**: Worse than main — 5 commits behind, destructive
- **Verdict**: **IGNORE** — superseded by main

#### Branch: `origin/claude/fix-deploy-3d-viewer-BKlcJ`
- **Last Activity**: 2026-02-12
- **Ahead of main**: 0 | **Behind main**: 4
- **Changes**: 42 files changed, removes backend/frontend SaaS infrastructure (3,915 deletions), replaces with standalone HTML demo approach
- **Purpose**: Attempted to simplify deployment by removing SaaS multi-tenancy
- **Classification**: OBSOLETE / SUPERSEDED
- **Comparison**: Worse than main — removes critical backend infrastructure
- **GOVERNANCE FLAG**: This branch strips multi-tenant architecture. Main has the more complete system.
- **Verdict**: **IGNORE** — regressive, removes needed infrastructure

### holograph_details Summary

| Branch | Classification | Verdict |
|--------|---------------|---------|
| main | PRODUCTION READY | **USE AS SOURCE** |
| entity-extraction-scaffold | EXPERIMENTAL | IGNORE |
| build-bim-viewer-saas | OBSOLETE | IGNORE |
| fix-deploy-3d-viewer | SUPERSEDED | IGNORE |

**Best Branch for Wave 13A**: `main`

### Reusable APIs (from main)

```typescript
// polr-holographic-viewer/materials/material-factory.ts
class MaterialFactory {
  static create(type: string, options: MaterialOptions): THREE.Material
  static getPhysicalMaterial(config: PhysicalMaterialConfig): THREE.MeshPhysicalMaterial
  static getHatchMaterial(pattern: HatchPattern): THREE.Material
}

// polr-holographic-viewer/services/dna-import.ts
function importDNAFile(file: File): Promise<DNAMaterial[]>
function exportToDNA(materials: DNAMaterial[]): DNAExport
function downloadDNAExport(materials: DNAMaterial[]): void

// polr-holographic-viewer/hooks/useDNACompatibility.ts
function useDNACompatibility(details: SemanticDetail[]): DNAAnalysisResult
function checkMaterialCompatibility(layerA: Layer, layerB: Layer): CompatibilityWarning | null

// backend/src/routes/details.ts — REST API
GET    /api/details          // List details for tenant
GET    /api/details/:id      // Get detail with layers
POST   /api/details          // Create detail
PUT    /api/details/:id      // Update detail
DELETE /api/details/:id      // Delete detail
GET    /api/details/:id/layers   // Get layers
PUT    /api/details/:id/layers   // Update layers
```

### Risks
1. **AI texture generation** (`ai-texture-generator.ts`) — may introduce non-determinism; should be isolated behind adapter
2. **Multi-tenant SaaS architecture** — overly complex for adapter integration; only expose rendering functions
3. **Direct DNA type coupling** — `types/construction-dna.ts` (444 lines) duplicates types from construction_dna; adapter must normalize

---

## 3 — CADless_drawings Branch Audit

### Repository Overview
- **Purpose**: POLR (Parameterized On-demand Live Renderers) — deterministic 2D SVG construction detail generation
- **Tech Stack**: Pure JavaScript/Express.js — 45 detail renderers across 3 categories
- **Main Branch HEAD**: `0108f16` (2026-03-19)

### Branch Analysis

#### Branch: `origin/main`
- **Last Activity**: 2026-03-19
- **Classification**: PRODUCTION READY
- **Contains**:
  - `server.js` — Express API server with dynamic renderer loading
  - `renderers/index.js` — Renderer registry with auto-discovery
  - `renderers/utils.js` — Pure SVG utility functions (createSVG, drawRect, drawLine, drawPath, addText, addCallout, addDetailBubble, addDimension, addGradeLine, validateParams)
  - `renderers/materials.js` — Hardcoded material product catalogs
  - `renderers/generate-pdf.js` — PDF generation via Puppeteer (POC)
  - **45 Detail Renderers**: Air Barrier (AB-001–020), Waterproofing (WP-001–012), Roofing (RF-001–013)
  - `renderers/templates/detail_inventory.json` — Detail catalog schema
  - `renderers/templates/project_config.schema.json` — Project configuration (JSON Schema Draft 7)
- **Verdict**: **USE AS SOURCE**

#### Branch: `origin/claude/verify-main-branch-docs-WSnIq`
- **Last Activity**: 2026-03-19
- **Ahead of main**: 1 commit | **Behind main**: 0
- **Changes**: README.md (+12 lines) — adds ValidKernel Research Note / PRE-UTK classification
- **Purpose**: Documentation — adds ecosystem research note
- **Classification**: SALVAGEABLE
- **Comparison**: Equal to main (docs-only delta, minor value)
- **Verdict**: **HARVEST SELECTIVELY** — the PRE-UTK classification note may be worth preserving in registry

### Determinism Analysis

| Component | Deterministic? | Confidence |
|-----------|---------------|------------|
| SVG Renderers (all 45) | YES | **HIGH** |
| SVG Utilities (utils.js) | YES | HIGH |
| Material Data (materials.js) | YES (static) | HIGH |
| PDF Generation (generate-pdf.js) | NO — uses `Date.now()` | LOW |

**Evidence**: All 45 renderers are pure functions — accept params, return SVG strings. No `Math.random()`, no `Date.now()`, no mutable global state, no async I/O in render path. Same inputs always produce identical SVG output.

**PDF exception**: `generate-pdf.js` line 45 uses `new Date().toISOString()` in audit logs and relies on Puppeteer (headless Chrome) which may introduce rendering variance. This is a proof-of-concept, not production path.

### CADless_drawings Summary

| Branch | Classification | Determinism | Verdict |
|--------|---------------|-------------|---------|
| main | PRODUCTION READY | HIGH | **USE AS SOURCE** |
| verify-main-branch-docs | SALVAGEABLE | N/A (docs) | HARVEST SELECTIVELY |

**Best Branch for Wave 13A**: `main`

### Reusable APIs (from main)

```javascript
// renderers/index.js — Registry API
getRenderer(id)              // Retrieve renderer by ID
render(id, params)           // Execute render with parameters → SVG string
getCatalog()                 // Full detail catalog
getCatalogBySystem(type)     // Filter by AIR_BARRIER/WATERPROOFING/ROOFING
getDetailMeta(id)            // Metadata for specific detail
listDetailIds()              // All available detail IDs
getStats()                   // Category statistics

// renderers/utils.js — SVG Primitives
createSVG(options)           // Base SVG document builder
drawRect(x, y, w, h, opts)  // Rectangle element
drawLine(x1, y1, x2, y2, opts) // Line element
drawPath(d, opts)            // Path element
addText(x, y, text, opts)   // Text with multiline support
addCallout(fx, fy, tx, ty, text, opts) // Leader lines
addDetailBubble(x, y, num, ref, opts) // Detail reference circles
addDimension(x1, y1, x2, y2, text, opts) // Dimension lines
validateParams(params, schema)  // IV.02 FAIL-CLOSED validation

// server.js — REST API
GET  /api/catalog             // Full catalog
GET  /api/catalog/grouped     // Grouped by category
GET  /api/details/:id         // Detail metadata
GET  /api/render/:id          // SVG render (query params)
POST /api/render/:id          // SVG render (body params)
GET  /api/stats               // Statistics
GET  /api/errors              // Load error diagnostics

// Each renderer exports:
{ META: { id, name, category, description, variations, scale },
  PARAM_SCHEMA: { ... },
  render(params): string /* SVG */ }
```

---

## 4 — Cross-Subsystem Recommendation

### Best Branch Selection

| Repository | Best Branch | Reason |
|-----------|-------------|--------|
| **construction_dna** | `main` | Only production-ready branch; all others are docs-only or obsolete |
| **holograph_details** | `main` | Most complete; all other branches are behind or destructive |
| **CADless_drawings** | `main` | Only meaningful branch; one docs-only branch has marginal value |

### Strategy

**Merge Strategy**: NONE — Do not merge any external branches into Construction OS repos.

**Adapter Strategy**: All three subsystems accessed ONLY through runtime adapters in `Construction_Runtime`.

**Harvest Strategy**:
- **construction_dna/main** → Harvest `packages/kernel` and `packages/core` APIs for adapter contract definitions
- **holograph_details/main** → Harvest `MaterialFactory`, `dna-import`, `useDNACompatibility` interfaces for 3D rendering adapter
- **CADless_drawings/main** → Harvest `render(id, params)` and renderer registry for 2D rendering adapter
- **IGNORE** all `song-kernel` code — not construction-related

---

## 5 — Wave 13A Integration Plan

### 5.1 — Integration Points in Construction_Runtime

```
runtime/
  adapters/
    material_dna_adapter.ts      ← wraps construction_dna kernel API
    holograph_renderer_adapter.ts ← wraps holograph_details 3D rendering
    cadless_renderer_adapter.ts   ← wraps CADless_drawings 2D SVG rendering
```

### 5.2 — Contracts Required in Construction_Kernel

```typescript
// material_class_contract
interface MaterialClassContract {
  resolveMaterial(id: string): MaterialDNA
  checkCompatibility(a: MaterialDNA, b: MaterialDNA): CompatibilityResult
  getFailureModes(material: MaterialDNA): FailureMode[]
}

// compatibility_result_contract
interface CompatibilityResultContract {
  compatible: boolean
  confidence: number
  warnings: CompatibilityWarning[]
  failureModes: FailureMode[]
}

// detail_render_contract
interface DetailRenderContract {
  render3D(detailDNA: DetailDNA, materialClass: string, params: RenderParams): Scene3D
  render2D(detailDNA: DetailDNA, params: RenderParams): SVGString
  generateSheet(details: DetailDNA[], config: SheetConfig): SheetOutput
}
```

### 5.3 — Adapter Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Construction_Kernel                   │
│  (truth: contracts, material classes, detail specs)   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                Construction_Runtime                   │
│                                                       │
│  ┌─────────────────┐ ┌──────────────┐ ┌───────────┐ │
│  │material_dna_    │ │holograph_    │ │cadless_   │ │
│  │adapter          │ │renderer_     │ │renderer_  │ │
│  │                 │ │adapter       │ │adapter    │ │
│  └────────┬────────┘ └──────┬───────┘ └─────┬─────┘ │
└───────────┼─────────────────┼───────────────┼───────┘
            │                 │               │
   ┌────────▼────────┐ ┌─────▼──────┐ ┌──────▼──────┐
   │construction_dna │ │holograph_  │ │CADless_     │
   │(packages/kernel)│ │details     │ │drawings     │
   │                 │ │(viewer)    │ │(renderers)  │
   └─────────────────┘ └────────────┘ └─────────────┘
         EXTERNAL          EXTERNAL        EXTERNAL
```

### 5.4 — Subsystem Boundaries

| Subsystem | Role | Boundary Rule |
|-----------|------|---------------|
| construction_dna | Material intelligence | READ-ONLY via adapter. Cannot define construction truth. |
| holograph_details | 3D rendering | Rendering service only. Cannot define assembly logic. |
| CADless_drawings | 2D SVG rendering | Deterministic output only. Cannot define construction truth. |

### 5.5 — What Remains External
- Material taxonomy database (construction_dna)
- 3D renderer engines and Three.js pipeline (holograph_details)
- Material compatibility datasets (construction_dna)
- SVG renderer implementations (CADless_drawings)
- AI texture generation (holograph_details)

### 5.6 — What Must Never Be Imported Directly
- `packages/song-kernel/*` — music system, not construction
- `ai-texture-generator.ts` — non-deterministic, experimental
- `polr-holographic-viewer/stores/*` — React state management (UI logic)
- `generate-pdf.js` — Puppeteer POC with non-deterministic audit logs
- Any multi-tenant SaaS infrastructure (auth, tenants, middleware)

### 5.7 — Major Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Song kernel in construction_dna repo | MEDIUM | Adapter imports ONLY from `packages/kernel` and `packages/core` |
| DNA type duplication between repos | HIGH | Single source of truth in Construction_Kernel contracts; adapters translate |
| holograph_details multi-tenant complexity | MEDIUM | Adapter wraps only rendering functions, ignores SaaS infrastructure |
| PDF generation non-determinism | LOW | Use SVG renderers directly; PDF generation is separate concern |
| AI texture generation side effects | MEDIUM | Exclude from adapter; use only static material definitions |
| No published packages in any subsystem | MEDIUM | Git submodule or source-level integration via adapters |

### 5.8 — Execution Pipeline Support

The audit confirms all three subsystems can support the Wave 13A pipeline:

```
Condition Graph → Detail Family → Parameter Resolution
    → Material DNA Intelligence (construction_dna adapter)
    → Compatibility + Failure Checks (construction_dna adapter)
    → Manufacturer Selection (construction_dna adapter)
    → 3D Detail Rendering (holograph_details adapter)
    → 2D Detail Rendering (CADless_drawings adapter)
    → Sheet Generation (CADless_drawings adapter)
    → Package Output
```

---

## 6 — Final Verdict

### Audit Completeness
The subsystem audit is **COMPLETE**. All branches in all three repositories have been inspected, classified, and compared against their respective main branches.

### Source Branches for Wave 13A

| Repository | Source Branch | Method |
|-----------|-------------|--------|
| **construction_dna** | `main` | Adapter-based access to `packages/kernel` + `packages/core` |
| **holograph_details** | `main` | Adapter-based access to rendering functions |
| **CADless_drawings** | `main` | Adapter-based access to renderer registry + SVG renderers |

### Disposition Summary

| Action | Branches |
|--------|----------|
| **USE AS SOURCE** | construction_dna/main, holograph_details/main, CADless_drawings/main |
| **HARVEST SELECTIVELY** | CADless_drawings/verify-main-branch-docs (PRE-UTK note only) |
| **IGNORE** | construction_dna/entity-extraction-scaffold, construction_dna/lightning-studio-music-kernel, construction_dna/setup-construction-dna-dashboard, holograph_details/entity-extraction-scaffold, holograph_details/build-bim-viewer-saas, holograph_details/fix-deploy-3d-viewer |
| **DANGEROUS/DRIFTED** | None identified |

### Safest Execution Path
1. Define adapter contracts in `Construction_Kernel`
2. Implement three runtime adapters in `Construction_Runtime`
3. Consume `main` branches of all three external repos via adapter boundary
4. Never import external subsystem code directly into Construction OS modules
5. Maintain ValidKernel governance: Kernel owns truth, Runtime owns execution, external subsystems are adapters only

### Governance Violations Found
- **NONE** — No branch in any subsystem attempts to define construction truth. All three repos correctly operate as rendering/intelligence subsystems.

---

**Wave 13A subsystem branch audit complete. Construction OS baseline treated as fixed, external subsystem branches audited, recommended source branches identified, and adapter-based integration path defined under ValidKernel boundary discipline.**
