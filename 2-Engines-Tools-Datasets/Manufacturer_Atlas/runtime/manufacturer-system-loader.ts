/**
 * System Loader
 * Read-only. Fails closed on missing data.
 */
import * as fs from "fs";
import * as path from "path";
import type { SystemRecord, LoaderFailure } from "./types";

const DIR = path.resolve(__dirname, "..", "truth-cache", "systems");

export function loadSystems(): SystemRecord[] | LoaderFailure {
  if (!fs.existsSync(DIR)) {
    return { loader: "system-loader", path: DIR, reason: "truth-cache/systems/ not found" };
  }
  const files = fs.readdirSync(DIR).filter((f) => f.endsWith(".json"));
  if (files.length === 0) {
    return { loader: "system-loader", path: DIR, reason: "no system JSON files found" };
  }
  const records: SystemRecord[] = [];
  for (const file of files) {
    const parsed = JSON.parse(fs.readFileSync(path.join(DIR, file), "utf-8"));
    for (const item of Array.isArray(parsed) ? parsed : [parsed]) {
      if (!item.record_id || !["system_family", "system", "assembly"].includes(item.type)) {
        return { loader: "system-loader", path: file, reason: "invalid system record" };
      }
      records.push(item);
    }
  }
  return records;
}
