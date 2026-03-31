/**
 * Rule Loader
 * Read-only. Fails closed on missing data.
 */
import * as fs from "fs";
import * as path from "path";
import type { InstallationRuleRecord, CertificationRuleRecord, LoaderFailure } from "./types";

const INSTALL_DIR = path.resolve(__dirname, "..", "truth-cache", "rules", "installation");
const CERT_DIR = path.resolve(__dirname, "..", "truth-cache", "rules", "certification");

function loadRuleDir<T>(dir: string, loaderName: string, expectedType: string): T[] | LoaderFailure {
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
      if (item.type !== expectedType || !item.record_id) {
        return { loader: loaderName, path: file, reason: `invalid ${expectedType} record` };
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
