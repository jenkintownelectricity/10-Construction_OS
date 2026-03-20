"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useBranding } from "@/components/branding/BrandingProvider";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard" },
  { href: "/settings/ai", label: "AI Settings" },
  { href: "/branding", label: "Branding" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { branding } = useBranding();

  return (
    <div className="min-h-screen flex flex-col">
      <header
        className="border-b px-6 py-3 flex items-center gap-6"
        style={{ backgroundColor: branding.colors.primary, borderColor: branding.colors.border }}
      >
        <div className="flex items-center gap-3">
          {branding.logoUrl && (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={branding.logoUrl} alt={branding.appName} className="h-8 w-auto" />
          )}
          <span className="font-semibold text-white text-lg">{branding.appName}</span>
        </div>
        <nav className="flex gap-1 ml-8">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                pathname === item.href
                  ? "bg-white/20 text-white"
                  : "text-white/70 hover:text-white hover:bg-white/10"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="ml-auto text-xs text-white/50">
          {branding.companyName}
        </div>
      </header>
      <main className="flex-1">{children}</main>
    </div>
  );
}
