# ShopDrawing.AI — Cross-Repository System Report

**Generated**: 2026-03-20
**Scope**: Full audit of all three repositories in the ShopDrawing.AI / ValidKernel ecosystem
**Repositories**:
1. `jenkintownelectricity/GPC_Shop_Drawings` — Production SaaS application
2. `jenkintownelectricity/ValidKernelOS_VKBUS` — Governance bus specification
3. `jenkintownelectricity/Construction_OS_Registry` — Governance registry & CI tooling

---

## Executive Summary

ShopDrawing.AI is a **production-deployed SaaS platform** for automated shop drawing production targeting building envelope contractors (GCP/PERM-A-BARRIER products). The system is backed by a formal governance framework (ValidKernel) that tracks every command, enforces receipt validation, and gates runtime execution.

| Component | Stack | Status |
|-----------|-------|--------|
| Frontend | React 18 CDN, 29 JSON chunks, 457KB assembled HTML | **Live** — shopdrawings.ai |
| Backend | FastAPI, 8 routers, 41 endpoints, Python 3.11+ | **Live** — Railway |
| Database | PostgreSQL 16, 7 tables, Alembic migrations | **Live** — Railway |
| AI | Claude Vision + Groq Llama 4 Scout | **Integrated** |
| CAD | ezdxf pipeline (885 lines), VR-001–VR-010 validation | **Real** |
| Auth | Clerk JWT + JWKS | **Real** |
| Billing | Stripe (backend ready, frontend stub) | **Partial** |
| Governance | ValidKernel v0.2.0, 24 commands, CI enforcement | **Active** |

---

## 1. Repository: GPC_Shop_Drawings

### Purpose
The core application — a full-stack SaaS for converting architectural detail screenshots into validated, layered DXF shop drawings with GCP product mapping.

### Architecture

```
ui/                          → React 18 SPA (29 JSON chunks, no build step)
  chunks/00-28               → Shell, theme, auth, workflow, CAD editor
  assemble.py                → Merges chunks → shopdrawing.html (457KB)

server/                      → FastAPI backend
  app/main.py                → 8 routers, CORS, error handler
  app/models/                → 7 SQLAlchemy models (Tenant, User, Project, Detail, TokenUsage, ProductRule, OperatorSetting)
  app/routers/               → auth, projects, upload, analyze, generate, validate, billing, admin
  app/services/              → 10 services (claude, groq, dxf, lisp, stripe, email_parser, normalizer, audit, ai_gateway)
  app/middleware/             → Clerk JWT auth, tenant context

src/                         → Core generation engines
  dxf_generator.py           → 885 lines — ezdxf pipeline with 13 GCP layers
  validation_engine.py       → 295 lines — VR-001 through VR-010
  visual_parser.py           → 338 lines — Claude Vision integration
  cad_instructions.py        → 311 lines — CAD instruction generator
  material_schedule.py       → 148 lines — BOM generator

data/                        → Static data
  product_rules.json         → 7 GCP products, keynote mapping, substrate rules
  detail_analysis_schema.json → JSON Schema v7 for detail analysis
  detail_matrix.json         → 49 details sheet assignment

details/                     → 13/49 analyzed detail JSONs
```

### Frontend: 8-Step Workflow

| Step | Chunk | Function |
|------|-------|----------|
| 1. Email/Scope Intake | 06 | Paste email, extract products/sheets/specs (editable) |
| 2. Spec Selection | 07 | CSI grid, keyword suggestions |
| 3. Document Upload | 08 | Drag-drop PDF/DWG |
| 4. PDF Review | 09 | PDF.js canvas with pan/zoom/region capture |
| 5. AI Analysis | 11 | Claude Vision screenshot analysis (editable) |
| 6. Line Style | 13 | 27 ACI colors, 6 linetypes, GCP/Carlisle presets |
| 7. DXF Generation | 17 | ezdxf pipeline, individual + batch ZIP |
| 8. Validation & Delivery | 19-20 | VR-001–VR-010 checks, delivery ZIP/PDF/email |

Additional views: Dashboard (05), Settings (27, 7 tabs), CAD Editor (28, 11 tools + snap engine), DXF Viewer (25), Billing (23).

### Backend: 41 API Endpoints

