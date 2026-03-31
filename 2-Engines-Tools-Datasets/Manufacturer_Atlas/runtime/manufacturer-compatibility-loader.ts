/**
 * Compatibility Loader
 * Read-only. Fails closed on missing data.
 */
import * as fs from "fs";
import * as path from "path";
import type { CompatibilityEntry, ConstraintRecord, ConditionRecord, LoaderFailure } from "./types";

const DIR = path.resolve(__dirname, "..", "truth-cache", "compatibility");

export function loadCompatibilityMatrix(): CompatibilityEntry[] | LoaderFailure {
  if (!fs.existsSync(DIR)) {
    return { loader: "compatibility-loader", path: DIR, reason: "truth-cache/compatibility/ not found" };
  }
  const files = fs.readdirSync(DIR).filter((f) => f.endsWith(".json"));
  if (files.length === 0) {
    return { loader: "compatibility-loader", path: DIR, reason: "no compatibility JSON files found" };
  }
  const entries: CompatibilityEntry[] = [];
  for (const file of files) {
    const parsed = JSON.parse(fs.readFileSync(path.join(DIR, file), "utf-8"));
    for (const item of Array.isArray(parsed) ? parsed : [parsed]) {
      if (!item.constraint_id && !item.condition_id) {
        return { loader: "compatibility-loader", path: file, reason: "entry missing both constraint_id and condition_id" };
      }
      entries.push(item);
    }
  }
  return entries;
}

export function filterConstraints(entries: CompatibilityEntry[]): ConstraintRecord[] {
  return entries.filter((e): e is ConstraintRecord => "constraint_id" in e);
}

export function filterConditions(entries: CompatibilityEntry[]): ConditionRecord[] {
  return entries.filter((e): e is ConditionRecord => "condition_id" in e);
}
