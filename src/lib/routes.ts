export interface NavRoute {
  href: string;
  label: string;
  section: "main" | "config";
}

export const NAV_ROUTES: NavRoute[] = [
  { href: "/", label: "Dashboard", section: "main" },
  { href: "/atlas", label: "Atlas", section: "main" },
  { href: "/projects", label: "Projects", section: "main" },
  { href: "/details", label: "Details", section: "main" },
  { href: "/manufacturers", label: "Manufacturers", section: "main" },
  { href: "/observations", label: "Observations", section: "main" },
  { href: "/artifacts", label: "Artifacts", section: "main" },
  { href: "/settings/ai", label: "AI Settings", section: "config" },
  { href: "/branding", label: "Branding", section: "config" },
];
