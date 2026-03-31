/**
 * Manufacturer Record Loader
 * Read-only. Fails closed on missing data.
 * Supports both legacy scaffold shape (record_id/type) and
 * upstream authority shape (manufacturer_id/name).
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
    const hasLegacyId = parsed.record_id && parsed.type === "manufacturer";
    const hasUpstreamId = parsed.manufacturer_id && parsed.name;
    if (!hasLegacyId && !hasUpstreamId) {
      return { loader: "manufacturer-record-loader", path: file, reason: "record missing both record_id/type and manufacturer_id/name" };
    }
    records.push(parsed);
  }
  return records;
}
