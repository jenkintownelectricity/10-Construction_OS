/**
 * Trust Boundary Proof Path — Construction_OS
 *
 * First end-to-end proof that the trust-boundary enforcement doctrine
 * works as a real runtime enforcement mechanism.
 *
 * This module demonstrates both:
 * - ACCEPTED_TYPED (valid manufacturer detail evidence passes)
 * - REJECTED_FAIL_CLOSED (invalid/unsafe input is rejected)
 *
 * Source doctrine: 00-validkernel-governance/docs/doctrine/TRUST-BOUNDARY-ENFORCEMENT-v1.md
 * Authority: L0_ARMAND_LEFEBVRE
 */

// ─── Types (mirrored from governance enforcement primitives) ──────────────────

export type TrustClass = "TRUSTED" | "PARTIALLY_TRUSTED" | "UNTRUSTED";

export type IngressSource =
  | "SERVICE_ADAPTER"
  | "SUPABASE_CLIENT_DATA"
  | "AI_SEMANTIC_MAPPING"
  | "BROWSER_UI_STATE"
  | "USER_UPLOADED_EVIDENCE"
  | "EXTERNAL_API"
  | "OTHER_DECLARED";

export type CrossingTarget =
  | "EVIDENCE_ENVELOPE"
  | "ADVISORY_ENVELOPE"
  | "DOMAIN_PROPOSAL"
  | "TYPED_DOMAIN_OBJECT"
  | "GOVERNED_STATE_MUTATION"
  | "DOMAIN_EXECUTION";

export type BoundaryDecision =
  | "ACCEPTED_TYPED"
  | "ACCEPTED_NON_SOVEREIGN"
  | "REJECTED_FAIL_CLOSED"
  | "REJECTED_UNDECLARED"
  | "REJECTED_PROVENANCE_MISSING"
  | "REJECTED_CONSTRAINT_FAILURE"
  | "REJECTED_SCHEMA_FAILURE";

export type SpineStageRef = "S0" | "S1" | "S2" | "S3" | "S4" | "S5" | "S6" | "S7" | "S8" | "S9" | "S10" | "S11";

export interface Provenance {
  origin: string;
  timestamp: string;
  actor: string;
  context: string;
}

export interface BoundaryCrossingRequest {
  ingressSource: IngressSource | null;
  rawPayload: unknown;
  declaredTrustClass: TrustClass;
  declaredTarget: CrossingTarget;
  provenance: Provenance | null;
  claimedSpinePath: SpineStageRef[];
  constraintPortRef: string | null;
  schemaValidatorRef: string | null;
}

export interface BoundaryCrossingResult {
  decision: BoundaryDecision;
  trustClassification: TrustClass;
  target: CrossingTarget;
  acceptedAs: string | null;
  rejectionReason: string | null;
  triggeredInvariants: string[];
  receiptPayload: TrustBoundaryReceipt;
}

export interface TrustBoundaryReceipt {
  timestamp: string;
  repoOrigin: string;
  moduleOrigin: string;
  ingressSource: string;
  originalTrustClass: TrustClass;
  requestedCrossing: CrossingTarget;
  spineStagePathDeclared: SpineStageRef[];
  constraintPortId: string | null;
  schemaValidatorId: string | null;
  decision: BoundaryDecision;
  invariantChecks: Array<{ id: string; result: "PASS" | "FAIL" }>;
  provenanceBlock: Provenance | null;
  doctrineVersion: string;
  sourceGovernanceRepo: string;
}

// ─── Forbidden Crossing Table ─────────────────────────────────────────────────

const FORBIDDEN_DIRECT_CROSSINGS: ReadonlySet<string> = new Set([
  "UNTRUSTED:GOVERNED_STATE_MUTATION",
  "UNTRUSTED:DOMAIN_EXECUTION",
  "PARTIALLY_TRUSTED:GOVERNED_STATE_MUTATION",
  "PARTIALLY_TRUSTED:DOMAIN_EXECUTION",
]);

// ─── Default Trust Classification ─────────────────────────────────────────────

function classifyIngress(source: IngressSource): TrustClass {
  switch (source) {
    case "SERVICE_ADAPTER":
    case "SUPABASE_CLIENT_DATA":
      return "PARTIALLY_TRUSTED";
    case "AI_SEMANTIC_MAPPING":
    case "BROWSER_UI_STATE":
    case "USER_UPLOADED_EVIDENCE":
    case "EXTERNAL_API":
    case "OTHER_DECLARED":
      return "UNTRUSTED";
  }
}

// ─── Core Enforcement Gate ────────────────────────────────────────────────────

