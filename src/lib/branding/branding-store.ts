import fs from "node:fs";
import path from "node:path";
import type { BrandingConfig } from "./branding-types";
import { DEFAULT_BRANDING } from "./branding-types";

const BRANDING_PATH = path.join(process.cwd(), "branding.json");

export function loadBranding(): BrandingConfig {
  try {
    if (fs.existsSync(BRANDING_PATH)) {
      const raw = JSON.parse(fs.readFileSync(BRANDING_PATH, "utf-8"));
      return { ...DEFAULT_BRANDING, ...raw, colors: { ...DEFAULT_BRANDING.colors, ...raw.colors } };
    }
  } catch {
    // fall through
  }
  return { ...DEFAULT_BRANDING };
}

export function saveBranding(updates: Partial<BrandingConfig>): BrandingConfig {
  const current = loadBranding();
  const merged: BrandingConfig = {
    ...current,
    ...updates,
    colors: updates.colors ? { ...current.colors, ...updates.colors } : current.colors,
  };
  fs.writeFileSync(BRANDING_PATH, JSON.stringify(merged, null, 2), "utf-8");
  return merged;
}
