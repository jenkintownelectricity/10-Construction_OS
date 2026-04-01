/**
 * Compatibility Loader
 * Read-only. Fails closed on missing data.
 * Supports both legacy shapes (constraint_id/condition_id) and
 * upstream authority shape (compatibility_id).
 */
import * as fs from "fs";
import * as path from "path";
import type { CompatibilityRecord, LoaderFailure } from "./types";

const DIR = path.resolve(__dirname, "..", "truth-cache", "compatibility");

export function loadCompatibilityMatrix(): CompatibilityRecord[] | LoaderFailure {
  if (!fs.existsSync(DIR)) {
    return { loader: "compatibility-loader", path: DIR, reason: "truth-cache/compatibility/ not found" };
  }
  const files = fs.readdirSync(DIR).filter((f) => f.endsWith(".json"));
  if (files.length === 0) {
    return { loader: "compatibility-loader", path: DIR, reason: "no compatibility JSON files found" };
  }
  const entries: CompatibilityRecord[] = [];
  for (const file of files) {
    const parsed = JSON.parse(fs.readFileSync(path.join(DIR, file), "utf-8"));
    for (const item of Array.isArray(parsed) ? parsed : [parsed]) {
      if (!item.compatibility_id && !item.constraint_id && !item.condition_id) {
        return { loader: "compatibility-loader", path: file, reason: "entry missing compatibility_id, constraint_id, and condition_id" };
      }
      entries.push(item);
    }
  }
  return entries;
}

export function filterUpstreamCompatibility(entries: CompatibilityRecord[]): CompatibilityRecord[] {
  return entries.filter((e) => "compatibility_id" in e && e.compatibility_id);
}

export function filterLegacyConstraints(entries: CompatibilityRecord[]): CompatibilityRecord[] {
  return entries.filter((e) => "constraint_id" in e && e.constraint_id);
}

export function filterLegacyConditions(entries: CompatibilityRecord[]): CompatibilityRecord[] {
  return entries.filter((e) => "condition_id" in e && e.condition_id);
}
