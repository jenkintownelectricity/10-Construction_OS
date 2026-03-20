import fs from "node:fs";
import path from "node:path";
import type { BrandingConfig } from "./branding-types";
import { DEFAULT_BRANDING } from "./branding-types";

const BRANDING_PATH = path.join(process.cwd(), "branding.json");

let cached: BrandingConfig | null = null;

export function loadBranding(): BrandingConfig {
  if (cached) return cached;
  try {
    if (fs.existsSync(BRANDING_PATH)) {
      const raw = JSON.parse(fs.readFileSync(BRANDING_PATH, "utf-8"));
      const result: BrandingConfig = { ...DEFAULT_BRANDING, ...raw, colors: { ...DEFAULT_BRANDING.colors, ...raw.colors } };
      cached = result;
      return result;
    }
  } catch {
    // fall through
  }
  cached = { ...DEFAULT_BRANDING };
  return cached;
}

export function saveBranding(updates: Partial<BrandingConfig>): BrandingConfig {
  const current = loadBranding();
  const merged: BrandingConfig = {
    ...current,
    ...updates,
    colors: updates.colors ? { ...current.colors, ...updates.colors } : current.colors,
  };
  fs.writeFileSync(BRANDING_PATH, JSON.stringify(merged, null, 2), "utf-8");
  cached = merged;
  return merged;
}
