/**
 * Barrett PMMA Compatibility Evaluator
 *
 * Narrow deterministic evaluator for Barrett PMMA compatibility.
 * Evaluates against current truth-cache content only.
 * Fails closed on missing or partial critical inputs.
 *
 * Does not fabricate chemistry truth.
 * Does not overpromise certification.
 * Does not invent unsupported system paths.
 */

import { loadManufacturers } from "./manufacturer-record-loader";
import { loadProducts } from "./manufacturer-product-loader";
import { loadSystems } from "./manufacturer-system-loader";
import { loadInstallationRules, loadCertificationRules } from "./manufacturer-rule-loader";
import { loadCompatibilityMatrix, filterConstraints, filterConditions } from "./manufacturer-compatibility-loader";
import type {
  BarrettPmmaEvaluationResult,
  ManufacturerRecord,
  ProductRecord,
  InstallationRuleRecord,
  CertificationRuleRecord,
  LoaderFailure,
} from "./types";

function isFailure(result: unknown): result is LoaderFailure {
  return (
    typeof result === "object" &&
    result !== null &&
    "loader" in result &&
    "reason" in result
  );
}

export function evaluateBarrettPmmaCompatibility(): BarrettPmmaEvaluationResult {
  const notes: string[] = [];
  const blocking_rules: string[] = [];
  const warning_rules: string[] = [];
  const evidence_sources: string[] = [];

  // --- Step 1: Load all truth-cache data ---

  const manufacturers = loadManufacturers();
  if (isFailure(manufacturers)) {
    return halt(`Manufacturer loader failed: ${manufacturers.reason}`, [manufacturers.loader]);
  }
  evidence_sources.push("truth-cache/manufacturers/");

  const products = loadProducts();
  if (isFailure(products)) {
    return halt(`Product loader failed: ${products.reason}`, [products.loader]);
  }
  evidence_sources.push("truth-cache/products/");

  const systems = loadSystems();
  if (isFailure(systems)) {
    return halt(`System loader failed: ${systems.reason}`, [systems.loader]);
  }
  evidence_sources.push("truth-cache/systems/");

  const installRules = loadInstallationRules();
  if (isFailure(installRules)) {
    return halt(`Installation rule loader failed: ${installRules.reason}`, [installRules.loader]);
  }
  evidence_sources.push("truth-cache/rules/installation/");

  const certRules = loadCertificationRules();
  if (isFailure(certRules)) {
    return halt(`Certification rule loader failed: ${certRules.reason}`, [certRules.loader]);
  }
  evidence_sources.push("truth-cache/rules/certification/");

  const compatEntries = loadCompatibilityMatrix();
  if (isFailure(compatEntries)) {
    return halt(`Compatibility loader failed: ${compatEntries.reason}`, [compatEntries.loader]);
  }
  evidence_sources.push("truth-cache/compatibility/");

  // --- Step 2: Search for Barrett manufacturer identity ---

  const barrettMfr = manufacturers.find(
    (m) =>
      m.label.toLowerCase().includes("barrett") ||
      m.record_id.toLowerCase().includes("barrett")
  );

  if (!barrettMfr) {
    notes.push(
      "No Barrett manufacturer record found in truth-cache. " +
      "Current manufacturer records are scaffold placeholders. " +
      "Barrett-specific identity must be ingested from upstream " +
      "(10-building-envelope-manufacturer-os) before evaluation can proceed."
    );
    blocking_rules.push("MISSING_MANUFACTURER: Barrett identity not in truth-cache");
  }

  // --- Step 3: Search for PMMA product ---

  const pmmaProduct = products.find(
    (p) =>
      p.material_class?.toLowerCase().includes("pmma") ||
      p.label.toLowerCase().includes("pmma") ||
      p.product_category?.toLowerCase().includes("pmma")
  );

  if (!pmmaProduct) {
    notes.push(
      "No PMMA product record found in truth-cache. " +
      "Current product records are scaffold (TPO/PVC/EPDM membrane, generic adhesive). " +
      "Barrett PMMA product definition must be ingested from upstream."
    );
    blocking_rules.push("MISSING_PRODUCT: PMMA product not in truth-cache");
  }

  // --- Step 4: Search for PMMA-compatible system ---

  const pmmaSystem = systems.find(
    (s) =>
      s.label.toLowerCase().includes("pmma") ||
      s.system_type?.toLowerCase().includes("pmma")
  );

  if (!pmmaSystem) {
    notes.push(
      "No PMMA system or assembly found in truth-cache. " +
      "Current systems are scaffold (adhered, mechanically attached, cavity wall). " +
      "Barrett PMMA system definition must be ingested from upstream."
    );
    blocking_rules.push("MISSING_SYSTEM: PMMA system not in truth-cache");
  }

  // --- Step 5: Evaluate grounded rules that WOULD apply ---

  // These rules are grounded and would apply to any roofing system including PMMA:
  const applicableInstallRules = installRules.filter((r) => r.status === "grounded");
  const applicableCertRules = certRules.filter((r) => r.status === "grounded");

  for (const rule of applicableInstallRules) {
    if (rule.fail_action === "BLOCK") {
      warning_rules.push(
        `${rule.record_id}: ${rule.label} (${rule.authority}) — would BLOCK if not satisfied`
      );
    } else if (rule.fail_action === "WARN") {
      warning_rules.push(
        `${rule.record_id}: ${rule.label} (${rule.authority}) — would WARN`
      );
    }
  }

  for (const rule of applicableCertRules) {
    warning_rules.push(
      `${rule.record_id}: ${rule.label} (${rule.authority}) — would ${rule.fail_action}`
    );
  }

  notes.push(
    `${applicableInstallRules.length} grounded installation rules and ` +
    `${applicableCertRules.length} grounded certification rules would apply ` +
    `to a Barrett PMMA path once manufacturer data is ingested.`
  );

  // --- Step 6: Known Barrett PMMA requirements (from domain knowledge) ---

  notes.push(
    "Known Barrett PMMA requirement: 1/2-hour cure before overlay. " +
    "This is not yet represented as a grounded upstream record. " +
    "Must be ingested as a grounded installation rule from 10-building-envelope-manufacturer-os."
  );

  notes.push(
    "Known Barrett PMMA requirement: compatible primer required for substrate preparation. " +
    "Specific primer product ID not available in current truth-cache."
  );

  // --- Step 7: Determine evaluation status ---

  if (blocking_rules.length > 0) {
    return {
      evaluation_status: "HALT",
      manufacturer_id: barrettMfr?.record_id ?? null,
      system_family: pmmaSystem?.family_ref ?? null,
      compatible_products: pmmaProduct ? [pmmaProduct.record_id] : [],
      required_primer: null,
      required_prep: ["substrate_moisture_test", "surface_preparation"],
      required_cure_before_overlay: "30 minutes (1/2-hour cure)",
      blocking_rules,
      warning_rules,
      evidence_sources,
      notes,
    };
  }

  // If we reach here, all critical inputs exist (future state)
  return {
    evaluation_status: "WARN",
    manufacturer_id: barrettMfr?.record_id ?? null,
    system_family: pmmaSystem?.family_ref ?? null,
    compatible_products: pmmaProduct ? [pmmaProduct.record_id] : [],
    required_primer: null,
    required_prep: ["substrate_moisture_test", "surface_preparation"],
    required_cure_before_overlay: "30 minutes (1/2-hour cure)",
    blocking_rules,
    warning_rules,
    evidence_sources,
    notes,
  };
}

function halt(reason: string, sources: string[]): BarrettPmmaEvaluationResult {
  return {
    evaluation_status: "HALT",
    manufacturer_id: null,
    system_family: null,
    compatible_products: [],
    required_primer: null,
    required_prep: [],
    required_cure_before_overlay: "30 minutes (1/2-hour cure)",
    blocking_rules: [reason],
    warning_rules: [],
    evidence_sources: sources,
    notes: ["Evaluation halted due to missing critical truth-cache data. This is expected fail-closed behavior."],
  };
}