| Router | Path | Key Endpoints |
|--------|------|---------------|
| auth | `/api/auth` | GET /me, POST /webhook (Clerk) |
| projects | `/api/projects` | CRUD projects + details |
| upload | `/api/upload` | File upload, list, download |
| analyze | `/api/analyze` | Email parse, screenshot analysis, submittal scan |
| generate | `/api/generate` | DXF single/batch, LISP, delivery package |
| validate | `/api/validate` | Rules list, detail/batch validation, local validate |
| billing | `/api/billing` | Plans, checkout, portal, usage, webhook |
| admin | `/api/admin` | Settings CRUD, products CRUD, tenants |

### AI Integration

**Claude Vision** (`claude_service.py`, 249 lines):
- Screenshot analysis → keynotes, GCP products, substrates, continuity, transitions
- Validation prompt → VR-001–VR-010 check against completed drawing
- Token metering + quota enforcement via `ai_gateway.py`

**Groq Llama 4 Scout** (`groq_service.py`, 267 lines):
- Submittal page scanning (markup/stamp detection)
- Line classification (KEEP/DELETE/MODIFY/BY_OTHERS)
- 5 parallel workers for batch processing

**Data Normalization** (`normalizer.py`, 327 lines):
- Validates AI output against canonical schema
- Maps to product/substrate enums
- Gates: `validate_for_generation()` and `validate_for_delivery()`

### DXF Generation Pipeline

The `dxf_generator.py` (885 lines) produces layered DXF files with:
- 13 deterministic GCP layers (VPS30→ACI 30, NPL10→ACI 94, NPS-Detail→ACI 140, etc.)
- Product callout MTEXT blocks
- Dimension annotations (feet-inches format)
- Numbered general notes
- Title block data
- Drafting guide hints (frozen layer)

### Validation Engine (VR-001 through VR-010)

