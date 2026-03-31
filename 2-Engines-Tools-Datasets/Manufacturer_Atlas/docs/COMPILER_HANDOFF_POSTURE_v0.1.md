# Compiler Handoff Posture v0.1

**PURPOSE:** Document the typed output contract from the Barrett PMMA
evaluator for downstream compiler consumption.
**DOWNSTREAM CONSUMER:** ShopDrawing_Compiler (no writes in this pass)

---

## Typed Output: BarrettPmmaEvaluationResult

```typescript
interface BarrettPmmaEvaluationResult {
  evaluation_status: "PASS" | "WARN" | "HALT";
  manufacturer_id: string | null;
  system_family: string | null;
  compatible_products: string[];
  required_primer: string | null;
  required_prep: string[];
  required_cure_before_overlay: string | null;
  blocking_rules: string[];
  warning_rules: string[];
  evidence_sources: string[];
  notes: string[];
}
```

## Field Guarantees

| Field | Guaranteed | Notes |
|-------|-----------|-------|
| evaluation_status | Always present | One of PASS, WARN, HALT |
| manufacturer_id | null if not found | Set only if Barrett identity is in truth-cache |
| system_family | null if not found | Set only if PMMA system is in truth-cache |
| compatible_products | Empty if not found | Lists product IDs if PMMA products exist |
| required_primer | null currently | Requires Barrett primer record in truth-cache |
| required_prep | Best-effort from grounded rules | surface_preparation, substrate_moisture_test |
| required_cure_before_overlay | "30 minutes (1/2-hour cure)" | Known domain requirement |
| blocking_rules | Lists all blocking reasons | Critical for downstream decision |
| warning_rules | Lists applicable grounded rules | Informational |
| evidence_sources | Lists truth-cache paths consulted | Audit trail |
| notes | Honest status of data availability | Always includes scaffold/missing notices |

## What Is NOT Guaranteed

- PASS status (current data will produce HALT because Barrett records are not yet ingested)
- Specific product IDs (scaffold until real manufacturer data is available)
- Primer product specification (not yet in truth-cache)
- Complete assembly layer sequence (requires manufacturer TDS)
- FM approval certifications (requires manufacturer FM tables)

## Compiler Consumption Rules

1. Compiler MUST check `evaluation_status` before proceeding
2. If HALT: compiler must not proceed with the path
3. If WARN: compiler may proceed but must propagate warnings
4. If PASS: compiler may use all fields for downstream generation
5. Compiler must not treat scaffold or null fields as grounded truth
6. Compiler is a downstream consumer only — it does not modify this output

## Current Expected Behavior

With current truth-cache content (scaffold manufacturer, no Barrett/PMMA records):

```
evaluation_status: HALT
blocking_rules:
  - MISSING_MANUFACTURER: Barrett identity not in truth-cache
  - MISSING_PRODUCT: PMMA product not in truth-cache
  - MISSING_SYSTEM: PMMA system not in truth-cache
required_cure_before_overlay: "30 minutes (1/2-hour cure)"
```

This is correct fail-closed behavior. The path becomes viable when
Barrett-specific records are ingested into 10-building-envelope-manufacturer-os
and consumed into truth-cache.
