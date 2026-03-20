"use client";

import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from "react";
import type { BrandingConfig, BrandColors } from "@/lib/branding/branding-types";
import { DEFAULT_BRANDING } from "@/lib/branding/branding-types";

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

export function BrandingProvider({ children }: { children: ReactNode }) {
  const [branding, setBranding] = useState<BrandingConfig>(DEFAULT_BRANDING);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/branding")
      .then((r) => r.json())
      .then((data) => {
        if (data.branding) {
          setBranding(data.branding);
          applyThemeVars(data.branding.colors);
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const updateBranding = useCallback(async (updates: Partial<BrandingConfig>) => {
    const res = await fetch("/api/branding", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });
    const data = await res.json();
    if (data.branding) {
      setBranding(data.branding);
      applyThemeVars(data.branding.colors);
    }
  }, []);

  return (
    <BrandingContext.Provider value={{ branding, updateBranding, loading }}>
      {children}
    </BrandingContext.Provider>
  );
}