| Rule | Check | Severity |
|------|-------|----------|
| VR-001 | All 07XXXX keynotes mapped to GCP product | FAIL |
| VR-002 | Substrate/product compatibility | FAIL |
| VR-003 | Non-GCP products have warranty boundary | FAIL |
| VR-004 | Lap minimums met (4" GCP requirement) | WARN |
| VR-005 | Air barrier continuity maintained | FAIL |
| VR-006 | Primer requirements specified | CHECK |
| VR-007 | Lineweight hierarchy correct | CHECK |
| VR-008 | Detail completeness (49 details) | PASS |
| VR-009 | Title block accuracy | WARN |
| VR-010 | GCP logo on collection sheets | DEFERRED |

### Billing

- **Backend**: Stripe service (122 lines) — create_customer, create_checkout, portal, webhook
- **Plans**: Free ($0, 1 project, $0.50 AI budget), Pro ($99/mo, 25 projects), Enterprise ($499/mo, unlimited)
- **Frontend**: Pricing tiers displayed but checkout not wired to Stripe yet
- **Token tracking**: Per-call metering with operator markup

### Deployment

| Layer | Platform | URL |
|-------|----------|-----|
| Frontend | Vercel | https://shopdrawings.ai |
| Backend | Railway | https://gpcshopdrawings-production.up.railway.app |
| Database | Railway PostgreSQL 16 | Internal |
| Docs | Railway | /docs (Swagger) |

### Known Gaps

- ProductLibraryView (chunk 14) — hardcoded, no API CRUD
- AdminView (chunk 22) — hardcoded, no wiring
- Stripe frontend — pricing display only, no real checkout
- Settings — localStorage only, no DB sync
- CAD Editor — draws to SVG, no DXF export yet
- Unit tests — 0 (empty test directories)

---

## 2. Repository: ValidKernelOS_VKBUS

### Purpose
The **specification and reference implementation** for the ValidKernel Bus (VKBUS) — a governance protocol that tracks command execution through structured receipts and a centralized registry.

### Key Specifications

| Document | Content |
|----------|---------|
| `VKBUS-SPEC.md` | Core bus specification v0.2.0 |
| `COMMAND-PROTOCOL.md` | Command lifecycle: PROPOSED → APPROVED → EXECUTING → EXECUTED/FAILED |
| `RECEIPT-SCHEMA.md` | Receipt JSON structure (command_id, timestamp, operator, status, outputs, commit_hash) |
| `REGISTRY-FORMAT.md` | Registry schema with command indexing |
| `RUNTIME-GATE.md` | Pre-execution validation gate |

### Architecture

```
docs/
  spec/                      → VKBUS v0.2.0 specification documents
  reference/                 → Reference implementation guides
  governance/                → Governance model documentation

tools/
  validate-receipt.py        → Receipt structure validator
  validate-registry.py       → Registry consistency checker
  runtime-gate.py            → Pre-execution command gate

schemas/
  receipt.schema.json        → JSON Schema for receipts
  registry.schema.json       → JSON Schema for registry
  command.schema.json        → JSON Schema for commands

.github/workflows/
  vkbus-validate.yml         → CI: validate receipts + registry on push/PR
```

### Command Lifecycle

```
PROPOSED → APPROVED → EXECUTING → EXECUTED
                                → FAILED
                                → ROLLED_BACK
```

Each transition produces a **receipt** — a signed JSON record with:
- `command_id` (e.g., `L0-CMD-2026-0209-001`)
- `timestamp`, `operator`, `status`
- `outputs` (files created/modified, commit hashes)
- `validation_result` (PASS/FAIL with details)

### Runtime Gate

Before any command executes, the runtime gate checks:
1. Command is registered in the registry
2. Command status is APPROVED
3. No blocking dependencies
4. Operator has authority

### Observer & Audit System

- VKBUS observers monitor command execution events
- Audit reports generated per wave/session
- Reference Graph integration for cross-repo tracking

---

## 3. Repository: Construction_OS_Registry

### Purpose
The **operational registry** — stores all ValidKernel command records, receipts, and governance tooling for the Construction OS ecosystem. Acts as the single source of truth for what commands have been executed across all repos.

### Structure

```
.validkernel/
  L0-CMD-*/                  → 24 command execution records
  authority/                 → Operator authority definitions
  receipts/                  → Structured receipt JSONs (24 receipts)
  registry/
    command-registry.json    → Master index of all 24 commands
  tools/
    validate-all-receipts.py → Batch receipt validator
    update-record.py         → Record status updater
    runtime-gate.py          → Pre-execution gate

.github/workflows/
  vkg-governance-check.yml   → CI enforcement on push/PR

docs/
  arch-drawings/             → Architecture diagrams
  commands/                  → Command documentation
  lds-governance/            → LDS command governance
  product-data/              → Product reference data
  validkernel/               → VKG spec v0.1
```

### Command Registry (24 Commands)

Key commands tracked:

| ID | Description | Status |
|----|-------------|--------|
| L0-CMD-2026-0208-002 | Parent: Shop Drawing Production System | EXECUTED |
| L0-CMD-2026-0209-001 | ezdxf Pipeline | EXECUTED |
| L0-CMD-2026-0209-002 | SaaS Frontend (25 chunks) | EXECUTED |
| L0-CMD-2026-0209-003 | Backend API (41 endpoints) | EXECUTED |
| L0-CMD-VKG-CI-ENFORCEMENT-001 | CI enforcement for VKG | EXECUTED |
| L0-CMD-VKRT-EXECUTABLE-001 | Runtime gate executable | EXECUTED |

### CI Enforcement

The GitHub Actions workflow (`.github/workflows/vkg-governance-check.yml`) runs on every push and PR to:
1. Validate all receipt structures against schema
2. Check registry consistency (no orphaned receipts)
3. Verify commit hash references exist
4. Block merges if governance checks fail

### Cross-Repository Governance

The registry tracks commands that span all three repos:
- **GPC_Shop_Drawings**: Application commands (DXF pipeline, frontend, backend)
- **ValidKernelOS_VKBUS**: Specification commands (bus protocol, schemas)
- **Construction_OS_Registry**: Self-referential governance commands (CI, tooling)

---

## 4. Cross-Repository Integration Map

```
┌─────────────────────────────────────┐
│     Construction_OS_Registry        │
│  ┌───────────────────────────────┐  │
│  │  command-registry.json (24)   │  │
│  │  receipts/ (24 JSON files)    │  │
│  │  CI: vkg-governance-check.yml │  │
│  └───────────────┬───────────────┘  │
│                  │ tracks            │
└──────────────────┼──────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌───────────────┐    ┌────────────────────┐
│ ValidKernelOS │    │  GPC_Shop_Drawings │
│    VKBUS      │    │                    │
│               │    │  Frontend (Vercel) │
│  Spec v0.2.0  │    │  Backend (Railway) │
│  Schemas      │◄───│  .validkernel/     │
│  Runtime Gate │    │  (local receipts)  │
│  Validators   │    │                    │
└───────────────┘    └────────────────────┘
     defines              implements
```

### Data Flow

1. **User** uploads architectural PDF to ShopDrawing.AI frontend
2. **Frontend** (Vercel) sends screenshot region to backend
3. **Backend** (Railway) calls Claude Vision → analysis JSON
4. **Normalizer** validates against product rules + schema
5. **DXF Generator** produces layered CAD file
6. **Validation Engine** runs VR-001–VR-010
7. **Delivery** packages DXF + validation report + material schedule
8. **Governance** logs each significant operation as a ValidKernel command

---

## 5. Implementation Maturity Assessment

### Fully Implemented (Production-Ready)

| Component | Evidence |
|-----------|----------|
| FastAPI backend | 41 endpoints, async SQLAlchemy, proper auth |
| Clerk authentication | JWT + JWKS validation, webhook sync |
| Claude Vision integration | Real API calls, token metering |
| Groq integration | Real API calls, batch processing |
| DXF generation | 885-line ezdxf pipeline, deterministic layers |
| Validation engine | 10 rules, real enforcement |
| Data normalization | 327 lines, schema validation, generation gates |
| Product rules | 7 GCP products, keynote mapping, substrate rules |
| Detail analysis | 13/49 details with real JSON data |
| Frontend workflow | 8-step persistent workflow |
| CAD editor | 11 tools, snap engine, undo/redo |
| Governance CI | GitHub Actions enforcement |
| Deployment | Live on Vercel + Railway |

### Partially Implemented

| Component | Status | Gap |
|-----------|--------|-----|
| Stripe billing | Backend ready (122 lines) | Frontend not wired |
| Settings | UI works (7 tabs) | No backend persistence |
| Admin panel | UI exists | Hardcoded data |
| Product library | UI exists | No API CRUD |

### Not Implemented

| Component | Priority |
|-----------|----------|
| Unit tests | High — 0 tests exist |
| Integration tests | High |
| CAD editor → DXF export | Medium |
| Batch detail processing | Medium (pipeline exists, needs orchestration) |
| Multi-tenant isolation tests | Medium |

---

## 6. Technology Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React | 18 (CDN) |
| Styling | Tailwind CSS | 3.x (CDN) |
| PDF Viewing | PDF.js | Latest |
| Icons | Lucide | Latest |
| Auth SDK | Clerk | Latest |
| Backend | FastAPI | 0.115.0+ |
| ORM | SQLAlchemy | 2.x (async) |
| Database | PostgreSQL | 16 |
| Migrations | Alembic | Latest |
| CAD | ezdxf | Latest |
| AI (Vision) | Anthropic Claude | claude-3-5-sonnet |
| AI (Text) | Groq Llama | 4 Scout |
| Payments | Stripe | Latest |
| Frontend Deploy | Vercel | Managed |
| Backend Deploy | Railway | Managed |
| CI/CD | GitHub Actions | Managed |
| Governance | ValidKernel | v0.2.0 |

---

## 7. Codebase Metrics

| Metric | Value |
|--------|-------|
| Total repositories | 3 |
| Backend Python files | ~30 |
| Backend lines of code | ~10,000+ |
| Frontend chunks | 29 |
| Assembled HTML size | 457KB |
| API endpoints | 41 |
| Database tables | 7 |
| Database indexes | 6+ |
| AI services | 2 (Claude, Groq) |
| Validation rules | 10 (VR-001–VR-010) |
| GCP product layers | 13 |
| Analyzed details | 13/49 |
| Governance commands | 24 |
| Governance receipts | 24 |
| Unit tests | 0 |
| Live deployments | 2 (Vercel, Railway) |

---

*Report generated by cross-repository audit on 2026-03-20.*
