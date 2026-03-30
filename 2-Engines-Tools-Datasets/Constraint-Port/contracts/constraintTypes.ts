/**
 * Constraint Port — Core Type Definitions
 * Types/interfaces only. No runtime code.
 *
 * Authority: L0-CMD-CONOS-VKGL04R-CPORT-001
 */

export type ConstraintType =
  | "PHYSICAL_INCOMPATIBILITY"
  | "CODE_VIOLATION"
  | "WARRANTY_VOID"
  | "SPEC_CONFLICT"
  | "INSTALL_SEQUENCE_VIOLATION"
  | "RESPONSIBILITY_CONFLICT";

export type LogicOperator = "BLOCK" | "WARN" | "REQUIRE_HUMAN_STAMP";

export type DecisionAction =
  | "PASS"
  | "WARN"
  | "BLOCK"
  | "REQUIRE_HUMAN_STAMP"
  | "DEFER_FOR_MISSING_EVIDENCE";

export type Severity = "INFO" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export type EvidenceCompleteness = "COMPLETE" | "PARTIAL" | "MISSING";

export type EntityType =
  | "material"
  | "assembly"
  | "system"
  | "method"
  | "sequence"
  | "scope_boundary";

export interface AppliesTo {
  entity_type: EntityType;
  entity_ids?: string[];
  entity_filter?: Record<string, unknown>;
}

export interface Trigger {
  condition: string;
  context_requirements?: string[];
}

export interface DependencyMap {
  kernels?: string[];
  external_refs?: string[];
}

export interface ConstraintObject {
  rule_id: string;
  rule_label: string;
  rule_family: string;
  constraint_type: ConstraintType;
  source_authority: string;
  source_ref: string;
  applies_to: AppliesTo;
  trigger: Trigger;
  dependency_map: DependencyMap;
  logic_operator: LogicOperator;
  required_evidence: string[];
  decision_on_fail: DecisionAction;
  notes?: string;
}

export interface EvidenceItem {
  key: string;
  value: unknown;
  source: string;
  verified?: boolean;
}

export interface ConstraintEvidence {
  evidence_id: string;
  rule_id: string;
  timestamp: string;
  evidence_items: EvidenceItem[];
  completeness: EvidenceCompleteness;
  missing_items?: string[];
}

export interface TriggeredBy {
  evidence_key: string;
  evidence_value: unknown;
  threshold?: unknown;
  comparison?: string;
}

export interface HumanOverride {
  overridden_by: string;
  override_timestamp: string;
  override_rationale: string;
  original_action: "BLOCK" | "REQUIRE_HUMAN_STAMP";
}

export interface ConstraintDecision {
  decision_id: string;
  rule_id: string;
  evidence_id: string;
  timestamp: string;
  action: DecisionAction;
  severity: Severity;
  rationale: string;
  source_authority: string;
  triggered_by?: TriggeredBy;
  dependency_chain?: string[];
  deterministic: true;
  human_override?: HumanOverride;
}
