/**
 * Manufacturer Record Loader
 * Read-only. Fails closed on missing data.
 * Does not own truth — consumed upstream reference only.
 */
import * as fs from "fs";
import * as path from "path";
import type { ManufacturerRecord, LoaderFailure } from "./types";

const DIR = path.resolve(__dirname, "..", "truth-cache", "manufacturers");

export function loadManufacturers(): ManufacturerRecord[] | LoaderFailure {
  if (!fs.existsSync(DIR)) {
    return { loader: "manufacturer-record-loader", path: DIR, reason: "truth-cache/manufacturers/ not found" };
  }
  const files = fs.readdirSync(DIR).filter((f) => f.endsWith(".json"));
  if (files.length === 0) {
    return { loader: "manufacturer-record-loader", path: DIR, reason: "no manufacturer JSON files found" };
  }
  const records: ManufacturerRecord[] = [];
  for (const file of files) {
    const parsed = JSON.parse(fs.readFileSync(path.join(DIR, file), "utf-8"));
    if (parsed.type !== "manufacturer" || !parsed.record_id) {
      return { loader: "manufacturer-record-loader", path: file, reason: "invalid manufacturer record" };
    }
    records.push(parsed);
  }
  return records;
}
