import type { BrandingConfig } from "./branding-types";
import { DEFAULT_BRANDING } from "./branding-types";

// In-memory store for server-side (Vercel-compatible, no filesystem)
let inMemoryBranding: BrandingConfig | null = null;

export function loadBranding(): BrandingConfig {
  if (inMemoryBranding) {
    return { ...inMemoryBranding };
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
  inMemoryBranding = merged;
  return merged;
}
