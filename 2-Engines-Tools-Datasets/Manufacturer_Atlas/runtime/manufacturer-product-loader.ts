/**
 * Product Loader
 * Read-only. Fails closed on missing data.
 * Supports both legacy scaffold shape (record_id/type) and
 * upstream authority shape (product_id/product_family).
 */
import * as fs from "fs";
import * as path from "path";
import type { ProductRecord, LoaderFailure } from "./types";

const DIR = path.resolve(__dirname, "..", "truth-cache", "products");

export function loadProducts(): ProductRecord[] | LoaderFailure {
  if (!fs.existsSync(DIR)) {
    return { loader: "product-loader", path: DIR, reason: "truth-cache/products/ not found" };
  }
  const files = fs.readdirSync(DIR).filter((f) => f.endsWith(".json"));
  if (files.length === 0) {
    return { loader: "product-loader", path: DIR, reason: "no product JSON files found" };
  }
  const records: ProductRecord[] = [];
  for (const file of files) {
    const parsed = JSON.parse(fs.readFileSync(path.join(DIR, file), "utf-8"));
    for (const item of Array.isArray(parsed) ? parsed : [parsed]) {
      const hasLegacy = item.record_id && item.type === "product";
      const hasUpstream = item.product_id && item.product_family;
      if (!hasLegacy && !hasUpstream) {
        return { loader: "product-loader", path: file, reason: "record missing both record_id/type and product_id/product_family" };
      }
      records.push(item);
    }
  }
  return records;
}
