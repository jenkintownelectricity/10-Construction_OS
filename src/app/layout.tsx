import type { Metadata } from "next";
import "./globals.css";
import { AppShell } from "@/components/ui/AppShell";
import { BrandingProvider } from "@/components/branding/BrandingProvider";

export const metadata: Metadata = {
  title: "Construction Atlas",
  description: "Construction Atlas — AI-Powered Construction Intelligence Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased">
        <BrandingProvider>
          <AppShell>{children}</AppShell>
        </BrandingProvider>
      </body>
    </html>
  );
}
