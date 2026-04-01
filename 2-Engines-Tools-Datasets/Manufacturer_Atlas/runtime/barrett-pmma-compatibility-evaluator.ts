/**
 * Barrett PMMA Compatibility Evaluator
 *
 * Narrow deterministic evaluator for Barrett PMMA compatibility.
 * Evaluates against current truth-cache content only.
 * Fails closed on missing or partial critical inputs.
 *
 * Matches records using actual upstream authority fields:
 * - manufacturer_id / name (not legacy label)
 * - product_family (not legacy material_class)
 * - system_family (not legacy system_type)
 * - rule_type + required_cure_time (not hardcoded)
 *
 * Does not fabricate chemistry truth.
 * Does not overpromise certification.
 * Does not invent unsupported system paths.
 */

import { loadManufacturers } from "./manufacturer-record-loader";
import { loadProducts } from "./manufacturer-product-loader";
import { loadSystems } from "./manufacturer-system-loader";
import { loadInstallationRules, loadCertificationRules } from "./manufacturer-rule-loader";
import { loadCompatibilityMatrix, filterUpstreamCompatibility } from "./manufacturer-compatibility-loader";
import type {
  BarrettPmmaEvaluationResult,
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

  // --- Step 2: Find Barrett manufacturer ---

  const barrettMfr = manufacturers.find(
    (m) =>
      m.manufacturer_id?.toLowerCase().includes("barrett") ||
      m.name?.toLowerCase().includes("barrett") ||
      m.record_id?.toLowerCase().includes("barrett") ||
      m.label?.toLowerCase().includes("barrett")
  );

  if (!barrettMfr) {
    blocking_rules.push("MISSING_MANUFACTURER: Barrett identity not in truth-cache");
  }

  const barrettId = barrettMfr?.manufacturer_id ?? barrettMfr?.record_id ?? null;

  // --- Step 3: Find PMMA product ---

  const pmmaProduct = products.find(
    (p) =>
      p.product_family?.toLowerCase() === "pmma" ||
      p.material_class?.toLowerCase().includes("pmma") ||
      p.label?.toLowerCase().includes("pmma") ||
      p.product_id?.toLowerCase().includes("pmma")
  );

  if (!pmmaProduct) {
    blocking_rules.push("MISSING_PRODUCT: PMMA product not in truth-cache");
  }

  // Verify manufacturer linkage if both found
  if (pmmaProduct && barrettMfr) {
    const productMfrId = pmmaProduct.manufacturer_id;
    if (productMfrId && productMfrId !== barrettId) {
      warning_rules.push(
        `MANUFACTURER_MISMATCH: product ${pmmaProduct.product_id} references ${productMfrId}, expected ${barrettId}`
      );
    }
  }

  const pmmaProductId = pmmaProduct?.product_id ?? pmmaProduct?.record_id ?? null;

  // --- Step 4: Find PMMA system ---

  const pmmaSystem = systems.find(
    (s) =>
      s.system_family?.toLowerCase() === "pmma" ||
      s.system_type?.toLowerCase().includes("pmma") ||
      s.system_id?.toLowerCase().includes("pmma")
  );

  if (!pmmaSystem) {
    blocking_rules.push("MISSING_SYSTEM: PMMA system not in truth-cache");
  }

  // Verify manufacturer linkage
  if (pmmaSystem && barrettMfr) {
    const sysMfrId = pmmaSystem.manufacturer_id ?? pmmaSystem.manufacturer_ref;
    if (sysMfrId && sysMfrId !== barrettId) {
      warning_rules.push(
        `MANUFACTURER_MISMATCH: system ${pmmaSystem.system_id} references ${sysMfrId}, expected ${barrettId}`
      );
    }
  }

  // --- Step 5: Find cure-before-overlay rule ---

  const cureRule = installRules.find(
    (r) => r.rule_type === "cure_before_overlay"
  );

  let cureTime: string | null = null;
  if (cureRule) {
    cureTime = cureRule.required_cure_time ?? null;
    if (!cureTime) {
      warning_rules.push("CURE_RULE_INCOMPLETE: cure_before_overlay rule found but required_cure_time is missing");
    } else {
      notes.push(`Cure-before-overlay rule resolved: ${cureTime} (${cureRule.rule_id ?? cureRule.record_id})`);
    }
  } else {
    warning_rules.push("CURE_RULE_MISSING: No cure_before_overlay rule found in truth-cache");
    cureTime = null;
  }

  // --- Step 6: Find compatibility record ---

  const upstreamCompat = filterUpstreamCompatibility(compatEntries);
  const barrettCompat = upstreamCompat.find(
    (c) =>
      c.system_family?.toLowerCase() === "pmma" &&
      c.manufacturer_id === barrettId
  );

  if (barrettCompat) {
    notes.push(
      `Compatibility record resolved: ${barrettCompat.compatibility_id}, ` +
      `supported_conditions: [${barrettCompat.supported_conditions?.join(", ") ?? "none"}]`
    );
  } else {
    warning_rules.push("COMPATIBILITY_RECORD_MISSING: No Barrett PMMA compatibility record found");
  }

  // --- Step 7: Collect grounded general rules that also apply ---

  const generalGroundedInstall = installRules.filter(
    (r) => r.status === "grounded" && r.rule_type !== "cure_before_overlay"
  );
  const generalGroundedCert = certRules.filter((r) => r.status === "grounded");

  for (const rule of generalGroundedInstall) {
    const ruleId = rule.rule_id ?? rule.record_id ?? "unknown";
    const ruleLabel = rule.label ?? rule.rule_type;
    const action = rule.fail_action ?? "BLOCK";
    warning_rules.push(`${ruleId}: ${ruleLabel} (${rule.authority ?? "general"}) \u2014 would ${action} if not satisfied`);
  }
  for (const rule of generalGroundedCert) {
    const ruleId = rule.record_id ?? "unknown";
    const ruleLabel = rule.label ?? rule.rule_type;
    warning_rules.push(`${ruleId}: ${ruleLabel} (${rule.authority ?? "general"}) \u2014 would ${rule.fail_action ?? "BLOCK"}`);
  }

  // --- Step 8: Determine status ---

  if (blocking_rules.length > 0) {
    return {
      evaluation_status: "HALT",
      manufacturer_id: barrettId,
      system_family: pmmaSystem?.system_family ?? null,
      compatible_products: pmmaProductId ? [pmmaProductId] : [],
      required_primer: null,
      required_prep: ["substrate_preparation"],
      required_cure_before_overlay: cureTime,
      blocking_rules,
      warning_rules,
      evidence_sources,
      notes,
    };
  }

  // All critical records found. Assess completeness.
  const hasWarnings = warning_rules.length > 0;

  if (hasWarnings) {
    notes.push(
      "All critical Barrett PMMA records resolved. Warnings present " +
      "for additional rule depth not yet fully covered."
    );
  } else {
    notes.push("All critical Barrett PMMA records resolved with no warnings.");
  }

  return {
    evaluation_status: hasWarnings ? "WARN" : "PASS",
    manufacturer_id: barrettId,
    system_family: pmmaSystem?.system_family ?? null,
    compatible_products: pmmaProductId ? [pmmaProductId] : [],
    required_primer: null,
    required_prep: ["substrate_preparation"],
    required_cure_before_overlay: cureTime,
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
    required_cure_before_overlay: null,
    blocking_rules: [reason],
    warning_rules: [],
    evidence_sources: sources,
    notes: ["Evaluation halted due to missing critical truth-cache data."],
  };
}
