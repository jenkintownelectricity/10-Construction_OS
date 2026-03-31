/**
 * Rule Loader
 * Read-only. Fails closed on missing data.
 * Supports both legacy scaffold shape (record_id/type) and
 * upstream authority shape (rule_id/rule_type).
 */
import * as fs from "fs";
import * as path from "path";
import type { InstallationRuleRecord, CertificationRuleRecord, LoaderFailure } from "./types";

const INSTALL_DIR = path.resolve(__dirname, "..", "truth-cache", "rules", "installation");
const CERT_DIR = path.resolve(__dirname, "..", "truth-cache", "rules", "certification");

function loadRuleDir<T>(dir: string, loaderName: string, expectedLegacyType: string): T[] | LoaderFailure {
  if (!fs.existsSync(dir)) {
    return { loader: loaderName, path: dir, reason: `${dir} not found` };
  }
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));
  if (files.length === 0) {
    return { loader: loaderName, path: dir, reason: "no rule JSON files found" };
  }
  const records: T[] = [];
  for (const file of files) {
    const parsed = JSON.parse(fs.readFileSync(path.join(dir, file), "utf-8"));
    for (const item of Array.isArray(parsed) ? parsed : [parsed]) {
      const hasLegacy = item.record_id && item.type === expectedLegacyType;
      const hasUpstream = item.rule_id && item.rule_type;
      if (!hasLegacy && !hasUpstream) {
        return { loader: loaderName, path: file, reason: `record missing both record_id/type and rule_id/rule_type` };
      }
      records.push(item);
    }
  }
  return records;
}

export function loadInstallationRules(): InstallationRuleRecord[] | LoaderFailure {
  return loadRuleDir<InstallationRuleRecord>(INSTALL_DIR, "rule-loader/installation", "installation_rule");
}

export function loadCertificationRules(): CertificationRuleRecord[] | LoaderFailure {
  return loadRuleDir<CertificationRuleRecord>(CERT_DIR, "rule-loader/certification", "certification_rule");
}
