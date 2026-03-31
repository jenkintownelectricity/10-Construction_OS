/**
 * Manufacturer Atlas Runtime — Local Types
 *
 * Local typing for consumed upstream manufacturer truth records.
 * These types are read-validation helpers, not canonical truth schemas.
 * Upstream authority: 10-building-envelope-manufacturer-os
 */

export type RecordStatus = "grounded" | "derived" | "scaffold" | "deferred" | "unverified";

export interface UpstreamRef {
  source: string;
  role: "consumed_reference";
}

export interface ManufacturerRecord {
  record_id: string;
  type: "manufacturer";
  label: string;
  domain: string;
  status: RecordStatus;
  scaffold_reason?: string;
  _upstream: UpstreamRef;
}

export interface ProductRecord {
  record_id: string;
  type: "product";
  label: string;
  domain: string;
  status: RecordStatus;
  product_category: string;
  material_class?: string;
  envelope_zone?: string;
  scaffold_reason?: string;
  _upstream: UpstreamRef;
}

export interface SystemRecord {
  record_id: string;
  type: "system_family" | "system" | "assembly";
  label: string;
  domain: string;
  status: RecordStatus;
  system_type?: string;
  envelope_zone?: string;
  attachment_method?: string;
  drainage_type?: string;
  manufacturer_ref?: string;
  family_ref?: string;
  system_ref?: string;
  condition_ref?: string;
  scaffold_reason?: string;
  _upstream: UpstreamRef;
}

export type RuleFailAction = "BLOCK" | "WARN" | "REQUIRE_HUMAN_STAMP";

export interface InstallationRuleRecord {
  record_id: string;
  type: "installation_rule";
  label: string;
  domain: string;
  status: RecordStatus;
  rule_type: string;
  authority: string;
  fail_action: RuleFailAction;
  description: string;
  _upstream: UpstreamRef;
}

export interface CertificationRuleRecord {
  record_id: string;
  type: "certification_rule";
  label: string;
  domain: string;
  status: RecordStatus;
  rule_type: string;
  authority: string;
  fail_action: RuleFailAction;
  description: string;
  _upstream: UpstreamRef;
}

export interface ConstraintRecord {
  constraint_id: string;
  system: string;
  condition: string;
  substrate: string;
  required_products: string[];
  required_rules: string[];
  output_detail_reference: string;
  status: RecordStatus;
  _upstream: UpstreamRef;
}

export interface ConditionRecord {
  condition_id: string;
  label: string;
  status: RecordStatus;
  trigger?: string;
  code_reference?: string;
  substrate_type?: string;
  requirements?: string[];
  _upstream: UpstreamRef;
}

export type CompatibilityEntry = ConstraintRecord | ConditionRecord;

export type EvaluationStatus = "PASS" | "WARN" | "HALT";

export interface BarrettPmmaEvaluationResult {
  evaluation_status: EvaluationStatus;
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

export interface LoaderFailure {
  loader: string;
  path: string;
  reason: string;
}