export function evaluateTrustBoundary(request: BoundaryCrossingRequest): BoundaryCrossingResult {
  const invariantChecks: Array<{ id: string; result: "PASS" | "FAIL" }> = [];
  const triggeredInvariants: string[] = [];
  const now = new Date().toISOString();

  function fail(decision: BoundaryDecision, reason: string): BoundaryCrossingResult {
    return {
      decision,
      trustClassification: request.declaredTrustClass,
      target: request.declaredTarget,
      acceptedAs: null,
      rejectionReason: reason,
      triggeredInvariants,
      receiptPayload: buildReceipt(request, decision, invariantChecks, now),
    };
  }

  // 1. Declared ingress
  if (!request.ingressSource) {
    invariantChecks.push({ id: "DECLARED_INGRESS", result: "FAIL" });
    triggeredInvariants.push("E_UNDECLARED_INGRESS");
    return fail("REJECTED_UNDECLARED", "Ingress source is not declared");
  }
  invariantChecks.push({ id: "DECLARED_INGRESS", result: "PASS" });

  // 2. Provenance present
  if (!request.provenance || !request.provenance.origin || !request.provenance.timestamp || !request.provenance.actor) {
    invariantChecks.push({ id: "PROVENANCE_PRESENT", result: "FAIL" });
    triggeredInvariants.push("E_MISSING_PROVENANCE");
    return fail("REJECTED_PROVENANCE_MISSING", "Provenance is missing or incomplete");
  }
  invariantChecks.push({ id: "PROVENANCE_PRESENT", result: "PASS" });

  // 3. Forbidden crossing check
  const crossingKey = `${request.declaredTrustClass}:${request.declaredTarget}`;
  if (FORBIDDEN_DIRECT_CROSSINGS.has(crossingKey)) {
    invariantChecks.push({ id: "ALLOWED_CROSSING", result: "FAIL" });
    triggeredInvariants.push("E_FORBIDDEN_CROSSING");
    return fail("REJECTED_FAIL_CLOSED", `Forbidden direct crossing: ${crossingKey}`);
  }
  invariantChecks.push({ id: "ALLOWED_CROSSING", result: "PASS" });

  // 4. Spine path declared
  if (!request.claimedSpinePath || request.claimedSpinePath.length === 0) {
    invariantChecks.push({ id: "SPINE_PATH_DECLARED", result: "FAIL" });
    triggeredInvariants.push("E_MISSING_SPINE_PATH");
    return fail("REJECTED_FAIL_CLOSED", "No spine stage path declared");
  }
  invariantChecks.push({ id: "SPINE_PATH_DECLARED", result: "PASS" });

  // 5. Schema validator ref
  if (!request.schemaValidatorRef) {
    invariantChecks.push({ id: "SCHEMA_VALIDATOR_REF", result: "FAIL" });
    triggeredInvariants.push("E_SCHEMA_FAILURE");
    return fail("REJECTED_SCHEMA_FAILURE", "Schema validator reference is missing");
  }
  invariantChecks.push({ id: "SCHEMA_VALIDATOR_REF", result: "PASS" });

  // 6. Constraint port ref
  if (!request.constraintPortRef) {
    invariantChecks.push({ id: "CONSTRAINT_PORT_REF", result: "FAIL" });
    triggeredInvariants.push("E_CONSTRAINT_HALT");
    return fail("REJECTED_CONSTRAINT_FAILURE", "Constraint port reference is missing");
  }
  invariantChecks.push({ id: "CONSTRAINT_PORT_REF", result: "PASS" });

  // 7. AI advisory → non-sovereign
  if (request.ingressSource === "AI_SEMANTIC_MAPPING") {
    invariantChecks.push({ id: "AI_NON_SOVEREIGN", result: "PASS" });
    return {
      decision: "ACCEPTED_NON_SOVEREIGN",
      trustClassification: "UNTRUSTED",
      target: request.declaredTarget,
      acceptedAs: "typed_advisory_object:non_sovereign",
      rejectionReason: null,
      triggeredInvariants,
      receiptPayload: buildReceipt(request, "ACCEPTED_NON_SOVEREIGN", invariantChecks, now),
    };
  }

  // 8. Standard acceptance
  invariantChecks.push({ id: "TYPED_BOUNDARY", result: "PASS" });
  return {
    decision: "ACCEPTED_TYPED",
    trustClassification: classifyIngress(request.ingressSource),
    target: request.declaredTarget,
    acceptedAs: "typed_domain_object",
    rejectionReason: null,
    triggeredInvariants,
    receiptPayload: buildReceipt(request, "ACCEPTED_TYPED", invariantChecks, now),
  };
}

// ─── Receipt Builder ──────────────────────────────────────────────────────────

function buildReceipt(
  request: BoundaryCrossingRequest,
  decision: BoundaryDecision,
  invariantChecks: Array<{ id: string; result: "PASS" | "FAIL" }>,
  timestamp: string,
): TrustBoundaryReceipt {
  return {
    timestamp,
    repoOrigin: "10-Construction_OS",
    moduleOrigin: "2-Engines-Tools-Datasets/trust-boundary-proof/proofBoundaryGate.ts",
    ingressSource: request.ingressSource ?? "UNDECLARED",
    originalTrustClass: request.declaredTrustClass,
    requestedCrossing: request.declaredTarget,
    spineStagePathDeclared: request.claimedSpinePath,
    constraintPortId: request.constraintPortRef,
    schemaValidatorId: request.schemaValidatorRef,
    decision,
    invariantChecks,
    provenanceBlock: request.provenance,
    doctrineVersion: "TRUST-BOUNDARY-ENFORCEMENT-v1",
    sourceGovernanceRepo: "00-validkernel-governance",
  };
}
