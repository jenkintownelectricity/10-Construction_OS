/**
 * Trust Boundary Proof Path Tests — Construction_OS
 *
 * Demonstrates end-to-end boundary enforcement for both:
 * - ACCEPTED_TYPED (valid manufacturer detail evidence)
 * - REJECTED_FAIL_CLOSED (various invalid/unsafe inputs)
 *
 * These tests prove the doctrine is operational, not merely visible.
 */

import { evaluateTrustBoundary } from "../proofBoundaryGate";
import type { BoundaryCrossingRequest, Provenance } from "../proofBoundaryGate";

// ─── Test Helpers ─────────────────────────────────────────────────────────────

const VALID_PROVENANCE: Provenance = {
  origin: "manufacturer-barrett-api",
  timestamp: "2026-04-05T12:00:00Z",
  actor: "construction-intake-worker",
  context: "detail-evidence-intake-proof",
};

function makeRequest(overrides: Partial<BoundaryCrossingRequest> = {}): BoundaryCrossingRequest {
  return {
    ingressSource: "USER_UPLOADED_EVIDENCE",
    rawPayload: { detailId: "DET-001", manufacturer: "Barrett", type: "parapet-cap" },
    declaredTrustClass: "UNTRUSTED",
    declaredTarget: "EVIDENCE_ENVELOPE",
    provenance: VALID_PROVENANCE,
    claimedSpinePath: ["S1", "S2", "S3", "S4"],
    constraintPortRef: "construction.constraint.port.evidence-intake",
    schemaValidatorRef: "construction.schema.evidence-envelope-v1",
    ...overrides,
  };
}

// ─── PROOF: ACCEPTED_TYPED ────────────────────────────────────────────────────

describe("PROOF: Valid manufacturer evidence → ACCEPTED_TYPED", () => {
  it("accepts valid uploaded evidence through full spine path", () => {
    const request = makeRequest();
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("ACCEPTED_TYPED");
    expect(result.acceptedAs).toBe("typed_domain_object");
    expect(result.rejectionReason).toBeNull();
    expect(result.receiptPayload.decision).toBe("ACCEPTED_TYPED");
    expect(result.receiptPayload.doctrineVersion).toBe("TRUST-BOUNDARY-ENFORCEMENT-v1");
    expect(result.receiptPayload.sourceGovernanceRepo).toBe("00-validkernel-governance");
    expect(result.receiptPayload.invariantChecks.every((c) => c.result === "PASS")).toBe(true);
  });

  it("accepts service adapter payload with schema + constraint pass", () => {
    const request = makeRequest({
      ingressSource: "SERVICE_ADAPTER",
      declaredTrustClass: "PARTIALLY_TRUSTED",
      declaredTarget: "DOMAIN_PROPOSAL",
      rawPayload: { adapterId: "supabase-detail-sync", payload: { assemblyId: "ASM-100" } },
      provenance: { ...VALID_PROVENANCE, origin: "supabase-adapter" },
    });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("ACCEPTED_TYPED");
    expect(result.acceptedAs).toBe("typed_domain_object");
  });

  it("accepts AI semantic mapping as NON-SOVEREIGN advisory only", () => {
    const request = makeRequest({
      ingressSource: "AI_SEMANTIC_MAPPING",
      declaredTrustClass: "UNTRUSTED",
      declaredTarget: "ADVISORY_ENVELOPE",
      rawPayload: { suggestion: "Parapet cap detail appears to match Barrett P-100" },
      provenance: { ...VALID_PROVENANCE, origin: "claude-advisory", actor: "ai-advisory-worker" },
    });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("ACCEPTED_NON_SOVEREIGN");
    expect(result.acceptedAs).toBe("typed_advisory_object:non_sovereign");
    expect(result.trustClassification).toBe("UNTRUSTED");
  });
});

// ─── PROOF: REJECTED_FAIL_CLOSED ──────────────────────────────────────────────

