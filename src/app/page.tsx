import Link from "next/link";

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto py-12 px-6">
      <h1 className="text-3xl font-bold mb-2" style={{ color: "var(--wl-primary, #1e3a5f)" }}>
        Construction Atlas
      </h1>
      <p className="text-brand-text-muted mb-8">
        AI-Powered Construction Intelligence Platform
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link href="/settings/ai" className="card hover:shadow-md transition-shadow block">
          <h2 className="text-lg font-semibold mb-1">AI Control Plane</h2>
          <p className="text-sm text-brand-text-muted">
            Configure AI providers, models, routing policies, and connection settings.
          </p>
        </Link>

        <Link href="/branding" className="card hover:shadow-md transition-shadow block">
          <h2 className="text-lg font-semibold mb-1">Branding</h2>
          <p className="text-sm text-brand-text-muted">
            Customize white-label identity, colors, and visual appearance.
          </p>
        </Link>
      </div>
    </div>
  );
}
