"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useBranding } from "@/components/branding/BrandingProvider";
import { NAV_ROUTES } from "@/lib/routes";

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { branding } = useBranding();

  const mainRoutes = NAV_ROUTES.filter((r) => r.section === "main");
  const configRoutes = NAV_ROUTES.filter((r) => r.section === "config");

  function isActive(href: string) {
    if (href === "/") return pathname === "/";
    return pathname === href || pathname.startsWith(href + "/");
  }

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: branding.colors.surface }}>
      <header
        className="border-b px-6 py-0 flex items-center"
        style={{ backgroundColor: branding.colors.primary, borderColor: branding.colors.border }}
      >
        {/* Logo / Identity */}
        <Link href="/" className="flex items-center gap-2.5 py-3 mr-6 shrink-0">
          {branding.logoUrl ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={branding.logoUrl}
              alt={branding.appName || "Logo"}
              className="h-7 w-auto"
              onError={(e) => { (e.target as HTMLImageElement).style.display = "none"; }}
            />
          ) : (
            <div className="w-7 h-7 rounded bg-white/20 flex items-center justify-center text-white font-bold text-xs">
              {branding.appName.charAt(0) || "A"}
            </div>
          )}
          <span className="font-semibold text-white text-base">{branding.appName}</span>
        </Link>

        {/* Main Nav */}
        <nav className="flex items-center gap-0.5 overflow-x-auto">
          {mainRoutes.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-3 py-3 text-sm font-medium transition-colors border-b-2 whitespace-nowrap ${
                isActive(item.href)
                  ? "border-white text-white"
                  : "border-transparent text-white/60 hover:text-white hover:border-white/30"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        {/* Config nav */}
        <div className="ml-auto flex items-center gap-0.5 shrink-0">
          {configRoutes.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`px-2.5 py-1.5 rounded text-xs font-medium transition-colors ${
                isActive(item.href)
                  ? "bg-white/20 text-white"
                  : "text-white/50 hover:text-white hover:bg-white/10"
              }`}
            >
              {item.label}
            </Link>
          ))}
          <span className="text-xs text-white/30 ml-3 hidden lg:inline">
            {branding.companyName}
          </span>
        </div>
      </header>
      <main className="flex-1">{children}</main>
    </div>
  );
}
