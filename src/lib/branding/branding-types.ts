export interface BrandingConfig {
  appName: string;
  companyName: string;
  logoUrl: string;
  faviconUrl: string;
  colors: BrandColors;
  density: "compact" | "comfortable" | "spacious";
}

export interface BrandColors {
  primary: string;
  secondary: string;
  accent: string;
  surface: string;
  surfaceAlt: string;
  border: string;
  text: string;
  textMuted: string;
}

export const DEFAULT_BRANDING: BrandingConfig = {
  appName: "Construction Atlas",
  companyName: "Atlas Systems",
  logoUrl: "",
  faviconUrl: "",
  colors: {
    primary: "#1e3a5f",
    secondary: "#2d5f8a",
    accent: "#f59e0b",
    surface: "#f8fafc",
    surfaceAlt: "#f1f5f9",
    border: "#e2e8f0",
    text: "#0f172a",
    textMuted: "#64748b",
  },
  density: "comfortable",
};
