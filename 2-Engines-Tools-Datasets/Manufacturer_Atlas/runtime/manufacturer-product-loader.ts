/**
 * Product Loader
 * Read-only. Fails closed on missing data.
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
      if (item.type !== "product" || !item.record_id) {
        return { loader: "product-loader", path: file, reason: "invalid product record" };
      }
      records.push(item);
    }
  }
  return records;
}
