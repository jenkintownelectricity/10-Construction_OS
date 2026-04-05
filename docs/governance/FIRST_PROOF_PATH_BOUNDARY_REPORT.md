# First Proof Path — Trust Boundary Enforcement Report

**Authority:** L0_ARMAND_LEFEBVRE  
**Date:** 2026-04-05  
**Domain:** Construction Building Envelope Systems  
**Source Doctrine:** 00-validkernel-governance/docs/doctrine/TRUST-BOUNDARY-ENFORCEMENT-v1.md  

---

## Summary

This report documents the first end-to-end proof that the trust-boundary enforcement doctrine operates as a real runtime enforcement mechanism in the construction domain.

The proof demonstrates both:
- **ACCEPTED_TYPED** — valid manufacturer detail evidence passes through the full enforcement gate
- **REJECTED_FAIL_CLOSED** — invalid/unsafe inputs are rejected with specific reason codes

---

## Proof Path: Manufacturer Detail Evidence Intake

### Scenario
A manufacturer (Barrett) submits detail evidence (parapet cap detail) via the construction intake system. The evidence originates as UNTRUSTED user-uploaded content and must pass through the trust boundary enforcement gate before it can become a Typed Domain Object in governed execution.

### Enforcement Path
```
User uploaded evidence (UNTRUSTED)
  → Evidence Intake Envelope (declared ingress)
    → Schema Validation (S3: construction.schema.evidence-envelope-v1)
      → Constraint Port Evaluation (S4: construction.constraint.port.evidence-intake)
        → Typed Evidence Object (ACCEPTED_TYPED)
          → Receipt Emitted
```

### Test Coverage

| Test | Input | Expected | Result |
|------|-------|----------|--------|
| Valid evidence upload | Full provenance, schema, constraint refs | ACCEPTED_TYPED | PASS |
| Service adapter payload | Supabase detail sync | ACCEPTED_TYPED | PASS |
| AI semantic mapping | Claude advisory suggestion | ACCEPTED_NON_SOVEREIGN | PASS |
| Undeclared ingress | null source | REJECTED_UNDECLARED | PASS |
| Missing provenance | null provenance | REJECTED_PROVENANCE_MISSING | PASS |
| Incomplete provenance | Empty actor | REJECTED_PROVENANCE_MISSING | PASS |
| UNTRUSTED → state mutation | Direct state mutation attempt | REJECTED_FAIL_CLOSED | PASS |
| UNTRUSTED → domain execution | Direct execution attempt | REJECTED_FAIL_CLOSED | PASS |
| PARTIALLY_TRUSTED → domain execution | Adapter direct execution | REJECTED_FAIL_CLOSED | PASS |
| Missing spine path | Empty path array | REJECTED_FAIL_CLOSED | PASS |
| Missing schema validator | null ref | REJECTED_SCHEMA_FAILURE | PASS |
| Missing constraint port | null ref | REJECTED_CONSTRAINT_FAILURE | PASS |
| Deterministic replay | Same input twice | Identical decisions | PASS |

### Invariant Checks Demonstrated

- DECLARED_INGRESS: verified on every crossing
- PROVENANCE_PRESENT: verified on every crossing
- ALLOWED_CROSSING: forbidden crossings blocked
- SPINE_PATH_DECLARED: empty paths rejected
- SCHEMA_VALIDATOR_REF: missing refs rejected
- CONSTRAINT_PORT_REF: missing refs rejected
- AI_NON_SOVEREIGN: AI output explicitly non-sovereign
- TYPED_BOUNDARY: final acceptance check

---

## Files

| File | Purpose |
|------|---------|
| `2-Engines-Tools-Datasets/trust-boundary-proof/proofBoundaryGate.ts` | Enforcement gate implementation |
| `2-Engines-Tools-Datasets/trust-boundary-proof/test/proofBoundaryGate.test.ts` | 13 test cases proving accept + reject |
| `docs/governance/FIRST_PROOF_PATH_BOUNDARY_REPORT.md` | This report |
| `receipts/governance/first_proof_path_receipt.json` | Machine-readable receipt |
