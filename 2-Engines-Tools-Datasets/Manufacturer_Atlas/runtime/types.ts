/**
 * Manufacturer Atlas Runtime — Local Types
 *
 * Local typing for consumed upstream manufacturer truth records.
 * These types are read-validation helpers, not canonical truth schemas.
 * Upstream authority: 10-building-envelope-manufacturer-os
 *
 * Supports both legacy scaffold shapes (record_id/type/label) and
 * upstream authority shapes (manufacturer_id/name/product_family).
 */

export type RecordStatus = "grounded" | "derived" | "scaffold" | "deferred" | "unverified";

export interface UpstreamRef {
  source: string;
  role: "consumed_reference";
}

// --- Manufacturer ---

export interface ManufacturerRecord {
  // Upstream authority shape
  manufacturer_id?: string;
  name?: string;
  system_families_supported?: string[];
  authority?: string;
  source_authority?: string;
  // Legacy scaffold shape
  record_id?: string;
  type?: "manufacturer";
  label?: string;
  scaffold_reason?: string;
  _upstream?: UpstreamRef;
  // Common
  domain: string;
  status: RecordStatus;
  record_origin?: string;
  authority_scope?: string;
  created_by?: string;
  verification_status?: string;
}

// --- Product ---

export interface ProductRecord {
  // Upstream authority shape
  product_id?: string;
  manufacturer_id?: string;
  product_family?: string;
  product_role?: string;
  system_family?: string;
  // Legacy scaffold shape
  record_id?: string;
  type?: "product";
  label?: string;
  product_category?: string;
  material_class?: string;
  envelope_zone?: string;
  scaffold_reason?: string;
  _upstream?: UpstreamRef;
  // Common
  domain?: string;
  status: RecordStatus;
  record_origin?: string;
  authority_scope?: string;
  created_by?: string;
  verification_status?: string;
}

// --- System ---

export interface SystemRecord {
  // Upstream authority shape
  system_id?: string;
  manufacturer_id?: string;
  system_family?: string;
  supported_conditions?: string[];
  // Legacy scaffold shape
  record_id?: string;
  type?: "system_family" | "system" | "assembly";
  label?: string;
  system_type?: string;
  envelope_zone?: string;
  attachment_method?: string;
  drainage_type?: string;
  manufacturer_ref?: string;
  family_ref?: string;
  system_ref?: string;
  condition_ref?: string;
  scaffold_reason?: string;
  _upstream?: UpstreamRef;
  // Common
  domain?: string;
  status: RecordStatus;
  record_origin?: string;
  authority_scope?: string;
  created_by?: string;
  verification_status?: string;
}

// --- Rules ---

export type RuleFailAction = "BLOCK" | "WARN" | "REQUIRE_HUMAN_STAMP";

export interface InstallationRuleRecord {
  // Upstream authority shape
  rule_id?: string;
  manufacturer_id?: string;
  system_family?: string;
  rule_type: string;
  required_cure_time?: string;
  // Legacy scaffold shape
  record_id?: string;
  type?: "installation_rule";
  label?: string;
  fail_action?: RuleFailAction;
  description?: string;
  _upstream?: UpstreamRef;
  // Common
  domain?: string;
  status: RecordStatus;
  authority?: string;
  record_origin?: string;
  authority_scope?: string;
  created_by?: string;
  verification_status?: string;
}

export interface CertificationRuleRecord {
  record_id?: string;
  type?: "certification_rule";
  label?: string;
  domain?: string;
  status: RecordStatus;
  rule_type: string;
  authority?: string;
  fail_action?: RuleFailAction;
  description?: string;
  _upstream?: UpstreamRef;
  record_origin?: string;
  authority_scope?: string;
  created_by?: string;
  verification_status?: string;
}

// --- Compatibility ---

export interface CompatibilityRecord {
  // Upstream authority shape
  compatibility_id?: string;
  manufacturer_id?: string;
  system_family?: string;
  compatible_products?: string[];
  supported_conditions?: string[];
  // Legacy constraint shape
  constraint_id?: string;
  system?: string;
  condition?: string;
  substrate?: string;
  required_products?: string[];
  required_rules?: string[];
  output_detail_reference?: string;
  // Legacy condition shape
  condition_id?: string;
  label?: string;
  trigger?: string;
  code_reference?: string;
  substrate_type?: string;
  requirements?: string[];
  // Common
  status: RecordStatus;
  _upstream?: UpstreamRef;
  record_origin?: string;
  authority_scope?: string;
  created_by?: string;
  verification_status?: string;
}

// --- Evaluator output ---

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
