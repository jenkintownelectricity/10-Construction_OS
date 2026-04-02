# Manufacturer Onboarding Documentation

## Purpose

This directory contains all documentation required for manufacturer system onboarding into the Construction OS detail generation platform.

## Manuals

| Document | Audience | Description |
|----------|----------|-------------|
| [manufacturer-detail-system-input-manual-v0.1.md](manufacturer-detail-system-input-manual-v0.1.md) | Manufacturers | Required inputs, DXF requirements, ownership classes, submission checklist |
| [manufacturer-system-ingestion-operator-manual-v0.1.md](manufacturer-system-ingestion-operator-manual-v0.1.md) | Internal operators | Golden DXF selection, progressive batching, layer mapping, sub-10-minute onboarding flow |

## DXF Semantic Taxonomy

| Document | Description |
|----------|-------------|
| [dxf-semantic-taxonomy-v0.1.md](dxf-semantic-taxonomy-v0.1.md) | Three ownership classes (SYSTEM_OWNED, CONTEXT_ONLY, ANNOTATION), entity type defaults, layer pattern mappings, ambiguity handling |

## Barrett Onboarding

| Document | Description |
|----------|-------------|
| [barrett-onboarding-flow-v0.1.md](barrett-onboarding-flow-v0.1.md) | Sub-10-minute onboarding flow for Barrett's 4 system families (Black Pearl, PMMA, RamProof GC, RamTough 250) |

## Related Files

| Location | Description |
|----------|-------------|
| `source/barrett/definitions/` | Barrett assembly family definition packs (4 families) |
| `source/barrett/audits/` | Assembly readiness audit |
| `source/barrett/receipts/` | Onboarding and hardening receipts |
| `config/manufacturer/` | DXF semantic defaults, ownership rules, readiness classification |
| `schemas/manufacturer/` | Family definition, enrichment record, readiness record schemas |

## DXF Ingestion

Raw DXF-to-JSON ingestion is handled by the existing ingestor tool (`tools/trace_ingestor.py` and related geometry tools). This documentation covers the semantic enrichment and manufacturer onboarding layer that sits on top of raw ingestion — it does not replace or modify the ingestor.