describe("PROOF: Invalid inputs → REJECTED_FAIL_CLOSED", () => {
  it("rejects undeclared ingress source", () => {
    const request = makeRequest({ ingressSource: null });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_UNDECLARED");
    expect(result.rejectionReason).toContain("not declared");
    expect(result.triggeredInvariants).toContain("E_UNDECLARED_INGRESS");
    expect(result.receiptPayload.decision).toBe("REJECTED_UNDECLARED");
  });

  it("rejects missing provenance", () => {
    const request = makeRequest({ provenance: null });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_PROVENANCE_MISSING");
    expect(result.triggeredInvariants).toContain("E_MISSING_PROVENANCE");
  });

  it("rejects incomplete provenance (missing actor)", () => {
    const request = makeRequest({
      provenance: { origin: "test", timestamp: "2026-04-05T12:00:00Z", actor: "", context: "test" },
    });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_PROVENANCE_MISSING");
  });

  it("rejects UNTRUSTED → GOVERNED_STATE_MUTATION (forbidden crossing)", () => {
    const request = makeRequest({
      declaredTrustClass: "UNTRUSTED",
      declaredTarget: "GOVERNED_STATE_MUTATION",
    });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_FAIL_CLOSED");
    expect(result.rejectionReason).toContain("Forbidden direct crossing");
    expect(result.triggeredInvariants).toContain("E_FORBIDDEN_CROSSING");
  });

  it("rejects UNTRUSTED → DOMAIN_EXECUTION (forbidden crossing)", () => {
    const request = makeRequest({
      declaredTrustClass: "UNTRUSTED",
      declaredTarget: "DOMAIN_EXECUTION",
    });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_FAIL_CLOSED");
    expect(result.triggeredInvariants).toContain("E_FORBIDDEN_CROSSING");
  });

  it("rejects PARTIALLY_TRUSTED → DOMAIN_EXECUTION (forbidden crossing)", () => {
    const request = makeRequest({
      ingressSource: "SERVICE_ADAPTER",
      declaredTrustClass: "PARTIALLY_TRUSTED",
      declaredTarget: "DOMAIN_EXECUTION",
    });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_FAIL_CLOSED");
  });

  it("rejects BROWSER_UI_STATE → TYPED_DOMAIN_OBJECT with missing spine path", () => {
    const request = makeRequest({
      ingressSource: "BROWSER_UI_STATE",
      declaredTrustClass: "UNTRUSTED",
      declaredTarget: "TYPED_DOMAIN_OBJECT",
      claimedSpinePath: [],
    });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_FAIL_CLOSED");
    expect(result.triggeredInvariants).toContain("E_MISSING_SPINE_PATH");
  });

  it("rejects missing schema validator reference", () => {
    const request = makeRequest({ schemaValidatorRef: null });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_SCHEMA_FAILURE");
  });

  it("rejects missing constraint port reference", () => {
    const request = makeRequest({ constraintPortRef: null });
    const result = evaluateTrustBoundary(request);

    expect(result.decision).toBe("REJECTED_CONSTRAINT_FAILURE");
  });
});

// ─── PROOF: Receipt Emission ──────────────────────────────────────────────────

describe("PROOF: Receipts emitted for every decision", () => {
  it("emits receipt on ACCEPTED_TYPED", () => {
    const result = evaluateTrustBoundary(makeRequest());
    const receipt = result.receiptPayload;

    expect(receipt.decision).toBe("ACCEPTED_TYPED");
    expect(receipt.timestamp).toBeTruthy();
    expect(receipt.repoOrigin).toBe("10-Construction_OS");
    expect(receipt.doctrineVersion).toBe("TRUST-BOUNDARY-ENFORCEMENT-v1");
    expect(receipt.sourceGovernanceRepo).toBe("00-validkernel-governance");
    expect(receipt.invariantChecks.length).toBeGreaterThan(0);
    expect(receipt.provenanceBlock).toBeTruthy();
  });

  it("emits receipt on REJECTED_FAIL_CLOSED", () => {
    const result = evaluateTrustBoundary(makeRequest({ ingressSource: null }));
    const receipt = result.receiptPayload;

    expect(receipt.decision).toBe("REJECTED_UNDECLARED");
    expect(receipt.timestamp).toBeTruthy();
    expect(receipt.doctrineVersion).toBe("TRUST-BOUNDARY-ENFORCEMENT-v1");
    expect(receipt.invariantChecks.some((c) => c.result === "FAIL")).toBe(true);
  });

  it("receipt captures full provenance block", () => {
    const result = evaluateTrustBoundary(makeRequest());
    const receipt = result.receiptPayload;

    expect(receipt.provenanceBlock).toEqual(VALID_PROVENANCE);
    expect(receipt.ingressSource).toBe("USER_UPLOADED_EVIDENCE");
    expect(receipt.originalTrustClass).toBe("UNTRUSTED");
    expect(receipt.requestedCrossing).toBe("EVIDENCE_ENVELOPE");
  });
});

// ─── PROOF: Deterministic Replay ──────────────────────────────────────────────

describe("PROOF: Deterministic replay produces identical decisions", () => {
  it("identical input → identical decision object (excluding timestamp)", () => {
    const request = makeRequest();
    const result1 = evaluateTrustBoundary(request);
    const result2 = evaluateTrustBoundary(request);

    expect(result1.decision).toBe(result2.decision);
    expect(result1.acceptedAs).toBe(result2.acceptedAs);
    expect(result1.rejectionReason).toBe(result2.rejectionReason);
    expect(result1.triggeredInvariants).toEqual(result2.triggeredInvariants);
    expect(result1.receiptPayload.invariantChecks).toEqual(result2.receiptPayload.invariantChecks);
  });
});
