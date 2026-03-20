"use client";

import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from "react";
import type { BrandingConfig, BrandColors } from "@/lib/branding/branding-types";
import { DEFAULT_BRANDING } from "@/lib/branding/branding-types";

const STORAGE_KEY = "construction-atlas-branding";

interface BrandingContextValue {
  branding: BrandingConfig;
  updateBranding: (updates: Partial<BrandingConfig>) => Promise<void>;
  loading: boolean;
}

const BrandingContext = createContext<BrandingContextValue>({
  branding: DEFAULT_BRANDING,
  updateBranding: async () => {},
  loading: true,
});

export function useBranding() {
  return useContext(BrandingContext);
}

function applyThemeVars(colors: BrandColors) {
  const root = document.documentElement;
  root.style.setProperty("--wl-primary", colors.primary);
  root.style.setProperty("--wl-secondary", colors.secondary);
  root.style.setProperty("--wl-accent", colors.accent);
  root.style.setProperty("--wl-surface", colors.surface);
  root.style.setProperty("--wl-surface-alt", colors.surfaceAlt);
  root.style.setProperty("--wl-border", colors.border);
  root.style.setProperty("--wl-text", colors.text);
  root.style.setProperty("--wl-text-muted", colors.textMuted);
}

function loadFromStorage(): BrandingConfig {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      return {
        ...DEFAULT_BRANDING,
        ...parsed,
        colors: { ...DEFAULT_BRANDING.colors, ...parsed.colors },
      };
    }
  } catch {
    // fall through
  }
  return { ...DEFAULT_BRANDING };
}

function saveToStorage(config: BrandingConfig) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
  } catch {
    // storage full or unavailable
  }
}

export function BrandingProvider({ children }: { children: ReactNode }) {
  const [branding, setBranding] = useState<BrandingConfig>(DEFAULT_BRANDING);
  const [loading, setLoading] = useState(true);

  // Load from localStorage immediately on mount — no API call needed
  useEffect(() => {
    const saved = loadFromStorage();
    setBranding(saved);
    applyThemeVars(saved.colors);
    setLoading(false);
  }, []);

  const updateBranding = useCallback(async (updates: Partial<BrandingConfig>) => {
    setBranding((prev) => {
      const merged: BrandingConfig = {
        ...prev,
        ...updates,
        colors: updates.colors ? { ...prev.colors, ...updates.colors } : prev.colors,
      };
      saveToStorage(merged);
      applyThemeVars(merged.colors);
      return merged;
    });
  }, []);

  return (
    <BrandingContext.Provider value={{ branding, updateBranding, loading }}>
      {children}
    </BrandingContext.Provider>
  );
}
